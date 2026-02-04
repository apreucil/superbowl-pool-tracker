# Super Bowl Pool 2026 - Live Tracker

A real-time web application that tracks the Super Bowl pool and displays current winners every 30 seconds.

## Features

- 🏈 **Live Score Updates** - Fetches Super Bowl scores every 30 seconds
- 🏆 **Real-time Winner Tracking** - Shows who's currently winning the pool
- 📊 **Quarterly Winners** - Tracks winners at the end of each quarter
- 📱 **Mobile Friendly** - Works great on phones and tablets
- 🎯 **Automatic Score Matching** - Matches last digits of scores to pool entries

## How It Works

Players pick the last digit of each team's score. For example, if the Seahawks score 14 and Patriots score 17, the winning numbers are 4 and 7. Anyone who picked 4 and 7 wins that round!

## Deployment Options (All Free)

### Option 1: Render.com (Recommended)

1. Create a free account at [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn app:app`
6. Deploy!

### Option 2: Railway

1. Create a free account at [railway.app](https://railway.app)
2. Create a new project → Deploy from GitHub
3. Add environment variables if needed
4. Railway auto-detects Flask and deploys

### Option 3: Replit

1. Create a free account at [replit.com](https://replit.com)
2. Click "Create Repl" → Upload this project
3. Click "Run" - it will auto-detect and run
4. Share the link with your pool members

### Option 4: PythonAnywhere

1. Create a free account at [pythonanywhere.com](https://pythonanywhere.com)
2. Upload files via web interface
3. Configure a web app with Flask
4. Set up a scheduled task for periodic updates

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Visit http://localhost:5000
```

## Files

- `app.py` - Flask backend that fetches scores and calculates winners
- `templates/index.html` - Responsive web interface
- `TenDollarPool2026.csv` - Pool data with player entries
- `requirements.txt` - Python dependencies
- `Procfile` - For Heroku/Render deployment

## Accessing from Phone

Once deployed:
1. Copy the deployment URL
2. Share with pool members via text/email
3. Everyone can access the live tracker from their browser
4. No app installation needed!

## Score API

The app uses the ESPN API to fetch live NFL scores. It looks for Super Bowl games and extracts:
- Current score for each team
- Last digits for pool matching
- Game period/quarter

## Notes

- Updates happen every 30 seconds (adjustable in frontend)
- Quarterly winners are stored in memory (add database for persistence)
- Works during the game - no functionality before kickoff
