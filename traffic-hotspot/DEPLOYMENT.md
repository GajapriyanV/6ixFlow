# 🚀 Deployment Guide

This guide covers deploying the 6ixFlow Toronto Traffic Hotspot Predictor to production.

## 🌐 Frontend Deployment (Vercel)

### 1. Prepare for Deployment

```bash
cd web
npm run build  # Test the build locally
```

### 2. Deploy to Vercel

1. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Select the `traffic-hotspot/web` folder as the root directory

2. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL=https://your-api-domain.com
   NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
   ```

3. **Deploy**: Vercel will automatically deploy on every push to main

### Alternative: Netlify

```bash
# Build the project
cd web
npm run build
npm run export  # For static export

# Deploy to Netlify
npx netlify deploy --prod --dir=out
```

## 🖥️ Backend Deployment

### Option 1: Railway

1. **Connect Repository**:
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Select the `traffic-hotspot` folder

2. **Environment Setup**:
   ```bash
   # Railway will auto-detect Python and install requirements.txt
   ```

3. **Deploy**: Railway will automatically deploy and provide a URL

### Option 2: Render

1. **Create Web Service**:
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Choose "Web Service"

2. **Configuration**:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: cd api && python main.py
   ```

### Option 3: Heroku

1. **Create Heroku App**:
   ```bash
   heroku create your-app-name
   ```

2. **Deploy**:
   ```bash
   git subtree push --prefix traffic-hotspot heroku main
   ```

## 🐳 Docker Deployment

### Backend Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "api/main.py"]
```

### Frontend Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY web/package*.json ./
RUN npm install

COPY web/ .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app

  frontend:
    build:
      context: .
      dockerfile: web/Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🔧 Production Considerations

### Environment Variables

**Backend**:
```bash
# Optional: Add these for production
CORS_ORIGINS=https://your-frontend-domain.com
LOG_LEVEL=INFO
```

**Frontend**:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
NEXT_PUBLIC_MAPBOX_TOKEN=your_production_mapbox_token
```

### Performance Optimization

1. **Model Caching**: Models are loaded once on startup
2. **API Caching**: Consider adding Redis for prediction caching
3. **CDN**: Use a CDN for static assets
4. **Database**: Consider adding a database for prediction history

### Security

1. **CORS**: Configure CORS origins for production
2. **Rate Limiting**: Add rate limiting to API endpoints
3. **Authentication**: Add API keys if needed
4. **HTTPS**: Ensure all traffic uses HTTPS

## 📊 Monitoring

### Health Checks

The API includes a health endpoint:
```bash
curl https://your-api-domain.com/health
```

### Logging

Add structured logging for production:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 🚨 Troubleshooting

### Common Issues

1. **Model Loading Errors**: Ensure all model files are included in deployment
2. **CORS Issues**: Check CORS configuration for production domains
3. **Memory Issues**: ML models require sufficient memory (1GB+ recommended)
4. **Mapbox Token**: Ensure production token has correct domain restrictions

### Debug Commands

```bash
# Check API health
curl https://your-api-domain.com/health

# Test prediction endpoint
curl -X POST https://your-api-domain.com/predict_at \
  -H "Content-Type: application/json" \
  -d '{"datetime": "2024-10-03T17:00:00"}'
```

## 📈 Scaling

For high traffic:
1. **Load Balancing**: Use multiple API instances
2. **Caching**: Implement Redis for prediction caching
3. **Database**: Store prediction history for analytics
4. **CDN**: Use CloudFlare or similar for static assets

---

Need help? Open an issue on [GitHub](https://github.com/GajapriyanV/6ixFlow/issues)!
