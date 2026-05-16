from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend')))
# Integrate flask_cors globally to allow cross-origin requests
CORS(app, resources={r"/*": {"origins": "*"}})

# In-memory mutable lists
current_match_history = []
momentum_history_array = []

def get_phase(over):
    if over <= 6.0:
        return "powerplay"
    elif over <= 15.0:
        return "middle_overs"
    else:
        return "death_overs"

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

@app.route('/update_match', methods=['POST'])
def update_match():
    data = request.get_json(force=True)
    current_match_history.append(data)
    
    # Calculate Momentum for this ball to save in history
    window = current_match_history[-30:]
    runs_in_window = sum(b.get("runs_on_this_ball", 0) for b in window)
    wickets_in_window = sum(1 for b in window if b.get("is_wicket_this_ball", False))
    
    momentum = (runs_in_window * 1.5) - (wickets_in_window * 10)
    over = data.get("over", 0.0)
    
    # Append to momentum history
    momentum_history_array.append([over, momentum])
    
    return jsonify({"status": "success"}), 201

@app.route('/get_dashboard_meta', methods=['GET'])
def get_dashboard_meta():
    return jsonify({
        "records": {
            "title": "Records",
            "team": "Royal Challengers Bangalore",
            "player_name": "Virat Kohli",
            "image_url": "https://i.pravatar.cc/150?img=11", 
            "highlight": "Orange Cap",
            "stat": "8004",
            "mini_list": [
                {"name": "Alzarri Joseph", "stat": "Best Bowl Figures", "img": "https://i.pravatar.cc/50?img=12"},
                {"name": "Bhuvneshwar", "stat": "Most Dots", "img": "https://i.pravatar.cc/50?img=13"},
                {"name": "Chris Gayle", "stat": "Fastest 100", "img": "https://i.pravatar.cc/50?img=14"}
            ]
        },
        "squads": [
            {"image": "https://i.pravatar.cc/50?img=15", "PlayerName": "Mayank Yadav", "Team": "LSG", "Category": "Bowler", "Type": "Bowler", "PlayerURL": "#"},
            {"image": "https://i.pravatar.cc/50?img=16", "PlayerName": "Yuzvendra Chahal", "Team": "PBKS", "Category": "Bowler", "Type": "Bowler", "PlayerURL": "#"},
            {"image": "https://i.pravatar.cc/50?img=17", "PlayerName": "Mohit Sharma", "Team": "DC", "Category": "Bowler", "Type": "Bowler", "PlayerURL": "#"},
            {"image": "https://i.pravatar.cc/50?img=18", "PlayerName": "Jitesh Sharma", "Team": "RCB", "Category": "WK-Batter", "Type": "Wicketkeeper Batter", "PlayerURL": "#"}
        ],
        "schedule": {
            "date": "Sat, 22 Mar '25",
            "match": "1st Match (N) • Eden Gardens",
            "team1": "Kolkata Knight Riders",
            "team2": "Royal Challengers Bangalore",
            "result": "RCB won by 7 wickets (with 22 balls remaining)"
        },
        "points_table": [
            {"team": "DC", "m": 3, "w": 3, "l": 0, "pt": 6},
            {"team": "RR", "m": 4, "w": 2, "l": 2, "pt": 4},
            {"team": "GT", "m": 4, "w": 3, "l": 1, "pt": 6},
            {"team": "PBKS", "m": 4, "w": 3, "l": 1, "pt": 6},
            {"team": "RCB", "m": 4, "w": 3, "l": 1, "pt": 6}
        ]
    })

