# 🚀 Quick Start Guide

## Get Your App Online in 5 Minutes!

### Option 1: Deploy to Render (Recommended - FREE)

1. **Push to GitHub**:
   ```powershell
   cd webapp
   git init
   git add .
   git commit -m "Initial commit"
   
   # Create repo on github.com, then:
   git remote add origin https://github.com/YOUR_USERNAME/rental-billing-extractor.git
   git push -u origin main
   ```

2. **Deploy to Render**:
   - Go to https://render.com
   - Sign up with GitHub
   - Click **New +** → **Web Service**
   - Select your repository
   - Name: `rental-billing-extractor`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Click **Create**

3. **Done!** Your app is live at: `https://rental-billing-extractor.onrender.com`

---

## How to Use

### For Users:
1. Go to your deployed URL
2. Enter email credentials:
   - Email: `renewal@reliablesoft.co.in`
   - Password: Your email password or app password
   - Select provider: Gmail/Outlook/Yahoo/Custom
3. Choose date to extract
4. Click "Extract & Download Excel"
5. Excel file downloads directly to your device

### Important:
- ✅ **No registration needed** - Just use directly
- ✅ **Credentials NOT stored** - Only used during extraction
- ✅ **Files NOT stored on server** - Direct download
- ✅ **No storage limits** - Everything in memory
- ✅ **Access from anywhere** - Just need the URL

---

## How It Works - Security & Storage

### Email Credentials:
```
User enters credentials in browser
    ↓
Sent securely to server (HTTPS)
    ↓
Used to connect to IMAP server
    ↓
Fetch emails
    ↓
Credentials discarded immediately
```

**Result**: Zero credential storage! 🔒

### File Generation:
```
Extract data from emails
    ↓
Generate Excel in memory (RAM)
    ↓
Send directly to user's browser
    ↓
Memory automatically cleared
```

**Result**: Zero file storage! 💾

### What Gets Stored:
- **Application code** (Python files) ✅
- **Dependencies** (libraries) ✅
- **Email credentials** ❌ Never!
- **Excel files** ❌ Never!
- **User data** ❌ Never!

---

## Share with Your Team

Just send them the URL!

**Example message to team**:
```
Hi team,

Use this tool to extract rental billing data:
https://rental-billing-extractor.onrender.com

How to use:
1. Enter your email credentials (not stored, only used during extraction)
2. Select the date
3. Click "Extract & Download Excel"
4. File downloads to your computer

Note: First load may take 30-60 seconds (free tier wakes up).

Questions? Contact [your name]
```

---

## Troubleshooting

### "App not loading" or "This site can't be reached"
- **Cause**: Free tier apps sleep after 15 min of inactivity
- **Fix**: Wait 30-60 seconds, it's waking up
- **Prevention**: First request of the day is always slow

### "Cannot connect to email server"
**For Gmail**:
1. Enable IMAP: Settings → Forwarding and POP/IMAP → Enable IMAP
2. Create App Password:
   - Google Account → Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Use this password in the app

**For Outlook**:
1. Server: `outlook.office365.com`
2. Enable IMAP in Outlook settings
3. Use regular password or app password

### "No emails found"
- Check the date is correct
- Verify emails exist for that date
- Ensure subject line matches expected format

---

## Cost Breakdown

### Free Deployment Options:

| Platform | Monthly Cost | Perfect For |
|----------|--------------|-------------|
| **Render** | $0 | Small teams, internal use |
| **Heroku** | $0 | Testing, development |
| **Railway** | $0 ($5 credit) | Quick deployment |

### Paid Options (if needed):

| Platform | Monthly Cost | Benefits |
|----------|--------------|----------|
| **Render** | $7/month | No sleep, faster, more resources |
| **Heroku** | $7/month | No sleep, custom domain |
| **Railway** | Pay-as-you-go | Scale automatically |

**For internal team use, FREE tier is perfect!** 💰

---

## Monitoring

### Check App Status:
- **Render**: Dashboard → Your Service → Logs
- **Heroku**: `heroku logs --tail`
- **Railway**: Dashboard → Logs

### What to Monitor:
- Successful extractions
- Failed IMAP connections (wrong credentials)
- PDF extraction issues
- Error messages

---

## Updating the App

Made changes to code?

```powershell
# Commit changes
git add .
git commit -m "Your change description"

# Push to GitHub
git push

# Render/Railway auto-redeploy!
# For Heroku: git push heroku main
```

Wait 2-3 minutes, changes are live! 🎉

---

## FAQ

**Q: Is it safe to enter email password?**
A: Yes! Connection is HTTPS encrypted, credentials never stored, only used during that request.

**Q: Where are files stored?**
A: Nowhere! Files are generated in memory and sent directly to your browser, then memory is cleared.

**Q: Can multiple people use it at once?**
A: Yes! Each request is independent.

**Q: What if I forget the URL?**
A: Bookmark it, or check your GitHub repository description.

**Q: How do I add authentication?**
A: Currently anyone with the URL can use it. For authentication, we can add user login (future enhancement).

**Q: Can I use it on mobile?**
A: Yes! The interface is mobile-responsive.

---

## Support

For issues:
1. Check logs in deployment platform
2. Verify email IMAP settings
3. Test with different date
4. Check internet connection

---

**You're all set! 🎊**

Next: Push to GitHub → Deploy to Render → Share URL → Done!
