```markdown
# Comprehensive System Handoff Specification
## Target Directory: `.ai/Handoff.md`

This file provides the complete, unambiguous system specification for an AI Agent to architect, compute, and render the IPL Live Analytics Dashboard without relying on any external assumptions or guesswork.

---

## 1. Executive Summary & Objective
The objective of this system is to ingest raw, simulated ball-by-ball cricket data and translate it into intuitive, highly visual narrative insights tailored specifically for casual sports fans. The system completely bypasses dense tabular data statistics in favor of graphical storytelling, trend lines, color-coded matchups, and gamified performance scores. 

---

## 2. Architecture Overview
The system implements a decoupled, local three-tier architecture to ensure fast updates, zero API rate-limiting issues during development, and a clean separation of concerns.

```text
[Data Generator (generator.py)] 
             │
             ▼ (HTTP POST JSON / Ingest API)
[Middle Layer Analytics Engine (app.py)] 
             │
             ▼ (HTTP GET JSON / Clean Analytics API)
[Frontend Presentation Layer (dashboard.py)]

```

### Tier 1: Data Generator (`data_generator/generator.py`)

* **Role:** Background simulator running on an infinite execution loop.
* **Behavior:** Emits a mock ball-by-ball JSON event every 5 seconds. It increments match variables logically (e.g., overs increment from 0.1 to 20.0, score increases based on ball outcome).
* **State:** Keeps track of current overs, cumulative score, wickets, target, and currently active batters/bowlers to ensure data sequence coherence.

### Tier 2: Middle Layer (`middle_layer/app.py`)

* **Role:** Stateless processing engine and data aggregator built with Flask.
* **State Management:** Holds a global list of received ball events in-memory (`current_match_history = []`). No database layer is utilized.
* **Calculations Engine:** Processes raw numbers into 6 discrete analytical data objects required by the frontend configuration arrays.

### Tier 3: Frontend Interface (`frontend/index.html` & `frontend/script.js`)

* **Role:** Responsive user interface built with Vanilla HTML/CSS/JS and Highcharts.js/Chart.js.
* **Polling Loop:** A JavaScript `setInterval` function fetching JSON from `/get_analytics` every 2 seconds, populating the DOM and dynamically updating the charts.

---

## 3. Strict Data Protocols

### 3.1 Ingestion Payload Schema (Generator -> Middle Layer)

Every POST request transmitted to `http://127.0.0.1:5000/update_match` must strictly adhere to the following JSON footprint:

```json
{
  "match_id": 101,
  "inning": 1,
  "over": 14.2,
  "current_score": 115,
  "wickets": 3,
  "target_score": 185, 
  "balls_remaining": 34,
  "runs_on_this_ball": 4,
  "is_wicket_this_ball": false,
  "extra_runs": 0,
  "current_batter": "Virat Kohli",
  "current_bowler": "Jasprit Bumrah"
}

```

### 3.2 Analytical Output Schema (Middle Layer -> Frontend)

The response from `GET http://127.0.0.1:5000/get_analytics` must compile all computations into a structured payload mapping directly to Highcharts series definitions:

```json
{
  "live_summary": {
    "score": "115/3",
    "over": 14.2,
    "batter": "Virat Kohli",
    "bowler": "Jasprit Bumrah"
  },
  "analytics": {
    "momentum_score": 15,
    "momentum_history": [[1.0, 5], [2.0, -2], [14.2, 15]],
    "matchup_status": "Struggling",
    "win_probability": {
      "team_a": 62.5,
      "team_b": 37.5
    },
    "boundary_dot_distribution": {
      "dots": 40,
      "singles": 35,
      "boundaries": 25
    },
    "milestone_probability": {
      "fifty_prob": 82.5,
      "century_prob": 12.0
    },
    "milestones_tracked": {
      "fifties": 2,
      "centuries": 0
    },
    "over_wicket_ratio": {
      "overs_pct": 71.0,
      "wickets_pct": 30.0
    },
    "phase_performance": {
      "powerplay": {"runs": 45, "wickets": 1, "run_rate": 7.5},
      "middle_overs": {"runs": 70, "wickets": 2, "run_rate": 8.2},
      "death_overs": {"runs": 0, "wickets": 0, "run_rate": 0.0}
    },
    "player_impact": {
      "batter_score": 78,
      "bowler_score": 42
    }
  }
}

```

---

## 4. Analytical Computation Logic (Middle Layer Specs)

The Middle Layer must execute the following mathematical formulas precisely upon receiving each ball:

1. **Momentum Tracking:** Calculated over a moving window of the last 30 ball entries (5 overs).

$$\text{Momentum} = (\text{Runs scored in window} \times 1.5) - (\text{Wickets lost in window} \times 10)$$


2. **Predictive Win Probability:**

$$\text{Run Rate Required (RRR)} = \frac{\text{Runs Needed}}{\text{Balls Remaining} / 6}$$


$$\text{Win Probability \%} = 100 - (\text{RRR} \times 6.5) - (\text{Wickets Lost} \times 7.5)$$



*(Bounded strictly between 1% and 99% until match termination).*
3. **Player Impact Rating:**
* **Batter:** $+10$ points per boundary, $+2$ per run, $-5$ per dot ball.
* **Bowler:** $+25$ points per wicket, $+4$ per dot ball, $-3$ per run conceded.



---

## 5. UI Layout Blueprint

The HTML layout must be a CSS Grid-based 3-column design matching the provided mockup:

* **Top Bar:** Logo, Navigation links (Home, Overview, Points Table, Squads).
* **Left Column:** Live Fixture block. A 2x2 grid of Donut charts (Milestone Probabilities, Milestone Trackers, Ov vs W, Boundaries).
* **Middle Column:** Player Records Card highlighting a specific stat (e.g., Orange Cap). Squads tabular list.
* **Right Column:** Schedule Card. Points Table.

```

```