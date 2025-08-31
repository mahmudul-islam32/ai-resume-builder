# Secure Cookie-Based Authentication System

This project now implements a secure cookie-based authentication system that protects against XSS and CSRF attacks with persistent authentication across page refreshes.

## Security Features

### 🔒 Secure Cookies
- **HttpOnly**: Cookies cannot be accessed by JavaScript (prevents XSS attacks)
- **Secure**: Cookies only sent over HTTPS (except in development mode)
- **SameSite**: Protects against CSRF attacks
- **Domain**: Configurable domain restriction

### 🔄 Token Management
- **Session Token**: 15-minute expiration (short-lived for security)
- **Refresh Token**: 7-day expiration (longer-lived for convenience)
- **Automatic Refresh**: Frontend automatically refreshes tokens every 10 minutes
- **Secure Storage**: Tokens stored in HttpOnly cookies, not accessible to JavaScript
- **Persistent Authentication**: Users stay logged in across page refreshes and browser sessions

## How Persistent Authentication Works

### 🔐 Authentication Flow
1. **Login**: User logs in and receives session + refresh tokens in secure cookies
2. **Page Refresh**: Frontend checks authentication status on load
3. **Token Validation**: If session token is valid, user stays logged in
4. **Automatic Refresh**: If session token expires, refresh token is used automatically
5. **Seamless Experience**: User never sees login page unless refresh token expires (7 days)

### 🔄 Automatic Token Refresh
- **Every 10 minutes**: Frontend automatically refreshes tokens
- **On 401 errors**: API calls automatically trigger token refresh
- **Queue system**: Multiple failed requests are queued and retried after refresh
- **Infinite loop prevention**: Prevents multiple simultaneous refresh attempts

## Backend Implementation

### Configuration (`backend/app/core/config.py`)
```python
# Cookie Settings
cookie_domain: Optional[str] = None
cookie_secure: bool = True  # Set to False for HTTP in development
cookie_httponly: bool = True
cookie_samesite: str = "lax"

# Token Expiration
access_token_expire_minutes: int = 15  # 15 minutes
refresh_token_expire_days: int = 7     # 1 week
```

### Authentication Endpoints (`backend/app/api/v1/endpoints/auth.py`)

#### Login (`POST /api/v1/auth/login`)
- Creates session and refresh tokens
- Sets secure HttpOnly cookies
- Returns tokens and user data in response body

**Response Format:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

#### Refresh (`POST /api/v1/auth/refresh`)
- Validates refresh token from cookie
- Creates new session and refresh tokens
- Updates cookies automatically
- Returns new tokens and user data

#### Logout (`POST /api/v1/auth/logout`)
- Clears all authentication cookies
- Invalidates session

#### Get Current User (`GET /api/v1/auth/me`)
- Validates session token from cookie
- Returns current user data

### Token Types
- **Access Token**: Used for API authentication (15 min)
- **Refresh Token**: Used to get new access tokens (7 days)
- **Session ID**: Unique identifier for each session

## Frontend Implementation

### API Service (`frontend/src/lib/utils/api.ts`)
```typescript
const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  withCredentials: true, // Important for cookies
});
```

### Automatic Token Refresh
- Refreshes tokens every 10 minutes
- Handles 401 errors automatically with queue system
- Redirects to login on refresh failure
- Prevents infinite loops

### Authentication Store (`frontend/src/lib/stores/auth.ts`)
- Manages user state
- Handles automatic token refresh
- Provides logout functionality
- Checks authentication on page load

### Layout Authentication Check (`frontend/src/routes/+layout.svelte`)
- Checks authentication status on page load
- Shows loading screen during auth check
- Redirects to login only if not authenticated
- Prevents unnecessary redirects during initial check

## Development Setup

### Environment Variables
```bash
# For development (HTTP)
DEVELOPMENT_MODE=true

# For production (HTTPS)
DEVELOPMENT_MODE=false
```

### Cookie Settings
- **Development**: `secure=false` (allows HTTP)
- **Production**: `secure=true` (requires HTTPS)

## Testing

### Quick Test
Run the simple authentication test:
```bash
python test_auth_simple.py
```

### Persistent Authentication Test
Test persistent authentication across requests:
```bash
python test_persistent_auth.py
```

