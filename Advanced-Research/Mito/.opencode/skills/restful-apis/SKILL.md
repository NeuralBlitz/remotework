---
name: restful-apis
description: >
  Expert guidance on RESTful API architecture and implementation. Use for: designing RESTful 
  endpoints, HTTP verb usage, error handling, pagination, filtering, sorting, versioning, 
  HATEOAS implementation, OpenAPI documentation, authentication, rate limiting, and building 
  production-quality web services.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: api-design
  tags: [rest, api, http, restful]
---

# RESTful API Design — Implementation Guide

Covers: **Endpoint Design · HTTP Semantics · Error Handling · Versioning · Documentation · Authentication**

-----

## API Design Principles

### Core REST Constraints

REST (Representational State Transfer) is an architectural style built on six constraints. Understanding these constraints is essential for building truly RESTful APIs that are scalable, maintainable, and intuitive.

The six constraints are: Client-Server Architecture, which separates concerns between client and server, allowing them to evolve independently; Statelessness, where each request contains all information needed to process it, with no server-side session; Cacheability, enabling clients to cache responses for improved performance; Layered System, allowing intermediaries between client and server; Uniform Interface, providing standardized resource-based interactions; and Code on Demand (optional), where servers can extend client functionality.

**Key Principles:**

- Resources are the core abstraction — nouns, not verbs
- Each resource has a unique URI
- Use HTTP methods semantically
- Representations describe resource state
- Stateless communication between client and server

### Resource Naming

```yaml
# Good vs Bad Naming Examples

# Bad - Using verbs
GET   /getUsers           # Wrong
POST  /createUser         # Wrong
POST  /user/create        # Wrong
GET   /getUserById/123    # Wrong

# Good - Using nouns
GET    /users             # List users
POST   /users             # Create user
GET    /users/123         # Get user
PATCH  /users/123         # Update user
DELETE /users/123         # Delete user

# Nested resources
GET    /users/123/orders           # User's orders
POST   /users/123/orders           # Create order for user
GET    /users/123/orders/456       # Specific order
GET    /users/123/orders/456/items # Items in order

# Collections
GET    /products                   # All products
GET    /categories/electronics/products  # Products in category

# Singleton resources
GET    /settings                   # Get settings
PATCH  /settings                  # Update settings (not /setting)

# Actions as resources
POST   /users/123/activate        # Activate user
POST   /users/123/deactivate      # Deactivate user
POST   /orders/456/cancel         # Cancel order

# Compound documents (include related resources)
GET    /users/123?include=orders,profile
```

-----

## HTTP Methods and Status Codes

### Proper Method Usage

| Method | Safe | Idempotent | Use For |
|--------|------|------------|---------|
| **GET** | Yes | Yes | Retrieve resources |
| **POST** | No | No | Create resources, execute actions |
| **PUT** | No | Yes | Replace resources entirely |
| **PATCH** | No | Yes | Partial resource update |
| **DELETE** | No | Yes | Remove resources |
| **HEAD** | Yes | Yes | Get headers only |
| **OPTIONS** | Yes | Yes | Get supported methods |

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI()

# In-memory storage
users_db = {}

# Request/Response models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    age: Optional[int] = None
    created_at: datetime

# GET - Retrieve resources
@app.get("/users", response_model=List[User])
async def list_users(
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = None
):
    """List users with pagination and search"""
    users = list(users_db.values())
    
    if search:
        users = [u for u in users if search.lower() in u.name.lower()]
    
    return users[offset:offset + limit]

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get a specific user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users_db[user_id]

# POST - Create resources
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    # Check for duplicate email
    existing = [u for u in users_db.values() if u.email == user.email]
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Create user
    new_user = User(
        id=str(uuid.uuid4()),
        name=user.name,
        email=user.email,
        age=user.age,
        created_at=datetime.now()
    )
    users_db[new_user.id] = new_user
    return new_user

# PUT - Replace entire resource
@app.put("/users/{user_id}", response_model=User)
async def replace_user(user_id: str, user: UserCreate):
    """Replace a user (full update)"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    updated_user = User(
        id=user_id,
        name=user.name,
        email=user.email,
        age=user.age,
        created_at=users_db[user_id].created_at
    )
    users_db[user_id] = updated_user
    return updated_user

# PATCH - Partial update
@app.patch("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: UserUpdate):
    """Update user fields (partial update)"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    existing_user = users_db[user_id]
    
    # Update only provided fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_user, field, value)
    
    users_db[user_id] = existing_user
    return existing_user

