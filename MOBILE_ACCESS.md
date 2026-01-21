# 📱 Mobile Access Guide - Pixel 10

## Quick Start Instructions

### Step 1: Find Your Computer's IP Address

**On Linux/Mac:**
```bash
ip addr show | grep "inet " | grep -v 127.0.0.1
# or
ifconfig | grep "inet " | grep -v 127.0.0.1
# or
hostname -I
```

**On Windows:**
```bash
ipconfig
```

Look for your local IP address (usually starts with `192.168.x.x` or `10.0.x.x`)

Example: `192.168.1.100`

### Step 2: Start the Servers

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

You should see output like:
```
  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.1.100:5173/
```

### Step 3: Connect Your Phone

1. **Ensure your Pixel 10 is on the same WiFi network** as your computer
2. Open Chrome or your browser on your Pixel 10
3. Navigate to: `http://YOUR_IP_ADDRESS:5173`
   - Example: `http://192.168.1.100:5173`

### Step 4: Use the App

You should now see the Portfolio Advisor login page on your phone!

## Troubleshooting

### Can't Connect?

1. **Firewall:** Make sure your firewall allows connections on ports 8000 and 5173

   **Linux (UFW):**
   ```bash
   sudo ufw allow 8000
   sudo ufw allow 5173
   ```

   **Windows:** Add inbound rules for ports 8000 and 5173

2. **Same Network:** Verify both devices are on the same WiFi network

3. **Ping Test:** From your phone's browser, try accessing:
   - `http://YOUR_IP:8000/health` - Should show `{"status": "healthy"}`

4. **CORS Issues:** The backend is configured to allow CORS, but if you have issues, update `backend/app/core/config.py`:
   ```python
   ALLOWED_ORIGINS: List[str] = ["http://YOUR_IP:5173", "http://localhost:5173"]
   ```

## Using ngrok (Alternative - Internet Access)

If you want to access it from anywhere (not just local network):

1. **Install ngrok:** https://ngrok.com/download

2. **Start backend tunnel:**
   ```bash
   ngrok http 8000
   ```
   Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

3. **Update frontend API URL:**
   Edit `frontend/src/services/api.js`:
   ```javascript
   const API_BASE_URL = 'https://abc123.ngrok.io'
   ```

4. **Start frontend tunnel:**
   ```bash
   ngrok http 5173
   ```
   Copy the HTTPS URL and open it on your phone!

## Performance Tips for Mobile

The app is responsive and should work well on your Pixel 10:
- All charts are touch-friendly
- Navigation drawer works with swipe gestures
- Forms are optimized for mobile keyboards
- Material-UI components are mobile-first

## Security Note

When accessing over local network:
- ✅ Safe for local testing
- ❌ Don't expose to the internet without proper security
- ❌ Don't use real financial data in development

For production deployment, use HTTPS and proper hosting (Vercel, Netlify, etc.)
