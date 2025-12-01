# Git Deployment Guide

## Quick Setup - Push to GitHub and Deploy

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `rental-billing-extractor`
3. Description: `Web-based rental billing email data extractor`
4. Choose **Public** (for free deployment) or **Private**
5. Do NOT initialize with README (we have files already)
6. Click **Create repository**

### Step 2: Initialize Git and Push

Open PowerShell in the `webapp` folder:

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Rental Billing Email Extractor"

# Add your GitHub repository as remote
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/rental-billing-extractor.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render (Free & Easy)

**Why Render?**
- Free tier available
- Easy deployment from GitHub
- No credit card required
- Automatic HTTPS
- Better than Heroku free tier

**Steps:**

1. Go to https://render.com and sign up with GitHub

2. Click **New +** → **Web Service**

3. Connect your GitHub repository `rental-billing-extractor`

4. Configure:
   - **Name**: `rental-billing-extractor`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

5. Add environment variable:
   - Key: `SECRET_KEY`
   - Value: `your-random-secret-key-here`

6. Click **Create Web Service**

7. Wait 2-3 minutes for deployment

8. Your app will be live at: `https://rental-billing-extractor.onrender.com`

### Step 4: Update requirements.txt for Deployment

Add gunicorn to requirements.txt:

```bash
cd webapp
echo "gunicorn==21.2.0" >> requirements.txt
git add requirements.txt
git commit -m "Add gunicorn for deployment"
git push
```

Render will automatically redeploy!

---

## Alternative: Deploy to Heroku

### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

### Steps:

```powershell
# Login to Heroku
heroku login

# Create Heroku app
heroku create rental-billing-extractor

# Add gunicorn to requirements.txt (if not already)
echo "gunicorn==21.2.0" >> requirements.txt

# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Commit changes
git add .
git commit -m "Prepare for Heroku deployment"

# Push to Heroku
git push heroku main

# Open your app
heroku open
```

Your app will be at: `https://rental-billing-extractor.herokuapp.com`

---

## Alternative: Deploy to Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your repository
5. Railway auto-detects Python and deploys
6. Your app will be live at: `https://your-app.railway.app`

---

## Sharing Your App

Once deployed, share the URL with users:
- **Render**: `https://rental-billing-extractor.onrender.com`
- **Heroku**: `https://rental-billing-extractor.herokuapp.com`
- **Railway**: `https://rental-billing-extractor.railway.app`

Users can:
1. Visit the URL
2. Enter their email credentials
3. Select date
4. Click "Extract & Download Excel"
5. File downloads directly to their device (NOT stored on server)

---

## Important Notes

### Security
- **Credentials are NEVER stored** - used only during the request, then discarded
- **Files are NOT stored on server** - generated in memory and sent directly to user
- **Use HTTPS** - All deployment platforms provide free SSL
- **Set SECRET_KEY** as environment variable (don't hardcode)

### Storage
- ✅ **No storage needed** - Files are generated in memory
- ✅ **No database needed** - Stateless application
- ✅ **No cleanup jobs needed** - Memory auto-clears after request
- ✅ **Scales well** - No disk space concerns

### Free Tier Limits
- **Render**: 750 hours/month, sleeps after 15 min inactivity
- **Heroku**: 1000 dyno hours/month, sleeps after 30 min inactivity
- **Railway**: $5 credit/month

**Tip**: For free tiers, first request may take 30-60 seconds (cold start) as app wakes up

---

## GitHub Repository Structure

```
rental-billing-extractor/
├── .gitignore              # Prevents committing sensitive files
├── app.py                  # Main Flask application
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── Procfile               # For Heroku deployment
├── README.md              # Documentation
├── DEPLOYMENT.md          # Deployment guide
├── GIT_DEPLOYMENT.md      # This file
└── templates/
    └── index.html         # Web interface
```

### Files NOT in Git (see .gitignore):
- `.env` - Local environment variables
- `__pycache__/` - Python cache
- `*.xlsx` - Excel files (not generated anyway!)
- `*.pdf` - PDF files
- Sensitive credentials

---

## Update Your App After Changes

```powershell
# Make your changes to code

# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push

# If using Render/Railway - automatically redeploys!
# If using Heroku:
git push heroku main
```

---

## Monitoring

### Check Logs

**Render**:
- Go to Dashboard → Your Service → Logs

**Heroku**:
```bash
heroku logs --tail
```

**Railway**:
- Go to Project → Deployments → View Logs

---

## Cost

All options have **FREE tiers** sufficient for internal use:

| Platform | Free Tier | Pros | Cons |
|----------|-----------|------|------|
| **Render** | 750 hrs/month | Easy setup, auto-deploy | Sleeps after 15 min |
| **Heroku** | 1000 hrs/month | Most popular | Sleeps after 30 min |
| **Railway** | $5 credit/month | Fast deployment | Credit limit |

**Recommendation**: Start with **Render** - it's the easiest and most reliable free option.

---

## Troubleshooting

### App not starting
- Check logs for errors
- Verify all dependencies in requirements.txt
- Ensure gunicorn is installed
- Check environment variables

### Cannot connect to email
- Ensure IMAP ports (993) are not blocked
- Verify email credentials work
- Check IMAP is enabled for email account

### Deployment fails
- Check Python version compatibility
- Verify requirements.txt is complete
- Check for syntax errors in app.py

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Deploy to Render (or Heroku/Railway)
3. ✅ Share URL with team
4. ✅ Test with actual email credentials
5. ✅ Monitor logs for any issues

**Your app is now accessible from anywhere, stores nothing, and costs nothing!** 🎉
