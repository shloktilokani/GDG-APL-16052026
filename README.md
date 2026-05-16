# 🏏 IPL Live Analytics Dashboard

A high-fidelity, real-time analytics dashboard for the Indian Premier League (IPL). This project transitions away from generic frameworks like Streamlit to a custom-built, native web architecture designed for precision, visual excellence, and advanced data-driven insights.

---

## 🚀 Project Understanding

The **IPL Live Analytics Dashboard** is a 3-tier decoupled application that processes authentic match data to provide deep analytical insights rather than simple statistics. It is designed to be **presentation-ready**, focusing on universally understood metrics that track the flow, strategy, and progression of a match.

### Key Features
- **Authentic Data Stream**: Uses real-world IPL ball-by-ball data from Cricsheet to simulate a live match feed.
- **Basic Analysis Focus**: Visualizes concepts like "Pace of Play" (Action vs. Idle) and "Scoring Strategy" (Safe vs. Aggressive) that are intuitive for non-sport audiences.
- **High-Fidelity UI**: A custom CSS Grid layout with glassmorphism aesthetics and dynamic Highcharts visualizations.

---

## 🛠 Tech Stack

### 🔹 Backend (The Analytical Engine)
- **Python 3.10+**: Core logic.
- **Flask**: Lightweight API server and static file hosting.
- **Pandas**: Used for high-speed, vectorized data slicing and analytical calculations.
- **Cricsheet JSON**: Authentic data source for ball-by-ball match history.

### 🔹 Frontend (The Visualization Layer)
- **HTML5 & Semantic Tags**: Structural integrity and SEO.
- **Vanilla CSS3**: Custom design system using CSS Grid and Flexbox for a responsive, premium look.
- **Javascript (ES6+)**: Handles the 2-second polling loop and DOM manipulation.
- **Highcharts.js**: Powers the dynamic, interactive donut visualizations and legends.

---

## 🧠 The `.ai/` Control Center (AI-First Development)

The `.ai/` directory is the most critical part of this codebase. It serves as the **Contextual Brain** for the AI coding assistant, ensuring that the project remains synchronized, rule-abiding, and architecturally consistent.

| File | Purpose | Weight in Development |
| :--- | :--- | :--- |
| **`settings.json`** | **The Manifest**: Defines technical constraints, port assignments, and dependency rules. It prevents the AI from deviating from the chosen tech stack. | 🔴 High |
| **`memory.md`** | **Long-term Memory**: Tracks architectural pivots, design decisions, and system metrics. It ensures the "Why" behind every change is preserved. | 🟠 Medium |
| **`handoff.md`** | **State Transfer**: The most vital file for continuity. It contains the exact technical state, pending blockers, and "Next Steps" for the next agent session. | 🔴 Critical |
| **`task.json`** | **The Ledger**: A granular TODO list that tracks progress at a component level. No task is considered "Done" until the agent updates this ledger. | 🟡 Medium |
| **`mock_data.json`** | **Schema Standard**: Defines the expected JSON payloads for the API, ensuring frontend/backend contract compliance. | 🟢 Low |

---

## ⚙️ How It Works

1. **Data Ingestion**: The backend reads a real IPL match JSON file and simulates a live stream by releasing one ball every 2 seconds into an in-memory queue.
2. **Analytical Processing**: Every time the frontend polls the API, the backend uses **Pandas** to calculate the latest match state (e.g., % of action plays, % of runs from boundaries).
3. **Dynamic Rendering**: The frontend fetches this JSON and uses Javascript to update the Highcharts series objects and DOM elements instantly without a page reload.

---

## 🏃 Running the Project

1. **Activate Environment**:
   ```bash
   source .myenv/bin/activate
   ```
2. **Start the Middle Layer**:
   ```bash
   python middle_layer/app.py
   ```
3. **Access the Dashboard**:
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

*This project is built using Antigravity AI, following strict agentic coding principles.*
