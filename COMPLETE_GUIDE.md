# 📧 Rental Billing Email Extractor - Complete Guide

## 🎯 What This Does

Extracts rental billing data from emails and generates Excel files with:
- Due Amount / Balance (negative for credits)
- Operator ID (OPID)
- Expiry Date

**Special Features:**
- When due amount is NIL, automatically extracts balance from PDF
- Converts credit balances to negative (e.g., 4632 Cr → -4632)
- Works from anywhere via web browser
- No storage of credentials or files

---

## 🚀 Complete Setup (3 Easy Steps)

### Step 1: Test Locally (5 minutes)

```powershell
# Navigate to webapp folder
cd webapp

# Run the test script
.\run_local.ps1
```

Open http://localhost:5000 in your browser and test!

### Step 2: Push to GitHub (2 minutes)

```powershell
# Run the setup script (it will guide you)
.\setup_git.ps1
```

It will ask for:
- Your GitHub username
- Repository name (default: rental-billing-extractor)

**Important**: Create the repository on GitHub FIRST (without initializing)

### Step 3: Deploy to Render (3 minutes)

1. Go to https://render.com
2. Sign up with GitHub
3. Click **New +** → **Web Service**
4. Select your repository: `rental-billing-extractor`
5. Settings:
   - Name: `rental-billing-extractor`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Plan: **Free**
6. Click **Create Web Service**

Wait 2-3 minutes... Done! 🎉

Your app is live at: `https://rental-billing-extractor.onrender.com`

---

## 📱 How Users Access It

1. Share the URL with your team
2. They open it in any browser (desktop/mobile)
3. Enter their email credentials:
   - Email address
   - Password (or App Password for Gmail)
   - Select provider (Gmail/Outlook/Yahoo)
4. Choose date
5. Click "Extract & Download Excel"
6. File downloads to their device

**That's it!** No installation, no setup, just works! ✨

---

## 🔐 Security Questions Answered

### "Where are my credentials stored?"
**NOWHERE!** They're only used during the request to connect to IMAP, then immediately discarded.

```
Your Browser [HTTPS] → Server (uses credentials) → IMAP Server
                            ↓
                     Credentials discarded
                     (NOT stored anywhere)
```

### "Where are Excel files stored?"
**NOWHERE!** Files are generated in memory (RAM) and sent directly to your browser.

```
Data extracted → Excel created in RAM → Sent to your browser → RAM cleared
```

No files are ever saved on the server!

### "Is my data safe?"
Yes!
- ✅ Connection is HTTPS encrypted
- ✅ No credentials stored
- ✅ No files stored
- ✅ No logs of sensitive data
- ✅ Stateless application

---

## 💰 Cost Breakdown

### Free Tier (Perfect for teams up to 10-20 people):

| What | Cost | Limits |
|------|------|--------|
| **GitHub** | $0 | Unlimited repos (public) |
| **Render** | $0 | 750 hours/month |
| **Storage** | $0 | No storage needed! |
| **Bandwidth** | $0 | Reasonable usage included |

**Total Monthly Cost: $0** 🎉

### Paid Tier (If you need 24/7 uptime):

| What | Cost | Benefits |
|------|------|----------|
| **Render Starter** | $7/month | No sleep, faster, always on |

**Total Monthly Cost: $7** (only if you need always-on service)

---

## 🎯 For Different Email Providers

### Gmail Users

**Setup App Password:**
1. Google Account → Security → 2-Step Verification (enable it)
2. App passwords → Generate new
3. Select "Mail" and device
4. Copy the 16-character password
5. Use this password in the app (not your Gmail password)

**IMAP Server:** Already selected (imap.gmail.com)

### Outlook/Office365 Users

**Enable IMAP:**
1. Outlook.com → Settings → View all Outlook settings
2. Mail → Sync email → Let devices and apps use IMAP
3. Save

**IMAP Server:** Select "Outlook/Office365"

### Yahoo Mail Users

**Setup App Password:**
1. Yahoo Account → Account Security
2. Generate app password
3. Use this password in the app

**IMAP Server:** Select "Yahoo Mail"

### Custom IMAP Server

If your company has a custom mail server:
1. Select "Custom Server"
2. Enter your IMAP server address (e.g., mail.company.com)
3. Enter credentials

---

## 📊 Workflow Diagram

