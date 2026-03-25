════════════════════════════════════════════════════════════════════════════════
          RENDER DEPLOYMENT - FORCE CLEAN BUILD INSTRUCTIONS
                      Step-by-Step with Screenshots Guide
════════════════════════════════════════════════════════════════════════════════

OBJECTIVE: Force Render to deploy latest code commit (95b2861) with clean build

Current Status:
  ✅ GitHub repository is updated with correct code (commit 95b2861)
  ✅ backend/main.py has correct imports (from backend.executor import ...)
  ✅ render.yaml is configured correctly (startCommand: backend.main:app)
  ✅ All files are synchronized between local, git, and GitHub

Next Step: Deploy to Render with clean build (no caches)

════════════════════════════════════════════════════════════════════════════════
STEP-BY-STEP DEPLOYMENT INSTRUCTIONS
════════════════════════════════════════════════════════════════════════════════

STEP 1: Open Render Dashboard
─────────────────────────────────────────────────────────────────────────────
Action:
  1. Open browser
  2. Go to: https://dashboard.render.com
  3. Log in with your Render account

You should see your list of services.

STEP 2: Select the API Service
─────────────────────────────────────────────────────────────────────────────
Action:
  1. Look for: "codeflow-visualizer-api"
  2. Click on it to open the service details

You should see:
  • Service name: codeflow-visualizer-api
  • Status: Active (or similar)
  • Last deployed: (specific date/time)
  • Tabs: Overview, Deployments, Logs, Events, Settings

STEP 3: Navigate to Deployments Tab
─────────────────────────────────────────────────────────────────────────────
Action:
  1. Click: "Deployments" tab (near Overview tab)
  2. You'll see list of previous deployments

Expected to see:
  • List of past deployments with timestamps
  • Latest should show the previous deployment
  • Commit hashes should be visible

(Optional) If you want to verify commit 95b2861 exists:
  • Look through deployment list
  • Should see a deployment that includes "95b2861" or your latest commit

STEP 4: Open Service Settings (To Clear Cache)
─────────────────────────────────────────────────────────────────────────────
Action:
  1. Click: "Settings" tab
  2. Scroll down to find: "Clear Build Cache" button
  3. Click: "Clear Build Cache"
  4. Confirm: "Clear" when prompted

This ensures:
  ✅ Old pip package caches are removed
  ✅ Fresh Python environment is created
  ✅ All dependencies are reinstalled fresh
  ✅ No stale modules from previous builds

Wait for confirmation that cache was cleared (usually instant).

STEP 5: Return to Service Overview
─────────────────────────────────────────────────────────────────────────────
Action:
  1. Click: "Overview" tab (or back to main service view)
  2. Look for: "Manual Deploy" button (usually top right)

You should see:
  • Service status
  • Manual Deploy button
  • Recent git commits info
  • Current environment variables

STEP 6: Trigger Manual Deploy
─────────────────────────────────────────────────────────────────────────────
Action:
  1. Click: "Manual Deploy" button (top of page, right side)
  2. A dropdown menu appears
  3. Select: "Deploy latest commit"
  4. Confirm: Click "Deploy" when prompted

Expected confirmation message:
  "Deploying commit 95b2861..."
  or
  "Deployment started"

The system will now:
  ✅ Pull latest code from GitHub (commit 95b2861)
  ✅ Install dependencies (pip install -r requirements.txt)
  ✅ Build Docker container
  ✅ Start uvicorn with: uvicorn backend.main:app --host 0.0.0.0 --port 10000
  ✅ Run any health checks

STEP 7: Monitor Build Progress
─────────────────────────────────────────────────────────────────────────────
Action:
  1. Go to: "Logs" tab
  2. Watch the real-time build output

You should see logs like:
  ```
  Building Docker image...
  Cloning repository from GitHub
  Checking out commit 95b2861...
  Installing dependencies...
  pip install fastapi==0.115.0
  pip install uvicorn[standard]==0.30.0
  ...
  [Dependency installation continues]
  ...
  Successfully installed [packages]
  Starting server process [PID]
  Waiting for application startup.
  Application startup complete.
  Uvicorn running on http://0.0.0.0:10000
  ```

Estimated time: 3-5 minutes for complete build and startup

CRITICAL: Look for these SUCCESS indicators:
  ✅ "Successfully installed" message
  ✅ "Application startup complete"
  ✅ "Uvicorn running on http://0.0.0.0:10000"

CRITICAL: Look for these ERROR indicators (should NOT see):
  ❌ "ModuleNotFoundError: No module named 'executor'"
  ❌ "ModuleNotFoundError: No module named 'backend'"
  ❌ "ImportError: cannot import name 'run_code'"
  ❌ "from executor import" in error message

If you see any errors:
  → Note the exact error message
  → Jump to TROUBLESHOOTING section below

STEP 8: Verify Deployment Success
─────────────────────────────────────────────────────────────────────────────
Action:
  1. Go to: "Events" or "Overview" tab
  2. Look for: "Deployment succeeded" or "Active" status

Expected status:
  ✅ Service status: "Live"
  ✅ Deployment status: "Succeeded"
  ✅ Last deployed: Current date/time (just now)

STEP 9: Test Live Application
─────────────────────────────────────────────────────────────────────────────
Action:
  1. Open terminal or browser
  2. Test health endpoint:

  curl https://codeflow-visualizer-api.onrender.com/health

Expected response:
  ```json
  {"status": "ok"}
  ```

If successful:
  ✅ Deployment is working
  ✅ Application started correctly
  ✅ Import issues are resolved
  ✅ Ready for full testing

