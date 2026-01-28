# Environment and Database Configuration

This document explains how to configure the application for different environments and databases.

## Environment Setup

### Environment Variable: `ENVIRONMENT`

Controls which configuration profile to use. Valid values: `development`, `staging`, `production`

```bash
export ENVIRONMENT=production  # For AWS RDS
export ENVIRONMENT=staging     # For staging environment
export ENVIRONMENT=development # For local development (default)
```

## Database Configuration by Environment

### Development (Default)

Local SQLite database. No configuration needed.

```bash
export ENVIRONMENT=development
# Optional: Override with custom DATABASE_URL
export DATABASE_URL=sqlite:///./app.db
```

**Automatic:** Uses `sqlite:///./app.db` in the project directory.

### Staging

Local or remote PostgreSQL database.

```bash
export ENVIRONMENT=staging
export DATABASE_URL=postgresql://username:password@localhost:5432/db_name
```

**Or use default staging database:**

```bash
export ENVIRONMENT=staging
# Uses: postgresql://qna_user:qna_pass@localhost:5432/qna_db_staging
```

### Production (AWS RDS)

AWS RDS PostgreSQL with optimized connection pooling.

```bash
export ENVIRONMENT=production
export DB_HOST=your-rds-endpoint.us-east-1.rds.amazonaws.com
export DB_PORT=5432
export DB_USER=admin
export DB_PASSWORD=your_secure_password
export DB_NAME=production_db
```

**Required variables for production:**
- `DB_HOST` - RDS endpoint (required)
- `DB_USER` - Database username (required)
- `DB_PASSWORD` - Database password (required)
- `DB_NAME` - Database name (required)
- `DB_PORT` - Database port (optional, defaults to 5432)

## Complete Environment File Example

### Development (.env.development)

```bash
ENVIRONMENT=development
SECRET_KEY=your-secret-key-for-development
LOG_LEVEL=DEBUG
```

### Production (.env.production)

```bash
ENVIRONMENT=production
SECRET_KEY=your-secret-key-for-production
LOG_LEVEL=INFO
DB_HOST=my-app-db.us-east-1.rds.amazonaws.com
DB_PORT=5432
DB_USER=dbadmin
DB_PASSWORD=secure_password_here
DB_NAME=davinci_prod
```

## Database Connection Configuration

### Development/Staging
- Standard SQLAlchemy configuration
- No connection pooling overhead
- Suitable for local development and testing

### Production (AWS RDS)
- **Pool Size:** 20 connections
- **Max Overflow:** 40 additional connections
- **Pool Pre-ping:** Enabled (verifies connection health before use)
- **Pool Recycle:** 3600 seconds (RDS timeout protection)
- **Echo:** Disabled (no query logging for performance)

These settings ensure:
- Optimal performance for production workloads
- Connection stability with AWS RDS
- Graceful handling of idle connection timeout (RDS default is 900 seconds)

## Quick Start

### Local Development

```bash
# Just run the app - uses SQLite by default
python -m uvicorn app.main:app --reload
```

### Production Deployment

```bash
# Set environment variables (typically via AWS RDS configuration)
export ENVIRONMENT=production
export DB_HOST=your-rds-endpoint.rds.amazonaws.com
export DB_USER=dbadmin
export DB_PASSWORD=secure_password
export DB_NAME=davinci_prod
export SECRET_KEY=your-production-secret-key

# Start the application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker Deployment

### Dockerfile Example

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose with AWS RDS

```yaml
version: '3.8'
services:
  api:
    build: .
    environment:
      ENVIRONMENT: production
      DB_HOST: ${DB_HOST}
      DB_PORT: ${DB_PORT}
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
      DB_NAME: ${DB_NAME}
      SECRET_KEY: ${SECRET_KEY}
    ports:
      - "8000:8000"
```

Run with:

```bash
DB_HOST=your-rds-endpoint.rds.amazonaws.com \
DB_USER=dbadmin \
DB_PASSWORD=password \
DB_NAME=davinci_prod \
SECRET_KEY=your-key \
docker-compose up
```

## Environment Variables Reference

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `ENVIRONMENT` | No | `development` | Deployment environment |
| `SECRET_KEY` | No | `super-secret-key` | JWT secret key |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity |
| `DATABASE_URL` | No | Varies by env | Full database URL (overrides other DB vars) |
| `DB_HOST` | Production only | - | RDS endpoint |
| `DB_PORT` | No | `5432` | Database port |
| `DB_USER` | Production only | - | Database username |
| `DB_PASSWORD` | Production only | - | Database password |
| `DB_NAME` | Production only | - | Database name |

## Database URL Format

### PostgreSQL (AWS RDS)

```
postgresql://username:password@host:port/database
```

Example:
```
postgresql://dbadmin:securepass@mydb.us-east-1.rds.amazonaws.com:5432/davinci_prod
```

### SQLite (Development)

```
sqlite:///./app.db
```

## Testing Configuration

For testing, use an isolated database:

```python
# tests/conftest.py
import os
os.environ["ENVIRONMENT"] = "development"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
```

## AWS RDS Setup Checklist

- [ ] Create RDS PostgreSQL instance in AWS
- [ ] Note the endpoint URL
- [ ] Create database user and password
- [ ] Create initial database
- [ ] Configure security group to allow application access
- [ ] Set environment variables on deployment platform
- [ ] Test connection before going live

## Troubleshooting

### "Production environment requires DB_HOST..."

**Solution:** When `ENVIRONMENT=production`, all of `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` must be set.

### Connection timeout on RDS

**Solution:** Ensure:
1. Security group allows inbound traffic on port 5432
2. RDS instance is publicly accessible (if needed)
3. Database user credentials are correct

### "Could not connect to database"

**Solution:** Verify connection string format:
```bash
# Test connection (requires psql)
psql postgresql://user:password@host:5432/dbname
```
