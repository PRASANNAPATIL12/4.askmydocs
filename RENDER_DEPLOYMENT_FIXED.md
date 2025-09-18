# 🚀 RENDER.COM DEPLOYMENT - FIXED VERSION

## Issue Resolved
**Problem**: Port mismatch - server was running on 8001 but Render expected 10000
**Solution**: Updated server-deploy.py to use PORT environment variable

## 🔧 EXACT DEPLOYMENT STEPS

### Step 1: Update Your GitHub Repository
Push the updated files to your repository:
```bash
git add .
git commit -m "Fix port configuration for Render deployment"
git push origin main
```

### Step 2: Create New Render Service

1. **Go to Render Dashboard**
   ```
   https://dashboard.render.com
   ```

2. **Click "New +" → "Web Service"**

3. **Connect Repository**
   - Select: `PRASANNAPATIL12/3.askmydocs`
   - Click "Connect"

### Step 3: Configure Service Settings

**CRITICAL**: Use these EXACT settings:

```
Service Name: askmydocs-backend
Environment: Python 3
Region: Oregon (US West)
Branch: main
Root Directory: backend
Build Command: ../render-build.sh
Start Command: python server-deploy.py
```

### Step 4: Environment Variables

Click "Advanced" and add exactly these variables:

```
MONGO_URL=mongodb+srv://prasannagoudasp12_db_user:OAXwiISAxIjfmR4a@cluster0.wc8trk9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

DATABASE_NAME=askmydocs

GEMINI_API_KEY=AIzaSyAfAFynwTGvJJRTVaCWdLbz8-TBi63PHCE

CORS_ORIGINS=*

PORT=10000
```

### Step 5: Deploy

1. **Click "Create Web Service"**
2. **Monitor Build Logs** - Should see:
   ```
   🚀 Starting DocuBrain backend build...
   📦 Installing Python dependencies...
   🔄 Setting up deployment server...
   ✅ Build completed successfully!
   🚀 Server will start on PORT=10000
   ```

3. **Monitor Deploy Logs** - Should see:
   ```
   ✅ Google Gemini loaded successfully for deployment
   ✅ Gemini client initialized
   ✅ Successfully connected to MongoDB database: askmydocs
   INFO: Uvicorn running on http://0.0.0.0:10000
   ```

### Step 6: Test Deployment

Your backend URL: `https://askmydocs-backend-XXXX.onrender.com`

Test endpoint:
```bash
curl https://your-backend-url.onrender.com
```

Expected response:
```json
{
  "message": "DocuBrain API is running! 🧠",
  "version": "1.0.0",
  "endpoints": {
    "register": "POST /api/auth/register",
    "login": "POST /api/auth/login", 
    "upload": "POST /api/documents/upload",
    "query": "POST /api/query",
    "docs": "/docs"
  }
}
```

## ✅ Success Indicators

- Build shows: "✅ Build completed successfully!"
- Deploy shows: "INFO: Uvicorn running on http://0.0.0.0:10000"
- Service status: "Live" (green)
- API responds with DocuBrain message

## 🔧 What Was Fixed

1. **Port Configuration**: Server now uses `PORT` environment variable
2. **Build Script**: Shows which port server will use
3. **Start Command**: Correctly uses `python server-deploy.py`

## 🚨 If Still Failing

Check these in order:

1. **Build Command**: Must be `../render-build.sh`
2. **Root Directory**: Must be `backend`
3. **Environment Variables**: All 5 variables set correctly
4. **GitHub**: Latest code pushed to main branch

The port issue is now fixed! Try the deployment again with these exact settings.