STEP 10: Test Core Execute Endpoint
─────────────────────────────────────────────────────────────────────────────
Action:
  Test actual code execution:

  curl -X POST https://codeflow-visualizer-api.onrender.com/execute \
    -H "Content-Type: application/json" \
    -d '{"code":"print(2+2)","input_data":""}'

Expected response:
  ```json
  {
    "output": "4\n",
    "error": "",
    "status": "success",
    "exit_code": 0
  }
  ```

If successful:
  ✅ Code execution is working
  ✅ Subprocess isolation is functional
  ✅ backend.executor module is loaded
  ✅ All imports resolved correctly

════════════════════════════════════════════════════════════════════════════════
🚨 TROUBLESHOOTING - IF THINGS GO WRONG
════════════════════════════════════════════════════════════════════════════════

Problem 1: "ModuleNotFoundError: No module named 'executor'"
─────────────────────────────────────────────────────────
Cause: render.yaml is still using old configuration or cache issue
Solution:
  1. Go to Settings tab
  2. Verify render.yaml section shows:
     startCommand: uvicorn backend.main:app --host 0.0.0.0 --port 10000
  3. If different, update it
  4. Clear Build Cache (Step 4 above)
  5. Re-run Manual Deploy

Problem 2: "ModuleNotFoundError: No module named 'backend'"
─────────────────────────────────────────────────────────
Cause: Render running from wrong directory or Python path issue
Solution:
  1. Check render.yaml buildCommand shows:
     pip install -r requirements.txt (NOT api/requirements.txt)
  2. Check that build is running from project root
  3. Clear Build Cache
  4. Manual Deploy again

Problem 3: Deployment still shows old code
─────────────────────────────────────────
Cause: GitHub push might not have reached remote
Solution:
  1. Verify locally:
     git log -1
     Should show commit 95b2861
  2. Check remote:
     git push origin main
     Should say "everything up-to-date" if already pushed
  3. In Render, manually check latest commit:
     Go to Deployments tab
     Verify 95b2861 appears in list
  4. If not showing, wait 1-2 minutes for GitHub webhook

Problem 4: Service shows "Error" or "Failed" status
──────────────────────────────────────────────────
Cause: Build failed or deployment crashed
Solution:
  1. Check Logs tab for error messages
  2. Note exact error
  3. Try "Clear Build Cache" and redeploy
  4. If still fails, check:
     - requirements.txt syntax
     - Python version compatibility
     - Port 10000 availability

Problem 5: Tests pass locally but fail on Render
────────────────────────────────────────────────
Cause: Environment differences (Python path, imports, etc.)
Solution:
  1. Run locally: python validate_imports.py
  2. Verify output matches expectations
  3. Clear cache on Render
  4. Check environment variables in Settings tab
  5. Redeploy with fresh build

════════════════════════════════════════════════════════════════════════════════
✅ SUCCESS CHECKLIST
════════════════════════════════════════════════════════════════════════════════

After deployment completes, verify:

Build Phase:
  ☐ No errors in build logs
  ☐ "Successfully installed" message present
  ☐ Dependencies installed from requirements.txt

Startup Phase:
  ☐ "Application startup complete" in logs
  ☐ "Uvicorn running on http://0.0.0.0:10000" appears
  ☐ Service status shows "Live" or "Active"

Code Correctness:
  ☐ No "ModuleNotFoundError" in logs
  ☐ No "ImportError" in logs
  ☐ backend.executor import works (based on earlier tests)

API Testing:
  ☐ /health endpoint returns {"status":"ok"}
  ☐ /execute endpoint accepts POST requests
  ☐ Code execution produces expected results

Frontend Integration:
  ☐ Frontend connects to API successfully
  ☐ Code Editor loads
  ☐ Execute button works without errors

All checkmarks present = ✅ DEPLOYMENT SUCCESS!

════════════════════════════════════════════════════════════════════════════════
⏱️  ESTIMATED TIMELINE
════════════════════════════════════════════════════════════════════════════════

Task                              Time        Running Total
────────────────────────────────────────────────────────────
1. Open Render dashboard          1 min       1 min
2. Select API service            30 sec      1:30
3. Clear build cache             30 sec      2:00
4. Trigger manual deploy         30 sec      2:30
5. Wait for build completion     3-5 min     5:30-7:30
6. Monitor logs                  30 sec      6:00-8:00
7. Test health endpoint          30 sec      6:30-8:30
8. Test execute endpoint         30 sec      7:00-9:00

Total: Approximately 7-9 minutes from start to complete validation

════════════════════════════════════════════════════════════════════════════════
📞 IF YOU NEED HELP
════════════════════════════════════════════════════════════════════════════════

Render Support: https://render.com/support
GitHub Status: https://www.githubstatus.com/
Check network connectivity: All services must be accessible

Common Render URLs:
  • Render Dashboard: https://dashboard.render.com
  • Service Logs: https://dashboard.render.com/codeflow-visualizer-api
  • Render Status: https://render.com/status

════════════════════════════════════════════════════════════════════════════════
🎯 FINAL CHECKLIST BEFORE STARTING
════════════════════════════════════════════════════════════════════════════════

Before you start the deployment:

  ☐ GitHub commit 95b2861 is pushed (verified earlier)
  ☐ render.yaml is updated in GitHub
  ☐ You have Render dashboard access
  ☐ You know your Render password (or have it)
  ☐ You're ready to wait 7-9 minutes for deployment
  ☐ You have curl or Postman to test endpoints
  ☐ You have this guide open for reference

Ready? Follow STEP 1 above to begin!

════════════════════════════════════════════════════════════════════════════════
