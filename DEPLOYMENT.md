# Deployment Guide

Deploy Focus Group AI to production.

## Option 1: Deploy to Railway (Easiest)

### Backend

1. Go to [railway.app](https://railway.app)
2. Create a new project from GitHub
3. Add environment variables:
   - `ANTHROPIC_API_KEY` - Your API key
   - `DATABASE_URL` - Railway will provide this
   - `ALLOWED_ORIGINS` - ["https://your-frontend-url.com"]

### Frontend

1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Add environment variables:
   - `NEXT_PUBLIC_API_URL` - Your Railway backend URL
   - `NEXT_PUBLIC_WS_URL` - Your Railway backend URL (wss://)

---

## Option 2: Deploy to Render

### Backend

1. Go to [render.com](https://render.com)
2. Create new Web Service from GitHub
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Environment variables:
   - `ANTHROPIC_API_KEY`
   - `DATABASE_URL` (Render PostgreSQL)
   - `REDIS_URL` (Render Redis)

### Frontend

1. Create new Static Site on Render
2. Build Command: `npm install && npm run build`
3. Publish Directory: `.next`
4. Environment variables:
   - `NEXT_PUBLIC_API_URL`
   - `NEXT_PUBLIC_WS_URL`

---

## Option 3: Deploy to AWS/GCP/Azure

### Requirements
- EC2/Compute instance
- PostgreSQL database
- Redis instance
- Load balancer (for WebSocket support)

### Setup

1. **Install dependencies:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
npm run build
```

2. **Environment variables:**
```bash
# Backend
export ANTHROPIC_API_KEY=your-key
export DATABASE_URL=postgresql://...
export REDIS_URL=redis://...

# Frontend
export NEXT_PUBLIC_API_URL=https://api.yourdomain.com
export NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
```

3. **Process managers:**
```bash
# Backend with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# Frontend with PM2
pm2 start npm --name "frontend" -- start
```

4. **Nginx configuration:**
```nginx
# Backend (with WebSocket support)
upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
```

---

## Option 4: Docker Deployment

### Build images

```bash
# Backend
cd backend
docker build -t focus-group-backend .

# Frontend
cd frontend
docker build -t focus-group-frontend .
```

### Run with Docker Compose

```bash
# Production docker-compose.yml
docker-compose -f docker-compose.prod.yml up -d
```

### Deploy to Container Registry

```bash
# Tag images
docker tag focus-group-backend:latest your-registry/focus-group-backend:latest
docker tag focus-group-frontend:latest your-registry/focus-group-frontend:latest

# Push to registry
docker push your-registry/focus-group-backend:latest
docker push your-registry/focus-group-frontend:latest
```

---

## Database Setup

### PostgreSQL

```sql
CREATE DATABASE focusgroup;
CREATE USER focusgroup_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE focusgroup TO focusgroup_user;
```

### Run migrations

```bash
cd backend
# Using Alembic (if you set it up)
alembic upgrade head
```

---

## Environment Variables Checklist

### Backend
- ✅ `ANTHROPIC_API_KEY` - Required
- ✅ `DATABASE_URL` - Required for persistence
- ✅ `REDIS_URL` - Optional, for caching
- ✅ `ALLOWED_ORIGINS` - Set to your frontend URL
- ✅ `DEFAULT_MODEL` - Default: claude-sonnet-4-20250514

### Frontend
- ✅ `NEXT_PUBLIC_API_URL` - Your backend URL
- ✅ `NEXT_PUBLIC_WS_URL` - Your backend WebSocket URL

---

## SSL/HTTPS Setup

### Using Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Monitoring & Logging

### Recommended Tools
- **Logging:** Sentry, LogRocket
- **Monitoring:** Datadog, New Relic
- **Uptime:** UptimeRobot, Pingdom
- **Analytics:** PostHog, Mixpanel

### Add to backend

```python
# app/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

---

## Performance Tips

1. **Enable caching** - Use Redis for persona data
2. **Database indexes** - Add indexes on frequently queried fields
3. **CDN** - Serve static assets via CDN
4. **Connection pooling** - Configure SQLAlchemy pool size
5. **Rate limiting** - Add rate limits to prevent abuse

---

## Security Checklist

- ✅ Use HTTPS everywhere
- ✅ Set proper CORS origins
- ✅ Validate all user inputs
- ✅ Rate limit API endpoints
- ✅ Use environment variables for secrets
- ✅ Enable database backups
- ✅ Monitor for unusual activity
- ✅ Keep dependencies updated

---

## Scaling

### Horizontal Scaling
- Deploy multiple backend instances behind load balancer
- Use Redis for session sharing
- Database connection pooling

### Vertical Scaling
- Increase CPU/RAM for LLM processing
- Optimize database queries
- Add database read replicas

---

**Questions?** Check the main README.md or open an issue.
