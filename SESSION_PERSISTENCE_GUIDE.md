# Session Persistence Testing Guide

## 🎯 The Problem
When you refresh the frontend page, it redirects to the login page instead of staying logged in. This should NOT happen - the session should persist across page refreshes.

## 🔧 How to Test

### 1. Start Docker Containers
```bash
# Make sure containers are running with DEVELOPMENT_MODE=true
docker-compose down
docker-compose up -d
```

### 2. Test with HTML Test Page
1. Open `test_frontend_auth.html` in your browser
2. Register a user
3. Login
4. **Refresh the page**
5. Click "Test Session Persistence" - should work without re-login

### 3. Test with Frontend App
1. Go to http://localhost:3000
2. Login
3. **Refresh the page** - should stay logged in
4. Navigate to different pages - should work

## 🔍 Troubleshooting Steps

### Step 1: Check Backend Cookies
```bash
# Test if cookies are being set properly
python test_docker_auth.py
```

**Expected Output:**
- Cookies should be `Secure: False` (not True)
- `session_token` and `refresh_token` cookies should exist
- Authentication should work with cookies

### Step 2: Check Frontend Console
1. Open browser dev tools (F12)
2. Go to Console tab
3. Login and refresh page
4. Look for authentication logs:
   - "Checking authentication..."
   - "Auth check successful" or "Auth check failed, trying refresh..."
   - "Token refresh successful" or "Token refresh also failed"

### Step 3: Check Network Tab
1. Open browser dev tools (F12)
2. Go to Network tab
3. Login and refresh page
4. Look for:
   - `/auth/me` request (should succeed)
   - `/auth/refresh` request (if needed)
   - Cookies being sent with requests

### Step 4: Check Cookie Storage
1. Open browser dev tools (F12)
2. Go to Application/Storage tab
3. Look for Cookies under localhost:8000
4. Should see:
   - `session_token` (HttpOnly)
   - `refresh_token` (HttpOnly)

## 🚨 Common Issues

### Issue 1: Cookies are Secure=True
**Symptoms:** Authentication fails after page refresh
**Solution:** Ensure `DEVELOPMENT_MODE=true` is set in Docker environment

### Issue 2: CORS Errors
**Symptoms:** Network errors in browser console
**Solution:** Check CORS configuration in backend

### Issue 3: Frontend not sending cookies
**Symptoms:** 401 errors on protected endpoints
**Solution:** Ensure `withCredentials: true` is set in API calls

### Issue 4: Backend not accessible
**Symptoms:** Connection refused errors
**Solution:** Check if Docker containers are running

## 🔧 Debug Commands

### Check Docker Environment
```bash
# Check if DEVELOPMENT_MODE is set
docker-compose exec backend env | grep DEVELOPMENT_MODE
# Should show: DEVELOPMENT_MODE=true
```

### Check Backend Logs
```bash
# Check backend logs for authentication messages
docker-compose logs backend | grep -i auth
```

### Test API Directly
```bash
# Test authentication flow
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -c cookies.txt

curl -X GET http://localhost:8000/api/v1/auth/me \
  -b cookies.txt
```

## 📋 Expected Behavior

### ✅ Working Session Persistence
1. User logs in → cookies are set
2. User refreshes page → authentication check runs
3. `/auth/me` succeeds → user stays logged in
4. If `/auth/me` fails → automatic refresh attempt
5. If refresh succeeds → user stays logged in
6. If refresh fails → redirect to login

### ❌ Broken Session Persistence
1. User logs in → cookies are set
2. User refreshes page → authentication check runs
3. `/auth/me` fails → refresh attempt fails
4. User redirected to login → session lost

## 🔍 Debug Checklist

- [ ] Docker containers running with `DEVELOPMENT_MODE=true`
- [ ] Cookies are `Secure: False` (not True)
- [ ] `session_token` and `refresh_token` cookies exist
- [ ] Frontend API calls include `withCredentials: true`
- [ ] CORS allows frontend origin
- [ ] Backend `/auth/me` endpoint works
- [ ] Backend `/auth/refresh` endpoint works
- [ ] Frontend authentication check runs on page load
- [ ] No JavaScript errors in browser console
- [ ] Network requests include cookies

## 🎯 Quick Fix Test

If session persistence is still not working:

1. **Clear browser cookies** for localhost:8000
2. **Restart Docker containers**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```
3. **Test with HTML page** first: `test_frontend_auth.html`
4. **Check browser console** for authentication logs
5. **Verify cookies** are being set and sent

## 🔐 Security Notes

- **HttpOnly cookies**: Tokens are not accessible to JavaScript
- **Automatic refresh**: Happens every 10 minutes
- **Session tokens**: 15-minute expiration
- **Refresh tokens**: 7-day expiration
- **Secure cookies**: Only in production (HTTPS)

The session should persist across page refreshes as long as the refresh token is valid (7 days).
