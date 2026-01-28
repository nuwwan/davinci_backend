# Quick Reference: Environment & Database Setup

## TL;DR - Quick Start

### Local Development (Default)
```bash
cd backend
python -m uvicorn app.main:app --reload
```
✅ Uses SQLite automatically. No setup needed.

### AWS Production
```bash
export ENVIRONMENT=production
export DB_HOST=your-rds-endpoint.amazonaws.com
export DB_USER=admin
export DB_PASSWORD=password
export DB_NAME=davinci_prod

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
✅ Connects to AWS RDS with optimized pooling

---

## Environment Variables

```bash
# Always
ENVIRONMENT=production                                    # or: development, staging
SECRET_KEY=your-secret-key                               # Change in production!

# Production Only (AWS RDS)
DB_HOST=your-db.us-east-1.rds.amazonaws.com
DB_PORT=5432                                             # optional, default: 5432
DB_USER=dbadmin
DB_PASSWORD=secure_password
DB_NAME=production_database
```

---

## What Database Am I Using?

| ENVIRONMENT | Default Database | Connection |
|---|---|---|
| `development` | SQLite | `sqlite:///./app.db` (local) |
| `staging` | PostgreSQL | `localhost:5432` (local) |
| `production` | AWS RDS | `your-rds-endpoint:5432` (cloud) |

---

## Docker Deployment

```bash
docker run -e ENVIRONMENT=production \
           -e DB_HOST=mydb.rds.amazonaws.com \
           -e DB_USER=admin \
           -e DB_PASSWORD=secure_pass \
           -e DB_NAME=prod_db \
           -e SECRET_KEY=secret \
           -p 8000:8000 \
           myapp:latest
```

---

## Verify Configuration

```bash
# Check which environment and database you're using
python -c "from app.core.config import ENVIRONMENT, DATABASE_URL; print(f'{ENVIRONMENT}: {DATABASE_URL}')"
```

---

## Connection Pooling (Production Only)

Production automatically uses:
- **20 base connections** + **40 overflow**
- **Connection health checks** before use
- **Auto-recycle** every hour (prevents RDS timeout)

No configuration needed - it's automatic!

---

## Logs

```bash
# Real-time logs with configuration details
tail -f logs/app.log

# Just errors
tail -f logs/error.log

# Search for DB connection info
grep "Initializing database" logs/app.log
```

---

## Common Issues & Fixes

| Problem | Fix |
|---|---|
| SQLite file not created | Make sure `ENVIRONMENT=development` (default) |
| Can't connect to RDS | Check `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` are all set when `ENVIRONMENT=production` |
| Connection timeout after 15min | Already fixed! Pool recycles every 60min to prevent RDS idle timeout |
| Wrong database being used | Check `ENVIRONMENT` variable: `echo $ENVIRONMENT` |

---

## AWS RDS Checklist

- [ ] Create RDS PostgreSQL instance
- [ ] Note the endpoint (e.g., `mydb.us-east-1.rds.amazonaws.com`)
- [ ] Create database and user
- [ ] Allow inbound traffic on port 5432
- [ ] Set 5 environment variables
- [ ] Run the app
- [ ] Check logs: `grep "production" logs/app.log`

---

## Files Changed

- ✅ `app/core/config.py` - Database URL logic
- ✅ `app/database.py` - Connection pooling
- ✅ `DATABASE_CONFIG.md` - Full guide
- ✅ `.env.example` - Template
- ✅ `CONFIGURATION_SUMMARY.md` - Complete reference

---

## More Info

📖 See [DATABASE_CONFIG.md](./DATABASE_CONFIG.md) for full documentation
📖 See [CONFIGURATION_SUMMARY.md](./CONFIGURATION_SUMMARY.md) for detailed setup guide
