import time
import json
import random
import requests

BATTERS = [
    "Virat Kohli", "Rohit Sharma", "Suryakumar Yadav", "Hardik Pandya", 
    "Rishabh Pant", "Ravindra Jadeja", "MS Dhoni", "Jasprit Bumrah", 
    "Mohammed Shami", "Yuzvendra Chahal", "Kuldeep Yadav"
]
BOWLERS = [
    "Mitchell Starc", "Pat Cummins", "Trent Boult", "Rashid Khan", 
    "Kagiso Rabada", "Anrich Nortje"
]

def format_over(balls_bowled):
    overs = balls_bowled // 6
    balls = balls_bowled % 6
    return round(overs + (balls / 10), 1)

def run_simulation():
    match_id = 101
    inning = 1
    target_score = 185
    
    current_score = 0
    wickets = 0
    balls_bowled = 0
    total_balls = 120
    
    striker_idx = 0
    non_striker_idx = 1
    
    bowler_index = 0
    current_bowler = BOWLERS[bowler_index]
    
    print("Starting IPL Match Simulator...")
    
    while balls_bowled < total_balls and wickets < 10:
        # Sleep for 5 seconds as specified
        time.sleep(5)
        
        balls_bowled += 1
        balls_remaining = total_balls - balls_bowled
        
        # Simulate ball outcome
        # 5% chance of wicket, else random runs
        is_wicket_this_ball = False
        runs_on_this_ball = 0
        
        outcome_prob = random.random()
        if outcome_prob < 0.05:
            is_wicket_this_ball = True
            wickets += 1
            # Next batter comes to crease
            striker_idx = max(striker_idx, non_striker_idx) + 1
        else:
            runs_on_this_ball = random.choice([0, 0, 1, 1, 1, 2, 2, 3, 4, 4, 6])
            current_score += runs_on_this_ball
            # Swap strike if odd runs
            if runs_on_this_ball % 2 != 0:
                striker_idx, non_striker_idx = non_striker_idx, striker_idx

        # Ensure we don't go out of bounds on batters
        current_batter = BATTERS[min(striker_idx, len(BATTERS)-1)]
        over_formatted = format_over(balls_bowled)
        
        # Payload construction
        payload = {
            "match_id": match_id,
            "inning": inning,
            "over": over_formatted,
            "current_score": current_score,
            "wickets": wickets,
            "target_score": target_score,
            "balls_remaining": balls_remaining,
            "runs_on_this_ball": runs_on_this_ball,
            "is_wicket_this_ball": is_wicket_this_ball,
            "extra_runs": 0,
            "current_batter": current_batter,
            "current_bowler": current_bowler
        }
        
        try:
            response = requests.post(
                "http://127.0.0.1:5000/update_match",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            print(f"[SUCCESS] Ball {balls_bowled} ({over_formatted}) | Score: {current_score}/{wickets} | Target: {target_score} | Wicket: {is_wicket_this_ball} | Runs: {runs_on_this_ball} | Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to send payload. Middle layer might not be running: {e}")
            
        # Swap bowler and strike at the end of the over
        if balls_bowled % 6 == 0:
            bowler_index = (bowler_index + 1) % len(BOWLERS)
            current_bowler = BOWLERS[bowler_index]
            striker_idx, non_striker_idx = non_striker_idx, striker_idx
            
    print("Innings complete.")

if __name__ == "__main__":
    run_simulation()
