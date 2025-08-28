# Docker Authentication Testing Guide

## 🐳 Quick Start

### 1. Start Docker Containers
```bash
# Start all services
docker-compose up -d

# Or for development
docker-compose -f docker-compose.dev.yml up -d
```

### 2. Test Authentication
```bash
# Run the Docker authentication test
python test_docker_auth.py
```

### 3. Test Frontend
Open your browser and go to:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## 🔧 Configuration

### Environment Variables
The backend now has `DEVELOPMENT_MODE=true` set in the Docker configuration, which:
- Sets `cookie_secure=false` for HTTP development
- Allows cookies to work over HTTP connections
- Maintains security in production

### Cookie Settings
- **Development**: `Secure=false` (works with HTTP)
- **Production**: `Secure=true` (requires HTTPS)
- **HttpOnly**: Always `true` (prevents XSS)
- **SameSite**: `lax` (CSRF protection)

## 🧪 Testing Steps

### 1. Backend Health Check
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### 2. Authentication Flow
```bash
# Test the complete authentication flow
python test_docker_auth.py
```

### 3. Manual Testing
```bash
# Register a user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"Test","last_name":"User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -c cookies.txt

# Test protected endpoint
curl -X GET http://localhost:8000/api/v1/auth/me \
  -b cookies.txt

# Refresh token
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -b cookies.txt

# Logout
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -b cookies.txt
```

## 🔍 Troubleshooting

### Cookies Not Working
1. **Check DEVELOPMENT_MODE**: Ensure `DEVELOPMENT_MODE=true` is set
2. **Check Cookie Security**: Cookies should be `Secure=false` in development
3. **Check CORS**: Frontend origin should be in allowed origins
4. **Check Network**: Ensure containers can communicate

### Frontend Not Authenticating
1. **Check API URL**: Ensure frontend is pointing to correct backend URL
2. **Check Credentials**: Ensure `withCredentials: true` is set in API calls
3. **Check Browser**: Check browser dev tools for cookie errors
4. **Check CORS**: Ensure CORS is properly configured

### Common Issues

#### Issue: Cookies are Secure but using HTTP
**Solution**: Set `DEVELOPMENT_MODE=true` in Docker environment
```yaml
environment:
  - DEVELOPMENT_MODE=true
```

#### Issue: CORS errors
**Solution**: Ensure frontend origin is in CORS allow_origins
```python
allow_origins=[
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    "http://frontend:3000"
]
```

#### Issue: Authentication fails after login
**Solution**: Check that cookies are being sent with requests
```javascript
// Frontend API configuration
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true  // Important!
});
```

## 📋 Expected Behavior

### ✅ Working Authentication
- Login returns tokens and user data
- Cookies are set with `Secure=false` in development
- Protected endpoints accessible with cookies
- Token refresh works automatically
- Logout clears cookies
- User stays logged in across page refreshes

### ❌ Common Failures
- Cookies set as `Secure=true` with HTTP (won't work)
- CORS errors preventing cookie transmission
- Missing `withCredentials: true` in frontend
- Backend not running or not accessible

## 🚀 Production Deployment

For production, remove `DEVELOPMENT_MODE=true` and ensure:
- HTTPS is configured
- Cookies will be `Secure=true`
- Proper domain configuration
- CORS settings for production domains

## 🔐 Security Notes

- **HttpOnly cookies**: Tokens are not accessible to JavaScript (XSS protection)
- **SameSite cookies**: Protects against CSRF attacks
- **Secure cookies**: In production, cookies only sent over HTTPS
- **Automatic refresh**: Tokens refreshed every 10 minutes
- **Session management**: Short-lived access tokens (15 min) with longer refresh tokens (7 days)
