# Frontend Authentication Debug Steps

## 🎯 The Issue
The backend authentication is working perfectly, but the frontend is not maintaining the session after page refresh.

## 🔍 Step-by-Step Debug Process

### Step 1: Open Browser and Dev Tools
1. Open your browser and go to `http://localhost:3000`
2. Press `F12` to open developer tools
3. Go to the **Console** tab
4. Go to the **Network** tab

### Step 2: Clear Browser Data
1. In dev tools, go to **Application** tab
2. Click on **Storage** → **Clear site data**
3. This will clear any old cookies or cached data

### Step 3: Test Login
1. Go to the login page
2. Enter credentials (e.g., `frontend@example.com` / `password123`)
3. Click login
4. **Watch the Console** for these logs:
   ```
   🔍 Attempting login...
   ✅ Login successful: {user data}
   ```

### Step 4: Test Page Refresh
1. After successful login, you should be on the dashboard
2. **Press F5 or Ctrl+R to refresh the page**
3. **Watch the Console** for these logs:
   ```
   🔍 Layout mounted - starting authentication check...
   🔍 Calling checkAuth()...
   🔍 Checking authentication...
   🔍 API URL: http://localhost:8000/api/v1
   🔍 With credentials: true
   🔍 Trying /auth/me...
   ✅ Auth check successful: {user data}
   🔍 checkAuth() result: true
   🔍 User is authenticated, staying on current page
   ```

### Step 5: Check Network Requests
1. In the **Network** tab, look for:
   - `POST /api/v1/auth/login` (should be 200)
   - `GET /api/v1/auth/me` (should be 200 after refresh)
   - Check if cookies are being sent with requests

### Step 6: Check Cookies
1. In dev tools, go to **Application** tab
2. Click on **Cookies** → `http://localhost:8000`
3. You should see:
   - `session_token` (HttpOnly)
   - `refresh_token` (HttpOnly)

## 🚨 What to Look For

### ✅ Good Signs
- Console shows authentication logs
- Network requests succeed (200 status)
- Cookies are present
- No JavaScript errors

### ❌ Bad Signs
- Console shows no authentication logs
- Network requests fail (401, 404, etc.)
- No cookies present
- JavaScript errors in console

## 🔧 Common Issues and Solutions

### Issue 1: No Authentication Logs
**Problem**: Console shows no authentication logs
**Solution**: Check if the frontend code changes are loaded

### Issue 2: Network Errors
**Problem**: API requests failing
**Solution**: Check CORS configuration and API URL

### Issue 3: No Cookies
**Problem**: Cookies not being set
**Solution**: Check if `withCredentials: true` is set

### Issue 4: JavaScript Errors
**Problem**: Errors in console
**Solution**: Check for missing dependencies or syntax errors

## 🎯 Quick Test

If you want to test quickly:

1. **Open the HTML test page**: `test_frontend_auth.html`
2. **Login** with any credentials
3. **Refresh the page**
4. **Click "Test Session Persistence"**
5. Should work without re-login

## 📋 Debug Checklist

- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend accessible at http://localhost:8000
- [ ] Console shows authentication logs
- [ ] Network requests succeed
- [ ] Cookies are present
- [ ] No JavaScript errors
- [ ] Page refresh maintains session

## 🔍 If Still Not Working

1. **Check Docker logs**:
   ```bash
   docker-compose logs frontend
   docker-compose logs backend
   ```

2. **Restart containers**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. **Test with curl**:
   ```bash
   python test_frontend_debug.py
   ```

4. **Check browser console** for specific error messages

## 🎯 Expected Behavior

After implementing the fixes:
- ✅ Login works
- ✅ Page refresh maintains session
- ✅ Console shows authentication logs
- ✅ Network requests include cookies
- ✅ User stays logged in across page refreshes

The session should persist for 7 days (refresh token lifetime) with automatic token refresh every 10 minutes.
