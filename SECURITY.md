# 🔒 Security Guide for ALX Travel App

## ✅ Security Checklist Before Deployment

### Environment Variables Protection
- [x] `.env` file created with sensitive data
- [x] `.env` added to `.gitignore`
- [x] `.env.example` template created for other developers
- [x] `python-decouple` installed for secure environment variable handling
- [x] `SECRET_KEY` moved to environment variables
- [x] `DEBUG` setting moved to environment variables
- [x] `ALLOWED_HOSTS` configured through environment variables

### Files Protected from Git
- [x] `.env` files (never commit these!)
- [x] Database files (`*.sqlite3`)
- [x] Python cache files (`__pycache__/`)
- [x] Virtual environment folders (`venv/`, `.venv/`)
- [x] IDE configuration files
- [x] Log files
- [x] Backup files

### Production Security Settings (TODO for later)
- [ ] Set `DEBUG=False` in production
- [ ] Use strong, unique `SECRET_KEY` in production
- [ ] Configure proper `ALLOWED_HOSTS` for your domain
- [ ] Use HTTPS in production
- [ ] Set up proper database authentication
- [ ] Configure email settings securely
- [ ] Add rate limiting
- [ ] Set up monitoring and logging

## 🔑 Environment Variables Reference

### Required Variables
```bash
SECRET_KEY=your-secret-key-here    # Django secret key
DEBUG=True                         # Development mode
ALLOWED_HOSTS=127.0.0.1,localhost # Allowed hosts
```

### Optional Variables (for future features)
```bash
# Database (when switching from SQLite)
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🚀 Setup for New Developers

1. **Clone the repository**
   ```bash
   git clone https://github.com/s-shemmee/alx_travel_app_0x00.git
   cd alx_travel_app_0x00
   ```

2. **Copy environment template**
   ```bash
   cp .env.example .env
   ```

3. **Update .env with your values**
   - Generate a new SECRET_KEY
   - Set DEBUG=True for development
   - Configure other settings as needed

4. **Install dependencies and run**
   ```bash
   pip install -r requirements.txt
   cd alx_travel_app
   python manage.py migrate
   python manage.py seed
   python manage.py runserver
   ```

## 🛡️ Security Best Practices

### For Development
- Never commit `.env` files
- Use different SECRET_KEY for each environment
- Keep DEBUG=True only in development
- Use strong passwords for database users

### For Production
- Use environment variables or secure secret management
- Set DEBUG=False
- Use HTTPS only
- Configure proper CORS settings
- Set up proper logging and monitoring
- Use strong database passwords
- Regular security updates

## 🔧 Quick Security Check

Run this command to verify your security setup:
```bash
python ../test_backend.py
```

If all tests pass, your basic security is configured correctly!

## 📞 Emergency Security Response

If you accidentally commit sensitive data:
1. Immediately change all passwords/keys
2. Remove sensitive data from git history
3. Force push the cleaned repository
4. Notify team members if applicable

---
**Remember: Security is not a one-time setup, it's an ongoing process!**
