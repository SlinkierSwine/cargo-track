# Auth Service - Business Logic Planning

## 1. Authentication and Authorization Requirements

### Authentication
- JWT-based authentication with access tokens
- Token expiration: 30 minutes (configurable)
- Refresh token mechanism for extended sessions
- Password hashing using bcrypt
- Rate limiting for login attempts (5 attempts per 15 minutes)

### Authorization
- Role-based access control (RBAC)
- Permission-based authorization for specific actions
- Token validation on each protected request
- Automatic token refresh when needed

## 2. User Roles and Permissions

### Admin Role
- **Permissions:**
  - Full access to all system features
  - User management (create, read, update, delete)
  - Role assignment and management
  - System configuration
  - View all orders and reports
- **Access Level:** System-wide

### Dispatcher Role
- **Permissions:**
  - View and manage orders
  - Assign drivers to orders
  - View vehicle and driver information
  - Create and manage routes
  - View warehouse information
- **Access Level:** Order management and dispatch operations

### Driver Role
- **Permissions:**
  - View assigned orders
  - Update order status (in progress, delivered, etc.)
  - View route information
  - Update location and status
  - View vehicle information
- **Access Level:** Assigned orders and personal information

### Client Role
- **Permissions:**
  - Create and view own orders
  - Track order status
  - View order history
  - Update personal information
  - View invoices and payments
- **Access Level:** Own orders and personal information

## 3. API Endpoints Design

### Authentication Endpoints
```
POST /auth/register
- Register new user
- Request: email, username, password, role (optional, defaults to CLIENT)
- Response: user info + access token

POST /auth/login
- User login
- Request: email/username, password
- Response: access token + refresh token

POST /auth/refresh
- Refresh access token
- Request: refresh token
- Response: new access token

POST /auth/logout
- User logout
- Request: access token
- Response: success message

POST /auth/forgot-password
- Request password reset
- Request: email
- Response: success message (email sent)

POST /auth/reset-password
- Reset password with token
- Request: reset token, new password
- Response: success message
```

### User Management Endpoints
```
GET /auth/me
- Get current user info
- Request: access token
- Response: user details

PUT /auth/me
- Update current user info
- Request: access token, updated fields
- Response: updated user info

PUT /auth/me/password
- Change password
- Request: access token, current password, new password
- Response: success message

GET /auth/users
- List users (admin only)
- Request: access token, pagination params
- Response: list of users

GET /auth/users/{user_id}
- Get user by ID (admin only)
- Request: access token, user_id
- Response: user details

POST /auth/users
- Create new user (admin only)
- Request: access token, user data
- Response: created user

PUT /auth/users/{user_id}
- Update user (admin only)
- Request: access token, user_id, updated fields
- Response: updated user

DELETE /auth/users/{user_id}
- Delete user (admin only)
- Request: access token, user_id
- Response: success message

PUT /auth/users/{user_id}/role
- Change user role (admin only)
- Request: access token, user_id, new role
- Response: updated user
```

### Health and Status Endpoints
```
GET /auth/health
- Service health check
- Response: service status

GET /auth/status
- Authentication service status
- Response: detailed service info
```

## 4. Data Models

### User Model
```python
class User:
    id: UUID
    email: EmailStr
    username: str
    hashed_password: str
    role: UserRole
    is_active: bool
    is_verified: bool
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
```

### Token Models
```python
class AccessToken:
    token: str
    user_id: UUID
    expires_at: datetime
    created_at: datetime

class RefreshToken:
    token: str
    user_id: UUID
    expires_at: datetime
    created_at: datetime
    is_revoked: bool
```

## 5. Security Considerations

### Password Security
- Minimum 8 characters
- Must contain at least one uppercase, one lowercase, one digit
- Password history (prevent reuse of last 3 passwords)
- Account lockout after 5 failed attempts

### Token Security
- Secure token storage (httpOnly cookies for refresh tokens)
- Token rotation on refresh
- Automatic token revocation on logout
- Token blacklisting for security incidents

### API Security
- Rate limiting on authentication endpoints
- Input validation and sanitization
- CORS configuration
- Request logging for security monitoring

## 6. Integration Points

### Event Publishing
- User created event
- User updated event
- User deleted event
- User role changed event
- Login event (for audit)

### External Service Dependencies
- Email service for password reset and verification
- Notification service for security alerts
- Audit service for compliance logging

## 7. Error Handling

### Authentication Errors
- Invalid credentials
- Account locked
- Token expired
- Token invalid
- Insufficient permissions

### Validation Errors
- Invalid email format
- Username already exists
- Password too weak
- Invalid role assignment

### System Errors
- Database connection issues
- Email service unavailable
- Token generation failures 