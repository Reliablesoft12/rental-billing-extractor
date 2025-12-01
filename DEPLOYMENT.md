# Deployment Guide

## Quick Start (Local Development)

1. Install Python 3.8 or higher
2. Navigate to webapp directory:
   ```bash
   cd webapp
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open browser: http://localhost:5000

## Deployment Options

### Option 1: Heroku Deployment

1. Create a Heroku account and install Heroku CLI

2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

3. Add gunicorn to requirements.txt:
   ```bash
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

4. Deploy:
   ```bash
   heroku login
   heroku create rental-billing-extractor
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

### Option 2: AWS EC2 Deployment

1. Launch an EC2 instance (Ubuntu 20.04 or later)

2. SSH into your instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx -y
   ```

4. Clone/upload your code and setup:
   ```bash
   cd /home/ubuntu
   mkdir rental-billing && cd rental-billing
   # Upload your files here
   
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

5. Create systemd service `/etc/systemd/system/rental-billing.service`:
   ```ini
   [Unit]
   Description=Rental Billing Extractor
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/rental-billing/webapp
   Environment="PATH=/home/ubuntu/rental-billing/venv/bin"
   ExecStart=/home/ubuntu/rental-billing/venv/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

6. Configure Nginx `/etc/nginx/sites-available/rental-billing`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

7. Enable and start:
   ```bash
   sudo ln -s /etc/nginx/sites-available/rental-billing /etc/nginx/sites-enabled/
   sudo systemctl start rental-billing
   sudo systemctl enable rental-billing
   sudo systemctl restart nginx
   ```

### Option 3: Azure App Service

1. Install Azure CLI and login:
   ```bash
   az login
   ```

2. Create resource group and app:
   ```bash
   az group create --name rental-billing-rg --location eastus
   az webapp up --name rental-billing-extractor --runtime "PYTHON:3.9" --sku B1
   ```

3. Configure app settings:
   ```bash
   az webapp config appsettings set --name rental-billing-extractor \
       --resource-group rental-billing-rg \
       --settings SECRET_KEY="your-secret-key-here"
   ```

### Option 4: Docker Deployment

1. Create `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 5000

   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

2. Create `docker-compose.yml`:
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - SECRET_KEY=your-secret-key
       restart: unless-stopped
   ```

3. Build and run:
   ```bash
   docker-compose up -d
   ```

## Environment Variables

Create a `.env` file (DO NOT commit to Git):
```
SECRET_KEY=your-very-secure-secret-key
FLASK_ENV=production
```

## Security Considerations

1. **Always use HTTPS in production** - Set up SSL certificates
2. **Use environment variables** for sensitive data
3. **Implement rate limiting** to prevent abuse
4. **Add authentication** for multi-user scenarios
5. **Validate and sanitize** all user inputs
6. **Set proper CORS policies** if needed

## Production Checklist

- [ ] Set DEBUG=False in production
- [ ] Use a production WSGI server (gunicorn, uWSGI)
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Implement backup strategy
- [ ] Use environment variables for secrets
- [ ] Set up automatic restarts
- [ ] Configure proper file permissions
- [ ] Test the deployment thoroughly

## Monitoring

### Application Logs
```bash
# For systemd service
sudo journalctl -u rental-billing -f

# For Docker
docker-compose logs -f
```

### Performance Monitoring
Consider integrating:
- New Relic
- DataDog
- Application Insights (Azure)
- CloudWatch (AWS)

## Scaling

For high traffic:
1. Use a load balancer (AWS ELB, Azure Load Balancer)
2. Scale horizontally with multiple instances
3. Use a CDN for static assets
4. Implement caching (Redis)
5. Use a message queue for background processing

## Maintenance

### Backup
```bash
# Backup configuration and data
tar -czf backup-$(date +%Y%m%d).tar.gz webapp/
```

### Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Restart service
sudo systemctl restart rental-billing
```

## Troubleshooting

### Application won't start
- Check logs: `sudo journalctl -u rental-billing -n 50`
- Verify Python version and dependencies
- Check file permissions

### Cannot connect to email
- Verify IMAP ports are open (993 for SSL)
- Check firewall rules
- Test IMAP connection manually

### High memory usage
- Reduce worker processes
- Implement streaming for large files
- Add memory limits

## Support

For deployment issues, refer to:
- Flask documentation: https://flask.palletsprojects.com/
- Gunicorn documentation: https://docs.gunicorn.org/
- Cloud provider documentation