@app.route('/get_analytics', methods=['GET'])
def get_analytics():
    if not current_match_history:
        return jsonify({"error": "No match data available yet."}), 400
        
    latest = current_match_history[-1]
    df = pd.DataFrame(current_match_history)
    
    # 1. Momentum Tracking
    momentum_score = momentum_history_array[-1][1] if momentum_history_array else 0
    matchup_status = "Dominating" if momentum_score >= 10 else "Struggling" if momentum_score <= -5 else "Balanced"
        
    # 2. Predictive Win Probability (Current and History)
    win_prob_history = []
    for b in current_match_history:
        r_needed = max(0, b["target_score"] - b["current_score"])
        b_rem = b["balls_remaining"]
        w_lost = b["wickets"]
        if b_rem > 0 and r_needed > 0:
            rate = r_needed / (b_rem / 6.0)
            wp = 100 - (rate * 6.5) - (w_lost * 7.5)
        elif r_needed <= 0:
            wp = 99.0
        else:
            wp = 1.0
        wp = max(1.0, min(99.0, wp))
        win_prob_history.append([b["over"], round(wp, 1)])
        
    latest_prob = win_prob_history[-1][1] if win_prob_history else 50.0
    team_a_prob = latest_prob
    team_b_prob = round(100.0 - team_a_prob, 1)
    
    # 3. Pace of Play: Action vs Idle
    total_balls = len(df)
    dots = len(df[df["runs_on_this_ball"] == 0])
    action_plays = total_balls - dots
    if total_balls > 0:
        action_pct = round((action_plays / total_balls) * 100, 1)
        idle_pct = round((dots / total_balls) * 100, 1)
    else:
        action_pct = idle_pct = 50.0

    # 4. Scoring Strategy: Safe vs Big Hits
    singles = len(df[(df["runs_on_this_ball"] >= 1) & (df["runs_on_this_ball"] <= 3)])
    boundaries = len(df[(df["runs_on_this_ball"] == 4) | (df["runs_on_this_ball"] == 6)])
    total_scoring_plays = singles + boundaries
    if total_scoring_plays > 0:
        safe_pct = round((singles / total_scoring_plays) * 100, 1)
        big_hit_pct = round((boundaries / total_scoring_plays) * 100, 1)
    else:
        safe_pct = big_hit_pct = 50.0

    # 5. Match Progression
    max_overs = 20.0
    completed_overs = latest["over"]
    prog_pct = min(100.0, (completed_overs / max_overs) * 100)
    remain_pct = round(100.0 - prog_pct, 1)
    prog_pct = round(prog_pct, 1)
    
    # 6. Phase Performance
    phases = {
        "powerplay": {"runs": 0, "wickets": 0, "balls": 0},
        "middle_overs": {"runs": 0, "wickets": 0, "balls": 0},
        "death_overs": {"runs": 0, "wickets": 0, "balls": 0}
    }
    for b in current_match_history:
        phase = get_phase(b["over"])
        phases[phase]["runs"] += b["runs_on_this_ball"]
        if b["is_wicket_this_ball"]:
            phases[phase]["wickets"] += 1
        phases[phase]["balls"] += 1
        
    for p in phases:
        balls = phases[p]["balls"]
        phases[p]["run_rate"] = round((phases[p]["runs"] / (balls / 6.0)), 1) if balls > 0 else 0.0
        del phases[p]["balls"]
        
    # 7. Player Impact Rating
    current_batter = latest["current_batter"]
    current_bowler = latest["current_bowler"]
    batter_score = 0
    bowler_score = 0
    for b in current_match_history:
        if b["current_batter"] == current_batter:
            if b["runs_on_this_ball"] in [4, 6]:
                batter_score += 10
            elif b["runs_on_this_ball"] == 0 and not b["is_wicket_this_ball"]:
                batter_score -= 5
            else:
                batter_score += (b["runs_on_this_ball"] * 2)
        if b["current_bowler"] == current_bowler:
            if b["is_wicket_this_ball"]:
                bowler_score += 25
            elif b["runs_on_this_ball"] == 0 and not b["is_wicket_this_ball"]:
                bowler_score += 4
            else:
                bowler_score -= (b["runs_on_this_ball"] * 3)
                
    response = {
        "live_summary": {
            "score": f"{latest['current_score']}/{latest['wickets']}",
            "over": latest["over"],
            "batter": current_batter,
            "bowler": current_bowler
        },
        "analytics": {
            "momentum_score": momentum_score,
            "momentum_history": momentum_history_array,
            "matchup_status": matchup_status,
            "win_probability": {
                "team_a": team_a_prob,
                "team_b": team_b_prob
            },
            "basic_analytics": {
                "pace_of_play": {
                    "action_pct": action_pct,
                    "idle_pct": idle_pct
                },
                "scoring_strategy": {
                    "safe_pct": safe_pct,
                    "big_hit_pct": big_hit_pct
                },
                "match_progression": {
                    "completed_pct": prog_pct,
                    "remaining_pct": remain_pct
                }
            },
            "phase_performance": phases,
            "player_impact": {
                "batter_score": batter_score,
                "bowler_score": bowler_score
            }
        }
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)
