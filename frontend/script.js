document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    fetchDashboardMeta();
    setInterval(fetchLiveAnalytics, 2000);
});

let charts = {};

function initCharts() {
    const commonOptions = {
        chart: { type: 'pie', backgroundColor: 'transparent' },
        title: { text: null },
        credits: { enabled: false },
        plotOptions: {
            pie: {
                innerSize: '65%',
                dataLabels: { enabled: false },
                showInLegend: true
            }
        },
        legend: {
            enabled: true,
            itemStyle: { fontSize: '10px', color: '#64748b', fontWeight: '500' },
            symbolPadding: 4,
            margin: 0
        }
    };

    charts.winProb = Highcharts.chart('chart-win-prob', Highcharts.merge(commonOptions, {
        series: [{ name: 'Prob %', data: [['Team A', 50], ['Team B', 50]], colors: ['#2563eb', '#f97316'] }]
    }));
    
    charts.paceOfPlay = Highcharts.chart('chart-pace-of-play', Highcharts.merge(commonOptions, {
        series: [{ name: 'Pct', data: [['Action', 50], ['Idle', 50]], colors: ['#22c55e', '#ef4444'] }]
    }));

    charts.scoringStrategy = Highcharts.chart('chart-scoring-strategy', Highcharts.merge(commonOptions, {
        series: [{ name: 'Pct', data: [['Safe', 50], ['Big Hits', 50]], colors: ['#3b82f6', '#8b5cf6'] }]
    }));

    charts.matchProgression = Highcharts.chart('chart-match-progression', Highcharts.merge(commonOptions, {
        series: [{ name: 'Pct', data: [['Completed', 0], ['Remaining', 100]], colors: ['#eab308', '#cbd5e1'] }]
    }));
}

function fetchDashboardMeta() {
    fetch('/get_dashboard_meta')
        .then(res => res.json())
        .then(data => {
            // Populate Records Card
            const rec = data.records;
            const recordsHtml = `
                <h3 style="color:var(--primary);">${rec.title}</h3>
                <p style="font-size:0.8rem; color:var(--text-muted);">${rec.team}</p>
                <div style="display:flex; justify-content:space-between; margin-top:10px;">
                    <div style="width: 55%;">
                        <div class="orange-cap-bg">
                            <div class="orange-cap-info">
                                <h4>${rec.stat}</h4>
                                <p>${rec.highlight}</p>
                            </div>
                        </div>
                    </div>
                    <div style="width: 40%; display:flex; flex-direction:column; justify-content:center; gap:8px;">
                        ${rec.mini_list.map(m => `
                            <div style="display:flex; align-items:center; gap:8px;">
                                <img src="${m.img}" style="width:24px; height:24px; border-radius:50%;">
                                <div>
                                    <p style="font-size:0.75rem; font-weight:600;">${m.name}</p>
                                    <p style="font-size:0.65rem; color:var(--text-muted);">${m.stat}</p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
            document.getElementById('records-card').innerHTML = recordsHtml;

            // Populate Squads Table
            const squadsTbody = document.querySelector('#squads-table tbody');
            squadsTbody.innerHTML = data.squads.map(s => `
                <tr>
                    <td><img src="${s.image}"></td>
                    <td style="font-weight:500;">${s.PlayerName}</td>
                    <td>${s.Team}</td>
                    <td>${s.Category}</td>
                    <td style="color:var(--text-muted);">${s.Type}</td>
                </tr>
            `).join('');

            // Populate Schedule
            const sched = data.schedule;
            document.getElementById('schedule-card').innerHTML = `
                <h3>Schedule</h3>
                <div style="margin-top:12px; border:1px solid var(--border); padding:16px; border-radius:12px;">
                    <p class="date">${sched.date}</p>
                    <p class="match-det">${sched.match}</p>
                    <div class="teams" style="margin-top:12px;">
                        <p style="margin-bottom:8px;">🏏 ${sched.team1}</p>
                        <p>🏏 ${sched.team2}</p>
                    </div>
                    <p class="result" style="margin-top:16px; font-weight:500;">${sched.result}</p>
                </div>
            `;

            // Populate Points Table
            const pointsTbody = document.querySelector('#points-table tbody');
            pointsTbody.innerHTML = data.points_table.map(p => `
                <tr>
                    <td><div class="dot blue" style="width:20px;height:20px;"></div></td>
                    <td style="font-weight:600;">${p.team}</td>
                    <td>${p.m}</td>
                    <td>${p.w}</td>
                    <td>${p.l}</td>
                    <td style="font-weight:600;">${p.pt}</td>
                </tr>
            `).join('');
        });
}

function fetchLiveAnalytics() {
    fetch('/get_analytics')
        .then(res => {
            if(!res.ok) throw new Error('waiting');
            return res.json();
        })
        .then(data => {
            const sum = data.live_summary;
            const a = data.analytics;

            // Update UI text
            document.getElementById('match-info-text').innerText = `RESULT - T20 - Over: ${sum.over}`;
            document.getElementById('team-a-score').innerText = sum.score;
            document.getElementById('live-status-text').innerText = `Batting: ${sum.batter} | Bowling: ${sum.bowler} | Status: ${a.matchup_status}`;

            // Update Charts Data
            charts.winProb.series[0].setData([
                ['Team A', a.win_probability.team_a],
                ['Team B', a.win_probability.team_b]
            ]);

            charts.paceOfPlay.series[0].setData([
                ['Action', a.basic_analytics.pace_of_play.action_pct || 0.1], 
                ['Idle', a.basic_analytics.pace_of_play.idle_pct || 0.1]
            ]);

            charts.scoringStrategy.series[0].setData([
                ['Safe', a.basic_analytics.scoring_strategy.safe_pct || 0.1],
                ['Big Hits', a.basic_analytics.scoring_strategy.big_hit_pct || 0.1]
            ]);

            charts.matchProgression.series[0].setData([
                ['Completed', a.basic_analytics.match_progression.completed_pct || 0.1],
                ['Remaining', a.basic_analytics.match_progression.remaining_pct || 0.1]
            ]);
        })
        .catch(err => {
            document.getElementById('live-status-text').innerText = 'Waiting for match simulation...';
        });
}
