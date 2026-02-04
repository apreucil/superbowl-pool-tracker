from flask import Flask, render_template, jsonify
from flask_cors import CORS
import csv
import requests
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Store pool data and game state
pool_data = []
quarterly_winners = {"Q1": None, "Q2": None, "Q3": None, "Q4": None}
last_quarter = 0

def load_pool_data():
    """Load CSV data into memory"""
    global pool_data
    pool_data = []
    try:
        with open('TenDollarPool2026.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pool_data.append({
                    'name': row['Name'],
                    'seahawks': int(row['Seahawks']),
                    'patriots': int(row['Patriots'])
                })
    except Exception as e:
        print(f"Error loading CSV: {e}")

def get_live_score():
    """Fetch live Super Bowl score from ESPN API"""
    try:
        # Fetch NFL games for today
        response = requests.get(
            'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard',
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            
            # Find Super Bowl game (usually last game or look for playoff indicator)
            for event in events:
                if 'Super Bowl' in event.get('name', '') or event.get('season', {}).get('type') == 3:
                    competitions = event.get('competitions', [])
                    if competitions:
                        comp = competitions[0]
                        competitors = comp.get('competitors', [])
                        
                        if len(competitors) == 2:
                            # Assuming first is home, second is away
                            # Determine which is Seahawks and which is Patriots
                            score_data = {}
                            for competitor in competitors:
                                team_name = competitor.get('team', {}).get('name', '')
                                score = int(competitor.get('score', 0))
                                if 'Seahawks' in team_name:
                                    score_data['seahawks'] = score
                                elif 'Patriots' in team_name:
                                    score_data['patriots'] = score
                                elif competitor.get('homeAway') == 'home':
                                    score_data['team1'] = score
                                    score_data['team1_name'] = team_name
                                else:
                                    score_data['team2'] = score
                                    score_data['team2_name'] = team_name
                            
                            if 'seahawks' in score_data and 'patriots' in score_data:
                                return score_data
            
            # Fallback: return first game in scoreboard
            if events and events[0].get('competitions'):
                comp = events[0]['competitions'][0]
                competitors = comp.get('competitors', [])
                if len(competitors) >= 2:
                    return {
                        'team1': int(competitors[0].get('score', 0)),
                        'team2': int(competitors[1].get('score', 0)),
                        'team1_name': competitors[0].get('team', {}).get('name', 'Team 1'),
                        'team2_name': competitors[1].get('team', {}).get('name', 'Team 2')
                    }
        
        return None
    except Exception as e:
        print(f"Error fetching score: {e}")
        return None

def calculate_winners(seahawks_score, patriots_score):
    """Calculate current winner(s) based on last digits"""
    seahawks_last = seahawks_score % 10
    patriots_last = patriots_score % 10
    
    winners = []
    for person in pool_data:
        if person['seahawks'] == seahawks_last and person['patriots'] == patriots_last:
            winners.append(person['name'])
    
    return winners

def get_quarter(score_data):
    """Estimate current quarter based on score progression"""
    # This is a simple heuristic - in production you'd get this from the API
    if 'period' in score_data:
        return score_data['period']
    return 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/score')
def api_score():
    """Return current score and winners"""
    score = get_live_score()
    
    if not score:
        return jsonify({
            'error': 'Could not fetch score',
            'current_winners': [],
            'seahawks': 0,
            'patriots': 0
        }), 404
    
    seahawks = score.get('seahawks', 0)
    patriots = score.get('patriots', 0)
    
    winners = calculate_winners(seahawks, patriots)
    
    return jsonify({
        'seahawks': seahawks,
        'patriots': patriots,
        'seahawks_last_digit': seahawks % 10,
        'patriots_last_digit': patriots % 10,
        'current_winners': winners,
        'timestamp': datetime.now().isoformat(),
        'quarterly_winners': quarterly_winners
    })

@app.route('/api/all-players')
def api_all_players():
    """Return all players and their pool numbers"""
    return jsonify(pool_data)

if __name__ == '__main__':
    load_pool_data()
    app.run(debug=False, port=5000)
