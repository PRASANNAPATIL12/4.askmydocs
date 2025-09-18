# DocuBrain Deployment Guide - FIXED VERSION

## Issue Resolution

The deployment was failing because `emergentintegrations==0.1.0` is not available on public PyPI repositories. This guide provides the corrected deployment process.

## Fixed Files Created

1. `backend/requirements-deploy.txt` - Clean requirements without emergentintegrations
2. `backend/server-deploy.py` - Server version using OpenAI API instead of emergentintegrations
3. `backend/.env.example` - Example environment configuration

## Backend Deployment (Render.com) - FIXED

### 1. Create Render Service
- Go to render.com → New → Web Service
- Connect your GitHub repo: https://github.com/PRASANNAPATIL12/3.askmydocs.git
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements-deploy.txt`
- **Start Command**: `python server-deploy.py`

### 2. Set Environment Variables in Render Dashboard

```env
MONGO_URL=mongodb+srv://prasannagoudasp12_db_user:OAXwiISAxIjfmR4a@cluster0.wc8trk9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
DATABASE_NAME=askmydocs
OPENAI_API_KEY=your_openai_api_key_here
CORS_ORIGINS=*
PORT=10000
```

**IMPORTANT**: You need to get an OpenAI API key from https://platform.openai.com/api-keys

### 3. Deploy
- Click "Create Web Service"
- Wait for deployment (5-10 minutes)
- Your backend URL will be: `https://your-service-name.onrender.com`

## Frontend Deployment (Vercel) - UPDATED

### 1. Prepare Frontend
Update your frontend environment variables after backend is deployed:

```env
REACT_APP_BACKEND_URL=https://your-backend-service.onrender.com
```

### 2. Deploy to Vercel
- Go to vercel.com → New Project
- Connect your GitHub repo: https://github.com/PRASANNAPATIL12/3.askmydocs.git
- **Root Directory**: `frontend`
- **Build Command**: `yarn build`
- **Output Directory**: `build`
- **Install Command**: `yarn install`

### 3. Set Environment Variables in Vercel
```env
REACT_APP_BACKEND_URL=https://your-backend-service.onrender.com
```

### 4. Deploy
- Click "Deploy"
- Your frontend will be available at: `https://your-project.vercel.app`

## Alternative: Using Your Own OpenAI Key

If you want to use your own OpenAI API key instead of emergentintegrations:

1. Get your OpenAI API key from https://platform.openai.com/api-keys
2. Add it to your Render environment variables as `OPENAI_API_KEY`
3. The deployment version will use OpenAI's gpt-4o-mini model

## Testing the Deployment

1. Open your frontend URL
2. Register a new account
3. Upload a PDF document
4. Ask a question about the document
5. Verify the AI responses work correctly

## Troubleshooting

### Common Issues:

1. **Build fails with emergentintegrations error**
   - Make sure you're using `requirements-deploy.txt`
   - Verify Root Directory is set to `backend`

2. **No AI responses**
   - Check that OPENAI_API_KEY is set correctly in Render
   - Verify your OpenAI account has credits

3. **CORS errors**
   - Make sure CORS_ORIGINS=* is set in backend environment
   - Verify your frontend URL is correct

4. **Database connection fails**
   - Double-check MONGO_URL is correct
   - Verify DATABASE_NAME is set to "askmydocs"

## Files Modified for Deployment

- `backend/requirements-deploy.txt` - Removed emergentintegrations dependency
- `backend/server-deploy.py` - Replaced emergentintegrations with OpenAI API
- `backend/.env.example` - Added OpenAI configuration

The deployment version maintains all functionality while using standard OpenAI API instead of the proprietary emergentintegrations package.