```
┌─────────────┐
│   User      │
│  Browser    │
└──────┬──────┘
       │ 1. Enter credentials & date
       ▼
┌─────────────────────────────────┐
│  Web App (Render/Cloud)         │
│  • Receives credentials          │
│  • NOT stored!                   │
└──────┬──────────────────┬───────┘
       │ 2. Connect       │ 6. Send Excel
       ▼                  ▼
┌──────────────┐    ┌─────────────┐
│ IMAP Server  │    │ User Browser│
│ (Gmail, etc) │    │ (Download)  │
└──────┬───────┘    └─────────────┘
       │ 3. Fetch emails
       ▼
┌──────────────────────────┐
│  Email Processing        │
│  • Extract data from HTML│
│  • If due=NIL, check PDF │
│  • Parse balance         │
└──────┬───────────────────┘
       │ 4. Generate Excel in memory
       ▼
┌─────────────────────┐
│ Excel file (in RAM) │
│ • NOT saved to disk │
│ • Sent to browser   │
│ • RAM cleared       │
└─────────────────────┘
```

---

## 🛠️ Troubleshooting

### App won't load / "This site can't be reached"
**Cause:** Free tier apps sleep after 15 min of inactivity  
**Fix:** Wait 30-60 seconds for it to wake up  
**Note:** First request of the day is always slow

### "Authentication failed" / "Cannot connect to email"

**For Gmail:**
- ✓ Use App Password, not regular password
- ✓ Enable 2-Step Verification first
- ✓ Enable IMAP in settings

**For Outlook:**
- ✓ Enable IMAP in Outlook settings
- ✓ Use outlook.office365.com as server
- ✓ Check password is correct

**For all:**
- ✓ Check internet connection
- ✓ Verify credentials in regular email client first

### "No emails found"
- ✓ Check date is correct
- ✓ Verify emails exist for that date
- ✓ Check subject line matches expected format:
  - "Invoice for R-Soft-SMS: Rental for the Month"
  - "Invoice for CNMS ON-Net"

### "PDF extraction failed"
- ✓ Ensure PDF is attached to email
- ✓ Check PDF contains "Balance Amount (A+B-C)"
- ✓ Verify PDF is not password protected
- ✓ Check logs for specific error

---

## 📈 Usage Tips

### For Administrators:
- Share URL with bookmark icon for easy access
- Create a shortcut on desktop
- Add to favorites/bookmarks
- Pin browser tab

### For Users:
- Bookmark the URL
- First load may take 30-60 seconds (normal for free tier)
- Subsequent loads are instant
- Use App Passwords for better security
- Download files are date-stamped

### For Multiple Dates:
- Run multiple times with different dates
- Each extraction is independent
- No limit on number of extractions

---

## 🔄 Updating the App

Made changes to code?

```powershell
# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push

# Render automatically redeploys in 2-3 minutes!
```

---

## 📞 Support

### Check Status:
- **App Logs:** Render Dashboard → Your Service → Logs
- **GitHub:** Check repository for latest code
- **Render Status:** Check if service is running

### Common Solutions:
1. **App slow:** Normal for free tier, wait for wake-up
2. **Credentials error:** Use App Password, not regular password
3. **No data:** Check date and email subject format
4. **PDF error:** Verify PDF format and content

---

## 🎓 Training for New Users

**Share this quick guide with new users:**

```
Rental Billing Extractor - Quick Guide

1. Go to: [YOUR_URL_HERE]

2. Enter Details:
   - Email: your.email@company.com
   - Password: Your App Password (not regular password!)
   - Provider: Select Gmail/Outlook/Yahoo
   - Date: Select date to extract

3. Click: "Extract & Download Excel"

4. Wait: 10-30 seconds (processing emails)

5. Done: File downloads automatically to your computer

Notes:
• First load may take 1 minute (app waking up)
• Credentials NOT stored (safe to use)
• Files NOT stored on server
• Use App Password for Gmail/Outlook

Questions? Contact [YOUR_NAME]
```

---

## 🎉 Success Checklist

- [ ] Tested locally with `run_local.ps1`
- [ ] Pushed to GitHub with `setup_git.ps1`
- [ ] Deployed to Render
- [ ] Tested with real email account
- [ ] Verified credit balances show as negative
- [ ] Confirmed PDF extraction works for NIL amounts
- [ ] Shared URL with team
- [ ] Bookmarked the URL
- [ ] Created App Passwords for Gmail users
- [ ] Documented URL and credentials for team

---

## 🚀 Next Steps

**Immediate:**
1. Deploy and test
2. Share with team
3. Monitor usage

**Future Enhancements:**
- Add user authentication
- Batch date processing
- Email notifications
- Data analytics dashboard
- Export to other formats
- Schedule automatic extractions

---

**You're all set! 🎊**

Your team can now extract billing data from anywhere, anytime, with zero storage and maximum security!

Questions? Check the other documentation files:
- `README.md` - Overview and features
- `GIT_DEPLOYMENT.md` - Detailed deployment options
- `DEPLOYMENT.md` - Advanced deployment scenarios
- `QUICK_START.md` - Ultra-quick setup guide
