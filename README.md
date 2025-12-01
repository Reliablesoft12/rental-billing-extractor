# Rental Billing Email Extractor

A secure, web-based application to extract rental billing data from emails and generate Excel reports.

## 🎯 Features

- ✅ **Web Interface**: No need for local Outlook installation
- ✅ **IMAP Support**: Works with Gmail, Outlook, Yahoo, and any IMAP server
- ✅ **Smart PDF Extraction**: Automatically extracts balance from PDFs when due amount is NIL
- ✅ **Credit Balance Handling**: Converts credit balances to negative values (e.g., 4632 Cr → -4632)
- ✅ **Excel Download**: Generates and downloads Excel files with extracted data
- ✅ **Date Filtering**: Extract data for specific dates
- ✅ **Enhanced Logging**: Detailed console output for debugging
- ✅ **Zero Storage**: No credentials or files stored on server
- ✅ **Secure**: HTTPS encrypted, credentials used only during request

## Installation

### Option 1: Local Python Script (Original)

1. Install dependencies:
```bash
pip install pywin32 PyPDF2
```

2. Run the script:
```bash
python extract_email_data.py
```

### Option 2: Web Application (New!)

1. Navigate to the webapp folder:
```bash
cd webapp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask application:
```bash
python app.py
```

4. Open your browser and go to:
```
http://localhost:5000
```

## 🚀 Quick Deploy to GitHub & Cloud

### Step 1: Push to GitHub
```powershell
cd webapp
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/rental-billing-extractor.git
git push -u origin main
```

### Step 2: Deploy to Render (Free)
1. Go to https://render.com
2. Sign up with GitHub
3. New → Web Service → Select your repo
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn app:app`
6. Click Create

**Done!** Share the URL with your team: `https://your-app.onrender.com`

For detailed deployment options, see [GIT_DEPLOYMENT.md](GIT_DEPLOYMENT.md)

---

## 📱 How to Use the Web Application

1. **Enter Email Credentials**:
   - Email address (the mailbox to extract from)
   - Password or App-specific password
   - Select your email provider (Gmail, Outlook, Yahoo, or custom)

2. **Select Date**:
   - Choose the date of emails you want to process

3. **Click "Extract & Download Excel"**:
   - The system will process emails and extract data
   - If due amount is NIL/0, it will automatically extract balance from attached PDFs
   - Excel file will be downloaded automatically

## 🔒 Security & Privacy

**How Credentials Work:**
```
User Browser → [HTTPS] → Server → IMAP Server
                           ↓
                    Credentials used ONLY during request
                           ↓
                    Immediately discarded after use
                           ↓
                    NEVER stored anywhere
```

**How Files Work:**
```
Extract data from emails
    ↓
Generate Excel in RAM (memory)
    ↓
Send to user's browser
    ↓
Memory cleared automatically
```

**What's Stored:**
- ✅ Application code (Python files)
- ❌ Email credentials (NEVER)
- ❌ Excel files (NEVER)
- ❌ User data (NEVER)

**Result: Zero storage, maximum security!** 🔐

## Important Notes

### For Gmail Users:
- You need to enable "Less secure app access" OR use an App Password
- To create an App Password:
  1. Go to Google Account settings
  2. Security → 2-Step Verification
  3. App passwords → Generate new password
  4. Use this password in the application

### For Outlook/Office365 Users:
- Use your regular password or create an App Password
- Ensure IMAP is enabled in your Outlook settings

### PDF Balance Extraction:
- When "Due Amount" in email HTML is NIL, NA, or 0
- System automatically looks for PDF attachments
- Extracts "Balance Amount (A+B-C)" from PDF
- Handles both Debit (Dr) and Credit (Cr) balances
- Credit balances are shown as negative numbers (e.g., -4632)

## Email Format Expected

The application looks for emails with subjects:
- "Invoice for R-Soft-SMS: Rental for the Month"
- "Invoice for CNMS ON-Net"

And extracts:
- Due Amount (from HTML body)
- OperatorID (OPID)
- Expiry Date
- Balance Amount from PDF (if due is NIL)

## Output

The Excel file contains three columns:
- **Amount/Balance**: Due amount or balance (negative if credit)
- **OPID**: Operator ID
- **Expiry Date**: Due date in dd-MMM-yyyy format

## Troubleshooting

### Cannot connect to IMAP server:
- Check your internet connection
- Verify IMAP is enabled for your email account
- Try using an app-specific password

### No data extracted:
- Verify emails exist for the selected date
- Check that email subjects match the expected format
- Review console logs for detailed error messages

### PDF extraction fails:
- Ensure PDF attachments are present in emails
- Check that PDFs contain "Balance Amount (A+B-C)" text
- Review console output for PDF extraction details

## Project Structure

```
Rental Billing Automation/
├── extract_email_data.py          # Original local script (with improvements)
└── webapp/                        # Web application
    ├── app.py                     # Flask application
    ├── requirements.txt           # Python dependencies
    └── templates/
        └── index.html             # Web interface
```

## Future Enhancements

Potential improvements:
- 🔄 Batch date processing (process multiple dates at once)
- 📊 Dashboard with statistics and charts
- 📧 Email notifications when processing completes
- 🗄️ Database integration for historical data
- 🔐 User authentication and multi-user support
- ☁️ Cloud deployment (AWS, Azure, Heroku)
- 📱 Mobile-responsive design improvements
- 🔍 Advanced search and filtering options

## License

This project is for internal use. Please ensure you comply with your email provider's terms of service when using IMAP access.

## Support

For issues or questions, please contact the development team.
