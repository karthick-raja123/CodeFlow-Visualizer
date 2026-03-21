#!/bin/bash
# Render Deployment Script
# This script outlines the Render deployment process

echo "🚀 CodeFlow Visualizer - Render Backend Deployment Guide"
echo "==========================================================="
echo ""

echo "📋 STEP 1: Verify requirements.txt"
echo "   ✅ fastapi==0.115.0"
echo "   ✅ uvicorn[standard]==0.30.0"
echo "   ✅ pydantic==2.9.0"
echo ""

echo "🔧 STEP 2: Configure main.py"
echo "   ✅ if __name__ == \"__main__\" guard added"
echo "   ✅ uvicorn.run() with host=0.0.0.0, port=10000"
echo "   ✅ CORS middleware configured"
echo "   ✅ ALLOWED_ORIGINS from environment variable"
echo ""

echo "📝 STEP 3: Use render.yaml (Already Configured)"
echo "   Service Name:        codeflow-api"
echo "   Runtime:             Python"
echo "   Build Command:       pip install -r backend/requirements.txt"
echo "   Start Command:       uvicorn backend.main:app --host 0.0.0.0 --port 10000"
echo ""

echo "🔐 STEP 4: Set Environment Variables in Render Dashboard"
echo "   ALLOWED_ORIGINS     = https://your-frontend-url.vercel.app"
echo "   APP_ENV             = production"
echo "   PYTHONUNBUFFERED    = 1"
echo ""

echo "✅ DEPLOYMENT READY!"
echo ""
echo "Visit https://render.com and:"
echo "1. Click 'New +' > 'Web Service'"
echo "2. Select 'Deploy an existing repository'"
echo "3. Connect Python-Visualizer repo"
echo "4. Use settings from render.yaml"
echo "5. Set environment variables"
echo "6. Click 'Create Web Service'"
echo ""
echo "🎉 Done! Your backend will be available at:"
echo "   https://codeflow-api.onrender.com"
