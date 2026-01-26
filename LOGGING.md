# Logging Configuration

This project uses **loguru** for comprehensive logging throughout the FastAPI application.

## Overview

Loguru is configured to output logs to:
1. **Console (stdout)** - For development and real-time monitoring
2. **app.log** - All application logs (rotated after 500 MB, retained for 10 days)
3. **error.log** - Error and critical logs only (rotated after 500 MB, retained for 30 days)

## Configuration

The logging configuration is defined in `app/core/logger.py`:

```python
from app.core.logger import logger
```

### Log Levels

- **DEBUG**: Detailed diagnostic information for debugging
- **INFO**: General informational messages about application flow
- **WARNING**: Warning messages for potentially problematic situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical messages for severe errors

## Usage Examples

### Basic Logging

```python
from app.core.logger import logger

# Info level
logger.info("User registration completed")

# Debug level
logger.debug("Processing request with parameters: {}", params)

# Warning level
logger.warning(f"User with ID {user_id} not found")

# Error level
logger.error(f"Database connection failed: {str(error)}")
```

### In Controllers

```python
from app.core.logger import logger

def create_subject(db: Session, subject: schemas.SubjectCreate):
    logger.debug(f"Creating subject in database: {subject.name}")
    db_subject = Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    logger.info(f"Subject created with ID: {db_subject.id}")
    return db_subject
```

### In Routers

```python
from app.core.logger import logger

@router.post("/")
def create_subject(subject: schema.SubjectCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating subject: {subject.name}")
    try:
        result = subject_controller.create_subject(db, subject)
        logger.info(f"Subject created successfully with ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating subject: {str(e)}")
        raise
```

### In Security Functions

```python
from app.core.logger import logger

def hash_password(password: str) -> str:
    logger.debug("Hashing password")
    return pwd_context.hash(password[:72])

def create_access_token(data: dict):
    logger.debug(f"Creating access token for user ID: {data.get('sub')}")
    # ... token creation logic ...
    logger.debug("Access token created successfully")
    return token
```

## Log Files Location

Logs are stored in the `backend/logs/` directory:

```
backend/
├── logs/
│   ├── app.log        # All application logs
│   ├── app.log.1      # Rotated archived logs (compressed)
│   └── error.log      # Error logs only
```

## Log Format

### Console Output
```
2026-01-26 01:18:10 | INFO     | app.routers.subject_router:create_subject:16 - Creating subject: Programming
```

**Components:**
- Timestamp (YYYY-MM-DD HH:mm:ss)
- Log Level
- Module name:function:line number
- Message

### File Output
```
2026-01-26 01:18:10 | INFO     | app.routers.subject_router:create_subject:16 - Creating subject: Programming
```

## Environment Variables

Control logging behavior with environment variables:

```bash
# Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
export LOG_LEVEL=INFO
```

Default log level is **INFO** if not specified.

## Best Practices

1. **Use appropriate log levels:**
   - DEBUG: Database queries, function entry/exit, variable values
   - INFO: User actions, successful operations, state changes
   - WARNING: Recoverable errors, unusual conditions, deprecated usage
   - ERROR: Failed operations, exceptions, unexpected behavior

2. **Include relevant context:**
   ```python
   logger.info(f"User logged in successfully: {user.email} (ID: {user.id})")
   ```

3. **Log at entry and exit of critical functions:**
   ```python
   logger.debug(f"Starting password verification")
   result = verify_password(password, hashed)
   logger.debug(f"Password verification result: {result}")
   ```

4. **Log security-related events:**
   ```python
   logger.warning(f"Failed login attempt for email: {email}")
   logger.info(f"User account activated: {user.email}")
   ```

5. **Include exceptions in error logs:**
   ```python
   try:
       # operation
   except Exception as e:
       logger.error(f"Operation failed: {str(e)}")
       raise
   ```

## Where Logging Is Implemented

Logging has been added to the following modules:

- ✅ `app/main.py` - Application initialization and lifecycle events
- ✅ `app/database.py` - Database connection and session management
- ✅ `app/core/security.py` - Password hashing, token creation, and verification
- ✅ `app/core/logger.py` - Logging configuration
- ✅ `app/controllers/auth_controller.py` - Authentication operations
- ✅ `app/controllers/subject_controller.py` - Subject CRUD operations
- ✅ `app/routers/auth_router.py` - Auth API endpoints
- ✅ `app/routers/subject_router.py` - Subject API endpoints

## Accessing Logs

### View real-time logs
```bash
tail -f backend/logs/app.log
```

### View only errors
```bash
cat backend/logs/error.log
```

### Search logs
```bash
grep "user_id" backend/logs/app.log
grep "ERROR" backend/logs/app.log
```

## Rotation and Retention

- **app.log**: Rotates when file size exceeds 500 MB, retains for 10 days
- **error.log**: Rotates when file size exceeds 500 MB, retains for 30 days
- Old logs are compressed with gzip to save disk space

This automatic rotation and compression prevents log files from consuming excessive disk space in production environments.
