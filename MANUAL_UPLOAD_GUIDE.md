# Manual GitHub Upload Guide (No Git Required)

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `rental-billing-extractor`
3. Description: `Web-based rental billing email data extractor`
4. Choose **Public** (for free deployment)
5. **Do NOT check** "Add a README file"
6. Click **Create repository**

## Step 2: Upload Files via Web Interface

1. On the new repository page, click **"uploading an existing file"** link

2. Drag and drop these files from `webapp` folder:
   - app.py
   - requirements.txt
   - Procfile
   - config.py
   - .gitignore
   - All .md files (README.md, DEPLOYMENT.md, etc.)

3. Create `templates` folder:
   - Click "Create new file"
   - Type: `templates/index.html`
   - Copy content from your local `templates/index.html`
   - Click "Commit new file"

4. Add commit message: "Initial commit: Rental Billing Email Extractor"

5. Click **Commit changes**

## Step 3: Deploy to Render

1. Go to https://render.com
2. Sign up with GitHub
3. Click **New +** → **Web Service**
4. Select your repository: `rental-billing-extractor`
5. Settings:
   - **Name**: `rental-billing-extractor`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
6. Click **Create Web Service**

## Done!

Your app will be live at: `https://rental-billing-extractor.onrender.com`

---

## Alternative: Use GitHub Desktop (Easier than command line)

1. Download GitHub Desktop: https://desktop.github.com
2. Install and sign in with GitHub account
3. File → Add Local Repository → Select your `webapp` folder
4. Click "Publish repository"
5. Push to GitHub with one click!

Then follow Step 3 above to deploy to Render.
