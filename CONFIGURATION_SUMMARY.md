# Production Database Setup - Complete Guide

## Summary of Changes

Your FastAPI application now supports environment-based database configuration with seamless switching between:
- **Development**: Local SQLite (no setup required)
- **Staging**: PostgreSQL (local or remote)
- **Production**: AWS RDS PostgreSQL with optimized connection pooling

## Files Modified/Created

### Modified Files
1. **app/core/config.py** - Added environment-based database URL generation
2. **app/database.py** - Updated to use new config and apply production-specific settings

### New Documentation Files
1. **DATABASE_CONFIG.md** - Comprehensive database configuration guide
2. **.env.example** - Environment variable template
3. **CONFIGURATION_SUMMARY.md** - This file

## How It Works

### 1. Environment Detection

```python
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
```

Defaults to `development` if not set. Valid values: `development`, `staging`, `production`

### 2. Automatic Database Selection

#### Development (Default)
```bash
# Just run the app - no configuration needed
python -m uvicorn app.main:app --reload
```
Uses: `sqlite:///./app.db`

#### Staging
```bash
export ENVIRONMENT=staging
```
Uses: `postgresql://qna_user:qna_pass@localhost:5432/qna_db_staging`

Or override with:
```bash
export DATABASE_URL=postgresql://custom:url@host:port/db
```

#### Production (AWS RDS)
```bash
export ENVIRONMENT=production
export DB_HOST=mydb.us-east-1.rds.amazonaws.com
export DB_USER=dbadmin
export DB_PASSWORD=secure_password
export DB_NAME=davinci_prod
```
Generates: `postgresql://dbadmin:secure_password@mydb.us-east-1.rds.amazonaws.com:5432/davinci_prod`

## Key Features

### Production Connection Pooling
When `ENVIRONMENT=production`, the database connection uses:
- **Pool Size**: 20 base connections
- **Max Overflow**: 40 additional temporary connections
- **Pool Pre-ping**: Enabled (checks connection health before use)
- **Pool Recycle**: 3600 seconds (protects against RDS idle timeout)

This configuration is optimized for:
- High concurrency
- AWS RDS compatibility
- Long-running applications
- Prevention of stale connection errors

### Development Configuration
- Minimal pooling overhead
- SQLite support for zero-setup local development
- Connection checks for SQLite compatibility

## Quick Start Guide

### For Development
```bash
# Nothing to do - just run:
python -m uvicorn app.main:app --reload
```

### For Production Deployment

#### Step 1: Create AWS RDS Instance
- Create a PostgreSQL database on AWS RDS
- Note the endpoint, master username, and password
- Ensure security group allows inbound traffic on port 5432

#### Step 2: Set Environment Variables
On your deployment platform (EC2, ECS, Lambda, etc.):

```bash
export ENVIRONMENT=production
export DB_HOST=your-db-instance.us-east-1.rds.amazonaws.com
export DB_PORT=5432
export DB_USER=dbadmin
export DB_PASSWORD=your_secure_password
export DB_NAME=davinci_production
export SECRET_KEY=your_production_secret_key
```

#### Step 3: Deploy Application
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The app will automatically:
- Detect production environment
- Build AWS RDS connection string
- Configure optimized connection pooling
- Log all configuration details

## Configuration Validation

The application validates production configuration on startup:

```
Environment: production
Initializing database connection: postgresql://user:pass@host:5432/db
Using production database connection pool configuration
```

If required variables are missing in production, you'll see:
```
ValueError: Production environment requires DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME
```

## Environment Variables Reference

| Variable | Required | Default | Used For |
|----------|----------|---------|----------|
| `ENVIRONMENT` | No | `development` | Environment selection |
| `SECRET_KEY` | No | `super-secret-key` | JWT token signing |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity |
| `DATABASE_URL` | No | Auto-generated | Override DB URL (all envs) |
| `DB_HOST` | Production only | - | RDS endpoint |
| `DB_PORT` | No | `5432` | Database port |
| `DB_USER` | Production only | - | DB username |
| `DB_PASSWORD` | Production only | - | DB password |
| `DB_NAME` | Production only | - | Database name |

## Docker & Kubernetes Deployment

### Docker (with RDS)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker run -e ENVIRONMENT=production \
           -e DB_HOST=mydb.rds.amazonaws.com \
           -e DB_USER=admin \
           -e DB_PASSWORD=secret \
           -e DB_NAME=proddb \
           -e SECRET_KEY=key \
           -p 8000:8000 \
           myapp:latest
```

### Kubernetes ConfigMap (for non-sensitive vars)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  ENVIRONMENT: "production"
  DB_PORT: "5432"
  LOG_LEVEL: "INFO"
```

### Kubernetes Secret (for sensitive vars)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:
  DB_HOST: "mydb.us-east-1.rds.amazonaws.com"
  DB_USER: "dbadmin"
  DB_PASSWORD: "secure_password"
  DB_NAME: "davinci_prod"
  SECRET_KEY: "your_secret_key"
```

## Testing & Verification

### Test Development Configuration
```bash
python -c "from app.core.config import DATABASE_URL, ENVIRONMENT; print(f'{ENVIRONMENT}: {DATABASE_URL}')"
# Output: development: sqlite:///./app.db
```

### Test Production Configuration
```bash
export ENVIRONMENT=production
export DB_HOST=test.rds.amazonaws.com
export DB_USER=admin
export DB_PASSWORD=pass
export DB_NAME=testdb

python -c "from app.core.config import DATABASE_URL, ENVIRONMENT; print(f'{ENVIRONMENT}: {DATABASE_URL}')"
# Output: production: postgresql://admin:pass@test.rds.amazonaws.com:5432/testdb
```

### Run Application Tests
```bash
pytest -v
# All tests should pass regardless of environment
```

## Logging

All database configuration is logged on startup. Check logs:

```bash
tail -f logs/app.log | grep -E "Environment|Initializing database|connection pool"
```

## AWS RDS Setup Checklist

- [ ] Create RDS PostgreSQL instance
- [ ] Configure security group (allow port 5432)
- [ ] Create master user and database
- [ ] Test connection locally (optional):
  ```bash
  psql postgresql://user:pass@endpoint:5432/dbname
  ```
- [ ] Set environment variables on deployment platform
- [ ] Deploy application
- [ ] Monitor logs for connection issues
- [ ] Verify application is running: `curl http://localhost:8000/`

## Troubleshooting

### "Could not connect to database"
1. Verify `ENVIRONMENT=production` is set
2. Check all DB_* environment variables are set
3. Verify RDS security group allows inbound traffic
4. Test connection: `psql postgresql://user:pass@host:5432/db`

### Connection timeout after 15 minutes
This is expected with AWS RDS (900 second idle timeout). The `pool_recycle=3600` setting prevents this.

### "Production environment requires DB_HOST..."
All production variables must be set: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

### "Invalid password" error
1. Verify password doesn't contain special characters that need escaping
2. If password has special chars, ensure proper URL encoding
3. Test credentials with: `psql postgresql://user:pass@host:5432/db`

## Further Reading

- [DATABASE_CONFIG.md](./DATABASE_CONFIG.md) - Detailed configuration guide
- [LOGGING.md](./LOGGING.md) - Logging setup and usage
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