### Comprehensive Test
Run the full API test suite:
```bash
python test_api_no_auth.py
```

### ATS Scoring Test
Test the ATS scoring functionality:
```bash
python test_ats_request.py
```

## Security Benefits

### 🛡️ XSS Protection
- Tokens stored in HttpOnly cookies
- JavaScript cannot access authentication tokens
- Prevents token theft via malicious scripts

### 🛡️ CSRF Protection
- SameSite cookie attribute
- Tokens automatically included in requests
- No manual token handling required

### 🛡️ Token Security
- Short-lived access tokens (15 min)
- Automatic refresh mechanism
- Secure token generation with session IDs

### 🛡️ Persistent Security
- Tokens automatically refreshed
- No manual intervention required
- Secure across browser sessions

## Usage Examples

### Login Flow
1. User submits login form
2. Backend validates credentials
3. Backend sets secure cookies
4. Backend returns tokens and user data
5. Frontend stores user data
6. Automatic token refresh starts
7. User stays logged in across page refreshes

### Page Refresh Behavior
1. User refreshes page
2. Frontend checks authentication status
3. If session token valid: user stays logged in
4. If session token expired: automatic refresh
5. If refresh token expired: redirect to login

### API Requests
```typescript
// Cookies are automatically included
const response = await api.get('/resumes/');
```

### Token Refresh
```typescript
// Automatic refresh every 10 minutes
// Manual refresh on 401 errors
const response = await api.post('/auth/refresh');
const { access_token, refresh_token, user } = response.data;
```

### Logout
```typescript
// Clears cookies and user state
await logout();
```

## Manual Testing

### Browser Testing
1. Start the backend server with `DEVELOPMENT_MODE=true`
2. Open browser developer tools
3. Go to Application/Storage tab
4. Check Cookies section
5. Verify HttpOnly and Secure attributes
6. Test page refresh - user should stay logged in

### API Testing with curl
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -c cookies.txt

# Access protected endpoint
curl -X GET http://localhost:8000/api/v1/users/profile \
  -b cookies.txt

# Refresh token
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -b cookies.txt

# Logout
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -b cookies.txt
```

## Production Deployment

### HTTPS Required
- Set `DEVELOPMENT_MODE=false`
- Ensure HTTPS is configured
- Cookies will be Secure by default

### Domain Configuration
- Set `cookie_domain` for cross-subdomain support
- Configure proper CORS settings
- Use proper SameSite settings

## Migration from localStorage

### Old System (Insecure)
```typescript
// Tokens stored in localStorage (vulnerable to XSS)
localStorage.setItem('token', accessToken);
```

### New System (Secure)
```typescript
// Tokens stored in HttpOnly cookies (XSS-safe)
// No manual token handling required
const response = await api.get('/protected-endpoint');
```

## Troubleshooting

### Common Issues

1. **Cookies not being sent**
   - Ensure `withCredentials: true` is set
   - Check CORS configuration
   - Verify cookie domain settings

2. **401 errors in development**
   - Set `DEVELOPMENT_MODE=true`
   - Check cookie secure setting
   - Verify token expiration

3. **CORS errors**
   - Configure proper CORS settings
   - Include credentials in CORS configuration
   - Check domain settings

4. **Tokens not showing in response**
   - Check that login endpoint returns both cookies and response body
   - Verify Token schema includes all required fields
   - Ensure frontend handles the new response format

5. **User logged out on page refresh**
   - Check that cookies are being set properly
   - Verify token refresh is working
   - Check browser console for errors

### Debug Mode
```bash
# Enable development mode
export DEVELOPMENT_MODE=true
python -m uvicorn app.main:app --reload
```

### Testing Checklist
- [ ] Registration works
- [ ] Login returns tokens and user data
- [ ] Cookies are set with proper attributes
- [ ] Protected endpoints are accessible
- [ ] Token refresh works
- [ ] Logout clears cookies
- [ ] Access denied after logout
- [ ] User stays logged in on page refresh
- [ ] Automatic token refresh works
- [ ] Session persists across browser tabs

This authentication system provides enterprise-grade security while maintaining a smooth user experience with automatic token management and persistent authentication.