# DELETE - Remove resources
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """Delete a user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    del users_db[user_id]
    return None

# HEAD - Check resource existence
@app.head("/users/{user_id}")
async def check_user_exists(user_id: str):
    """Check if user exists"""
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"Content-Type": "application/json"}

# OPTIONS - Get supported methods
@app.options("/users")
async def list_supported_methods():
    """List supported HTTP methods"""
    return {
        "GET": {"description": "List users"},
        "POST": {"description": "Create user"},
        "OPTIONS": {"description": "List supported methods"}
    }
```

### HTTP Status Codes

```python
# Success Codes
200 OK                    # GET, PATCH successful
201 Created              # POST created new resource
202 Accepted             # Async processing started
204 No Content           # DELETE successful, no body to return

# Redirection Codes
301 Moved Permanently     # Resource moved permanently
302 Found                 # Temporary redirect
304 Not Modified          # Cached response still valid

# Client Error Codes
400 Bad Request           # Invalid request format
401 Unauthorized          # Authentication required
403 Forbidden             # Authenticated but not authorized
404 Not Found             # Resource doesn't exist
405 Method Not Allowed    # HTTP method not supported
409 Conflict              # Business logic conflict (e.g., duplicate)
422 Unprocessable Entity # Valid format but semantic errors
429 Too Many Requests     # Rate limit exceeded

# Server Error Codes
500 Internal Server Error # Unexpected server error
502 Bad Gateway           # Upstream service error
503 Service Unavailable  # Temporary overload
504 Gateway Timeout       # Upstream timeout
```

-----

## Query Parameters

### Filtering, Sorting, Pagination

```python
from enum import Enum
from typing import List, Optional, Set
from pydantic import BaseModel

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class UserFilter(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    is_active: Optional[bool] = None

@app.get("/users")
async def list_users_filtered(
    # Pagination
    page: int = 1,
    limit: int = 20,
    
    # Filtering
    search: Optional[str] = None,
    name: Optional[str] = None,
    email: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    is_active: Optional[bool] = None,
    role: Optional[str] = None,
    
    # Sorting
    sort_by: str = "created_at",
    sort_order: SortOrder = SortOrder.DESC,
    
    # Field selection
    fields: Optional[str] = None,
    
    # Related resources
    include: Optional[str] = None
):
    """List users with full query parameter support"""
    
    # Build query
    query = list(users_db.values())
    
    # Apply filters
    if search:
        query = [u for u in query 
                 if search.lower() in u.name.lower() 
                 or search.lower() in u.email.lower()]
    
    if name:
        query = [u for u in query if name.lower() in u.name.lower()]
    
    if email:
        query = [u for u in query if email.lower() in u.email.lower()]
    
    if min_age is not None:
        query = [u for u in query if u.age and u.age >= min_age]
    
    if max_age is not None:
        query = [u for u in query if u.age and u.age <= max_age]
    
    if is_active is not None:
        query = [u for u in query if u.is_active == is_active]
    
    if role:
        query = [u for u in query if u.role == role]
    
    # Apply sorting
    reverse = sort_order == SortOrder.DESC
    query = sorted(query, key=lambda x: getattr(x, sort_by, ""), reverse=reverse)
    
    # Apply pagination
    total = len(query)
    start = (page - 1) * limit
    end = start + limit
    items = query[start:end]
    
    # Apply field selection
    if fields:
        field_set = set(fields.split(","))
        items = [
            {k: v for k, v in item.dict().items() if k in field_set}
            for item in items
        ]
    
    # Build response
    return {
        "data": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        },
        "sort": {
            "by": sort_by,
            "order": sort_order
        }
    }
```

### Cursor-Based Pagination

```python
class CursorPaginator:
    """Cursor-based pagination for large datasets"""
    
    def __init__(self, page_size: int = 20):
        self.page_size = page_size
    
    def paginate(
        self,
        query,
        cursor: Optional[str] = None,
        sort_by: str = "created_at",
        sort_order: SortOrder = SortOrder.DESC
    ):
        # Decode cursor
        if cursor:
            cursor_data = self._decode_cursor(cursor)
            last_value = cursor_data.get(sort_by)
        else:
            last_value = None
        
        # Apply cursor filter
        if last_value is not None:
            if sort_order == SortOrder.DESC:
                query = [q for q in query if getattr(q, sort_by) < last_value]
            else:
                query = [q for q in query if getattr(q, sort_by) > last_value]
        
        # Sort and limit
        reverse = sort_order == SortOrder.DESC
        query = sorted(query, key=lambda x: getattr(x, sort_by, ""), reverse=reverse)
        items = query[:self.page_size + 1]  # Get one extra to check if more exist
        
        has_more = len(items) > self.page_size
        items = items[:self.page_size]
        
        # Create next cursor
        next_cursor = None
        if has_more and items:
            last_item = items[-1]
            next_cursor = self._encode_cursor({
                sort_by: getattr(last_item, sort_by)
            })
        
        return {
            "data": items,
            "pagination": {
                "has_more": has_more,
                "next_cursor": next_cursor
            }
        }
    
    def _encode_cursor(self, data: dict) -> str:
        import base64
        return base64.b64encode(json.dumps(data).encode()).decode()
    
    def _decode_cursor(self, cursor: str) -> dict:
        import base64
        return json.loads(base64.b64decode(cursor.encode()).decode())
```

-----

## Error Handling

### Standardized Error Responses

```python
from typing import Optional, List, Any, Dict
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Error response model
class ErrorDetail(BaseModel):
    field: str
    message: str
    code: str

class ErrorResponse(BaseModel):
    error: str
    message: str
    code: str
    details: Optional[List[ErrorDetail]] = None
    request_id: Optional[str] = None
    timestamp: str
    help_url: Optional[str] = None

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.detail,
            code=f"ERR_{exc.status_code}",
            request_id=request.state.request_id,
            timestamp=datetime.now().isoformat()
        ).dict(exclude_none=True)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [
        ErrorDetail(
            field=".".join(str(x) for x in e["loc"]),
            message=e["msg"],
            code=e["type"]
        )
        for e in exc.errors()
    ]
    
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="ValidationError",
            message="Request validation failed",
            code="ERR_VALIDATION",
            details=details,
            request_id=request.state.request_id,
            timestamp=datetime.now().isoformat()
        ).dict(exclude_none=True)
    )

# Custom exceptions
class BusinessException(Exception):
    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 400,
        details: Optional[Dict] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(message)

@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.message,
            code=exc.code,
            details=[ErrorDetail(field="", message=exc.message, code=exc.code)]
                    if exc.details else None,
            request_id=request.state.request_id,
            timestamp=datetime.now().isoformat()
        ).dict(exclude_none=True)
    )

# Usage examples
@app.post("/orders")
async def create_order(order: OrderCreate):
    if order.quantity > 100:
        raise BusinessException(
            message="Maximum quantity exceeded",
            code="ERR_MAX_QUANTITY",
            status_code=422,
            details={"max_quantity": 100, "requested": order.quantity}
        )
```

### Error Code Reference

| Code | Status | Description |
|------|--------|-------------|
| ERR_400 | 400 | Bad Request |
| ERR_401 | 401 | Authentication Required |
| ERR_403 | 403 | Forbidden |
| ERR_404 | 404 | Resource Not Found |
| ERR_409 | 409 | Conflict |
| ERR_422 | 422 | Validation Error |
| ERR_429 | 429 | Rate Limit Exceeded |
| ERR_500 | 500 | Internal Server Error |
| ERR_503 | 503 | Service Unavailable |

-----

## API Versioning

### Versioning Strategies

```python
# Strategy 1: URL Path (most common)
@app.api_route("/v1/users", methods=["GET", "POST"])
async def users_v1(request: Request):
    return handle_request(request, version=1)

@app.api_route("/v2/users", methods=["GET", "POST"])
async def users_v2(request: Request):
    return handle_request(request, version=2)

# Strategy 2: Query Parameter
@app.get("/users")
async def get_users(request: Request, version: int = 1):
    if version == 1:
        return handle_v1(request)
    return handle_v2(request)

# Strategy 3: Header
@app.get("/users")
async def get_users(request: Request):
    version = request.headers.get("API-Version", "1")
    if version == "2":
        return handle_v2(request)
    return handle_v1(request)

# Strategy 4: Content Negotiation (Accept header)
# Accept: application/vnd.myapp.v2+json
@app.get("/users")
async def get_users(request: Request):
    accept = request.headers.get("Accept", "")
    if "v2" in accept:
        return handle_v2(request)
    return handle_v1(request)
```

### Version Migration Example

```python
# v1 endpoint
class UserV1(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime

# v2 endpoint with new field
class UserV2(BaseModel):
    id: str
    name: str
    email: EmailStr
    avatar_url: Optional[str] = None  # New field
    status: str = "active"              # New field with default
    created_at: datetime
    updated_at: datetime               # New field

# Deprecated decorator
from fastapi import FastAPI
from fastapi_utils import deprecated

@deprecated("Use /v2/users instead")
@app.get("/v1/users", response_model=List[UserV1])
async def get_users_v1():
    """Deprecated: Use v2 endpoint"""
    return get_users_v2_data()  # Reuse v2 logic

@app.get("/v2/users", response_model=List[UserV2])
async def get_users_v2():
    return get_users_v2_data()
```

-----

## Authentication & Authorization

### API Key Authentication

```python
from fastapi import Security, Depends, HTTPException
from fastapi.security import APIKeyHeader
from typing import Optional

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    # Validate against database
    key_data = await get_api_key(api_key)
    if not key_data or not key_data.is_active:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return key_data

@app.get("/users", dependencies=[Depends(verify_api_key)])
async def get_users(api_key_data: APIKey = Depends(verify_api_key)):
    return {"users": [], "api_key_owner": api_key_data.owner}
```

### JWT Authentication

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user(user_id)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### Role-Based Access Control

```python
from enum import Enum
from functools import wraps

class Role(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    GUEST = "guest"

def require_roles(*allowed_roles: Role):
    def decorator(func):
        @wraps(func)
        async def wrapper(current_user: User = Depends(get_current_user), *args, **kwargs):
            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Requires one of roles: {[r.value for r in allowed_roles]}"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@app.delete("/users/{user_id}")
@require_roles(Role.ADMIN, Role.MANAGER)
async def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_user)
):
    # Only admins can delete users, managers can only delete inactive users
    if current_user.role == Role.MANAGER:
        user = await get_user(user_id)
        if user and user.is_active:
            raise HTTPException(status_code=403, detail="Managers can only delete inactive users")
    
    await delete_user_from_db(user_id)
    return {"message": "User deleted"}
```

-----

## Rate Limiting

```python
from fastapi import Request, HTTPException
from fastapi.middlewareiddleware import Middleware
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def check_rate_limit(self, client_id: str) -> bool:
        async with self.lock:
            now = datetime.now()
            minute_ago = now - timedelta(minutes=1)
            
            # Clean old requests
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if req_time > minute_ago
            ]
            
            # Check limit
            if len(self.requests[client_id]) >= self.requests_per_minute:
                return False
            
            # Add current request
            self.requests[client_id].append(now)
            return True

rate_limiter = RateLimiter(requests_per_minute=60)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = request.client.host  # Or user ID if authenticated
    
    if not await rate_limiter.check_rate_limit(client_id):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": "60"}
        )
    
    response = await call_next(request)
    return response
```

-----

## OpenAPI Documentation

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="User Management API",
    description="API for managing users with full CRUD operations",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="User Management API",
        version="2.0.0",
        description="API for managing users",
        routes=app.routes,
    )
    
    # Add custom components
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "http",
            "scheme": "bearer",
            "description": "Enter JWT token"
        },
        "API Key": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
    
    # Add security to all endpoints
    openapi_schema["security"] = [
        {"Bearer Auth": []},
        {"API Key": []}
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

-----

## Best Practices

1. **Use consistent naming conventions** — Stick to singular or plural consistently.

2. **Return appropriate status codes** — Don't return 200 for errors or 201 for reads.

3. **Version your API** — Plan for evolution from the start.

4. **Document everything** — Use OpenAPI/Swagger for automatic documentation.

5. **Secure endpoints** — Implement authentication and authorization properly.

6. **Implement rate limiting** — Protect your API from abuse.

7. **Provide useful error messages** — Help developers debug issues.

8. **Use pagination** — Never return unbounded results.

9. **Consider HATEOAS** — Include links to related resources when appropriate.

10. **Monitor and log** — Track usage patterns and errors.
