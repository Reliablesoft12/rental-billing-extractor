from flask import Flask, render_template, request, send_file, jsonify
import imaplib
import email
from email.header import decode_header
import re
import os
import PyPDF2
import pandas as pd
from datetime import datetime
import io
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Regex patterns
amount_pattern = re.compile(r'Due\s*Amount\s*</td>\s*<td>:\s*</td>\s*<td[^>]*>(.*?)</td>', re.IGNORECASE)
opid_pattern = re.compile(r'OperatorID\s*</td>\s*<td>:\s*</td>\s*<td[^>]*>([A-Z0-9]+)</td>', re.IGNORECASE)
expiry_pattern = re.compile(r'Due\s*Date\s*</td>\s*<td>:\s*</td>\s*<td[^>]*>(\d{2}-\w{3}-\d{4})</td>', re.IGNORECASE)

# PDF patterns
balance_pattern = re.compile(r'Balance\s*Amount\s*\(A\+B-C\)\s*[:\s]*([\d.,]+)\s*(Dr|Cr)?', re.IGNORECASE)
balance_fallback_pattern = re.compile(r'Balance\s*Amount.*?([\d.,]+)\s*(Dr|Cr)', re.IGNORECASE)


def convert_balance(amount, balance_type=None):
    """Convert balance amount with Dr/Cr indicator
    Returns negative value for Cr (credit), positive for Dr (debit)
    """
    amount = str(amount).replace(",", "").strip()
    
    # Check if type is in the amount string
    if amount.lower().endswith("cr"):
        return f"-{amount[:-2].strip()}"
    elif amount.lower().endswith("dr"):
        return amount[:-2].strip()
    # Check separate balance_type parameter
    elif balance_type:
        if balance_type.lower().strip() == "cr":
            return f"-{amount}"
        elif balance_type.lower().strip() == "dr":
            return amount
    
    return amount


def extract_from_pdf_bytes(pdf_bytes, filename="attachment.pdf"):
    """Extract Balance Amount (A+B-C) from PDF bytes"""
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + " "

        # Clean up newlines/spaces
        cleaned_text = re.sub(r'\s+', ' ', text)

        # Try primary pattern: Balance Amount (A+B-C)
        match = balance_pattern.search(cleaned_text)
        if match:
            amount = match.group(1).strip()
            balance_type = match.group(2) if len(match.groups()) > 1 else None
            result = convert_balance(amount, balance_type)
            print(f"Found Balance Amount (A+B-C) in {filename}: {result}")
            return result
        
        # Try fallback pattern
        match = balance_fallback_pattern.search(cleaned_text)
        if match:
            amount = match.group(1).strip()
            balance_type = match.group(2) if len(match.groups()) > 1 else None
            result = convert_balance(amount, balance_type)
            print(f"Found Balance Amount (fallback) in {filename}: {result}")
            return result
            
        print(f"No balance found in {filename}")
        return None
        
    except Exception as e:
        print(f"ERROR reading PDF '{filename}': {e}")
        return None


def connect_imap(email_address, password, imap_server):
    """Connect to email via IMAP"""
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        return mail
    except Exception as e:
        raise Exception(f"Failed to connect to IMAP server: {str(e)}")


def process_emails(email_address, password, imap_server, filter_date):
    """Process emails and extract data"""
    data = []
    
    try:
        mail = connect_imap(email_address, password, imap_server)
        mail.select('inbox')
        
        # Format date for IMAP search
        date_str = filter_date.strftime('%d-%b-%Y')
        
        # Search for emails on specific date
        status, messages = mail.search(None, f'(ON {date_str})')
        
        if status != 'OK':
            return data, "Failed to search emails"
        
        email_ids = messages[0].split()
        print(f"Found {len(email_ids)} emails on {date_str}")
        
        for email_id in email_ids:
            try:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                
                if status != 'OK':
                    continue
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode subject
                        subject = ""
                        if msg["Subject"]:
                            decoded = decode_header(msg["Subject"])[0]
                            if isinstance(decoded[0], bytes):
                                subject = decoded[0].decode(decoded[1] or 'utf-8')
                            else:
                                subject = decoded[0]
                        
                        print(f"Processing: {subject}")
                        
                        # Check if it's a rental invoice
                        if ("Invoice for R-Soft-SMS: Rental for the Month" in subject or
                            "Invoice for CNMS ON-Net" in subject):
                            
                            html_body = ""
                            attachments = []
                            
                            # Extract HTML body and attachments
                            if msg.is_multipart():
                                for part in msg.walk():
                                    content_type = part.get_content_type()
                                    
                                    if content_type == "text/html":
                                        try:
                                            html_body = part.get_payload(decode=True).decode()
                                        except:
                                            pass
                                    
                                    # Check for PDF attachments
                                    if part.get_filename() and part.get_filename().lower().endswith('.pdf'):
                                        attachments.append({
                                            'filename': part.get_filename(),
                                            'data': part.get_payload(decode=True)
                                        })
                            else:
                                if msg.get_content_type() == "text/html":
                                    html_body = msg.get_payload(decode=True).decode()
                            
                            # Extract data from HTML
                            amount_match = amount_pattern.search(html_body)
                            opid_match = opid_pattern.search(html_body)
                            expiry_match = expiry_pattern.search(html_body)
                            
                            amount = amount_match.group(1).replace("&nbsp;", "").strip() if amount_match else "NA"
                            opid = opid_match.group(1) if opid_match else "NA"
                            expiry_date = expiry_match.group(1) if expiry_match else "NA"
                            
                            # If amount is NIL/0, extract from PDF
                            if amount.lower() in ["nil", "na", "0", "0.00", ""]:
                                print(f"  Due amount is NIL ({amount}), checking PDF...")
                                for attachment in attachments:
                                    balance_value = extract_from_pdf_bytes(
                                        attachment['data'],
                                        attachment['filename']
                                    )
                                    if balance_value:
                                        amount = balance_value
                                        print(f"  ✓ Using balance from PDF: {balance_value}")
                                        break
                            
                            data.append({
                                'Amount/Balance': amount,
                                'OPID': opid,
                                'Expiry Date': expiry_date
                            })
                            
                            print(f"  Extracted - Amount: {amount}, OPID: {opid}, Expiry: {expiry_date}")
                            
            except Exception as e:
                print(f"Error processing email {email_id}: {e}")
                continue
        
        mail.close()
        mail.logout()
        
        return data, None
        
    except Exception as e:
        return data, str(e)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/extract', methods=['POST'])
def extract_data():
    try:
        # Get form data
        email_address = request.form.get('email')
        password = request.form.get('password')
        imap_server = request.form.get('imap_server', 'imap.gmail.com')
        date_str = request.form.get('date')
        
        if not all([email_address, password, date_str]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Parse date
        try:
            filter_date = datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Process emails
        data, error = process_emails(email_address, password, imap_server, filter_date)
        
        if error:
            return jsonify({'error': error}), 500
        
        if not data:
            return jsonify({'error': 'No matching emails found'}), 404
        
        # Create Excel file in memory (no server storage)
        df = pd.DataFrame(data)
        
        # Generate Excel file directly in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Email Data')
        output.seek(0)
        
        # Generate filename with timestamp
        filename = f'email_data_{filter_date.strftime("%Y%m%d")}_{datetime.now().strftime("%H%M%S")}.xlsx'
        
        # Send file directly to user browser (no server storage)
        # File is created in memory and sent, then automatically garbage collected
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"Error in extract_data: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
