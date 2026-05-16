from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
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

@app.route('/get_analytics', methods=['GET'])
def get_analytics():
    if not current_match_history:
        return jsonify({"error": "No match data available yet."}), 400
        
    latest = current_match_history[-1]
    
    # 1. Momentum Tracking
    window = current_match_history[-30:]
    runs_in_window = sum(b.get("runs_on_this_ball", 0) for b in window)
    wickets_in_window = sum(1 for b in window if b.get("is_wicket_this_ball", False))
    momentum_score = (runs_in_window * 1.5) - (wickets_in_window * 10)
    
    # Matchup status
    if momentum_score >= 10:
        matchup_status = "Dominating"
    elif momentum_score <= -5:
        matchup_status = "Struggling"
    else:
        matchup_status = "Balanced"
        
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
    
    # 3. Boundary Dot Distribution (Counts or Percentages, returning percentages based on mock data)
    dots = sum(1 for b in current_match_history if b["runs_on_this_ball"] == 0 and not b["is_wicket_this_ball"])
    boundaries = sum(1 for b in current_match_history if b["runs_on_this_ball"] in [4, 6])
    singles = sum(1 for b in current_match_history if b["runs_on_this_ball"] in [1, 2, 3])
    
    total_balls = len(current_match_history)
    dots_pct = round((dots / total_balls) * 100, 1) if total_balls else 0.0
    boundaries_pct = round((boundaries / total_balls) * 100, 1) if total_balls else 0.0
    singles_pct = round((singles / total_balls) * 100, 1) if total_balls else 0.0
    
    # 4. Phase Performance
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
        # run rate calculation
        phases[p]["run_rate"] = round((phases[p]["runs"] / (balls / 6.0)), 1) if balls > 0 else 0.0
        del phases[p]["balls"]
        
    # 5. Player Impact Rating (Calculated only for currently active players across the history)
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
            "win_probability_history": win_prob_history,
            "boundary_dot_distribution": {
                "dots": dots_pct,
                "singles": singles_pct,
                "boundaries": boundaries_pct
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
