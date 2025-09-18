# DocuBrain Backend Deployment to Render.com - STEP BY STEP

## 🚀 Clear Deployment Steps

### Step 1: Prepare Your Repository
Make sure these files are in your GitHub repo:
- `backend/requirements-deploy.txt` ✅
- `backend/server-deploy.py` ✅
- `backend/database.py` ✅
- `backend/lightweight_embeddings.py` ✅
- `render-build.sh` ✅

### Step 2: Create Render Service

1. **Go to Render.com**
   ```
   https://render.com
   ```

2. **Click "New +" → "Web Service"**

3. **Connect Repository**
   - Connect your GitHub account
   - Select repository: `PRASANNAPATIL12/3.askmydocs`
   - Click "Connect"

### Step 3: Configure Service Settings

**IMPORTANT**: Use these exact settings:

```
Name: askmydocs-backend
Environment: Python 3
Region: Oregon (US West)
Branch: main
Root Directory: backend
Build Command: ../render-build.sh
Start Command: python server-deploy.py
```

### Step 4: Set Environment Variables

Click "Advanced" → "Add Environment Variable" and add these **EXACTLY**:

```
MONGO_URL=mongodb+srv://prasannagoudasp12_db_user:OAXwiISAxIjfmR4a@cluster0.wc8trk9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

DATABASE_NAME=askmydocs

GEMINI_API_KEY=AIzaSyAfAFynwTGvJJRTVaCWdLbz8-TBi63PHCE

CORS_ORIGINS=*

PORT=10000
```

### Step 5: Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (5-10 minutes)
3. **Monitor build logs** - you should see:
   ```
   🚀 Starting DocuBrain backend build...
   📦 Installing Python dependencies...
   🔄 Setting up deployment server...
   ✅ Build completed successfully!
   ```

### Step 6: Verify Deployment

Your backend URL will be: `https://askmydocs-backend-XXXX.onrender.com`

Test it by visiting: `https://your-backend-url.onrender.com`

You should see:
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

## 🛠️ Working Commands Summary

```bash
# These are the exact commands Render will run:

# 1. Build Command:
../render-build.sh

# 2. Start Command:
python server-deploy.py

# The build script does:
pip install -r requirements-deploy.txt
cp server-deploy.py server.py
```

## 🔧 Troubleshooting

### If Build Fails:
1. Check build logs in Render dashboard
2. Verify Root Directory is set to `backend`
3. Ensure build command is `../render-build.sh`

### If Service Won't Start:
1. Check service logs in Render dashboard
2. Verify all environment variables are set correctly
3. Make sure PORT=10000 is set

### If API Doesn't Respond:
1. Test the root endpoint first
2. Check CORS_ORIGINS=* is set
3. Verify MongoDB connection string is correct

## ✅ Success Indicators

- Build logs show "✅ Build completed successfully!"
- Service status shows "Live"
- Root endpoint returns JSON with "DocuBrain API is running! 🧠"
- `/docs` endpoint shows FastAPI documentation

Your backend will be ready for frontend integration once you see these indicators!