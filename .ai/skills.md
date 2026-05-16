# System Capability and Skills Matrix Specification
## Target Directory: `.ai/skills.md`

This file serves as a comprehensive technical execution registry for an AI Agent. It details every programming pattern, structural library, calculation logic, and architectural implementation technique needed to assemble the system without relying on guesswork or default behaviors.

---

## 1. Core Language & Execution Requirements

### 1.1 Python 3.10+ Advanced Runtime Context
*   **Asynchronous Context Management:** Ability to manage clean shutdowns for background execution scripts.
*   **Memory Footprint Optimization:** Structuring long-running data loops (`generator.py`) to prevent cumulative memory leak inflation using explicit scope isolation.
*   **Type Hinting Consistency:** Implementation of robust Type Hinting across all application layers using the `typing` module (`Dict`, `List`, `Tuple`, `Union`, `Any`).

---

## 2. Tier-Specific Engineering Capabilities

### 2.1 Data Simulation & Network Transmission (`data_generator/`)
The agent must possess the capability to build an deterministic live simulator script using the following micro-skills:
*   **Stateless Loop Scheduling:** Implementing controlled loop throttling via `time.sleep()` without blocking OS thread threads.
*   **Payload Serialization:** Utilizing Python's native `json` module to map runtime variables into structural strings without formatting errors.
*   **HTTP Protocol Compliance:** Constructing explicit `requests.post()` calls with custom headers (`"Content-Type": "application/json"`) and comprehensive exception handling blocks (`requests.exceptions.RequestException`, `ConnectionError`).

### 2.2 Micro-Services & Analytics Processing Layer (`middle_layer/`)
The agent must configure a reliable Flask application utilizing these micro-skills:
*   **In-Memory State Mutability:** Managing thread-safe append and read operations on active global Python data lists (`current_match_history`).
*   **Cross-Origin Resource Sharing (CORS):** Injecting explicit middleware declarations via `flask_cors.CORS` initialized to open origins (`resources={r"/*": {"origins": "*"}}`) to unblock cross-port communication from Streamlit.
*   **API Routing Architecture:** 
    *   Constructing a parsing route for `POST /update_match` that extracts JSON payloads using `request.get_json(force=True)`.
    *   Constructing a serialization route for `GET /get_analytics` returning structured payloads through `flask.jsonify()`.

### 2.3 Interface Generation & Real-Time Redrawing (`frontend/`)
The agent must build a responsive layout using these specific Streamlit interaction paradigms:
*   **Asynchronous Interface Instantiation:** Isolating UI elements into explicit `st.empty()` layout placeholders to rewrite content dynamically on every polling tick.
*   **Polling Optimization:** Implementing client-side polling loops that refresh charts using precise time interval ticks without invoking `st.rerun()`, avoiding screen-flickering side effects.
*   **Raw DOM and CDN Injections:** Utilizing `st.components.v1.html` to declare HTML/JS wrappers that safely fetch the Highcharts core script from the cloud distribution network (`https://code.highcharts.com/highcharts.js`).

---

## 3. Mathematical & Algorithmic Computation Skills

The agent must accurately translate statistical logic patterns into Python processing functions inside the analytical tier:

### 3.1 Sliding Window Aggregation (Momentum Calculation)
*   **Skill:** Processing data over a variable list index slice (`current_match_history[-30:]`).
*   **Logic Rule:** Iterating through the subset slice, cleanly accumulating `runs_on_this_ball` and counting occurrences where `is_wicket_this_ball == true`.

### 3.2 Positional Data Mapping (Matchup Analyzer)
*   **Skill:** Key-Value structural pair evaluation.
*   **Logic Rule:** Parsing string names against nested multidimensional lookups to instantly extract categorizations without falling back on default values.

### 3.3 Dynamic Boundary Truncation (Win Probability Calculator)
*   **Skill:** Implementing value restriction boundaries.
*   **Logic Rule:** Using bounding checks (`max(1, min(99, calculated_value))`) to keep floating-point outputs mathematically rational within sports parameters.

---

## 4. Highcharts Configuration Assembly

The agent must possess complete knowledge of Highcharts object architectures to dynamically construct specific layout strings. It needs to correctly write structural JavaScript strings for the following modules:

```text
Highcharts Component Tree Requirement:
├── Highcharts.chart()
    ├── chart: { type: 'spline' | 'area' | 'solidgauge' | 'column' }
    ├── title: { text: string }
    ├── xAxis: { categories: array | type: 'linear' }
    ├── yAxis: { min: number, max: number }
    └── series: [{ name: string, data: array }]