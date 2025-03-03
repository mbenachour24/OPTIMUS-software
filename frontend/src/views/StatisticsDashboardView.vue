<template>
  <div>
    <header>
      <h1>Optimus - Statistics Dashboard</h1>
    </header>

    <aside class="sidebar">
      <h3>Navigation</h3>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
      <h3>Systems</h3>
      <ul>
        <li><a href="/judicial">Judicial System</a></li>
        <li><a href="/political">Political System</a></li>
        <li><a href="/cases">View Cases</a></li>
        <li><a href="/norms">View Norms</a></li>
      </ul>
      <h3>Analytics</h3>
      <ul>
        <li><a href="/statistics">Statistics Dashboard</a></li>
      </ul>
    </aside>

    <main class="main-content">
      <h2>System Statistics</h2>
      <!-- Summary Cards -->
      <div class="stats-summary">
        <div class="stat-card">
          <h3>Cases</h3>
          <div class="stat-numbers">
            <p>Pending: <span id="pending-count">0</span></p>
            <p>Solved: <span id="solved-count">0</span></p>
            <p>Total: <span id="total-cases">0</span></p>
          </div>
        </div>
        <div class="stat-card">
          <h3>Norms</h3>
          <div class="stat-numbers">
            <p>Valid: <span id="valid-norms">0</span></p>
            <p>Invalid: <span id="invalid-norms">0</span></p>
            <p>Total: <span id="total-norms">0</span></p>
          </div>
        </div>
        <div class="stat-card">
          <h3>System Health</h3>
          <div class="stat-numbers">
            <p>Resolution Rate: <span id="resolution-rate">0%</span></p>
          </div>
        </div>
      </div>

      <div class="stats-summary">
        <div class="stat-card">
          <h3>Normative Inflation</h3>
          <button @click="openDialog" class="info-button" aria-label="More Info">ℹ️</button>
          <div class="stat-numbers">
            <p>Normative Density: <span id="normative-density">0</span></p>
            <p>Processing Rate: <span id="processing-rate">0</span></p>
            <p>Backlog: <span id="backlog">0</span></p>
            <p>Temporal Gap: <span id="temporal-gap">0</span></p>
          </div>
        </div>
      </div>

      <!-- Hidden Dialog for Statistical Explanation -->
      <div id="math-dialog" class="dialog" role="dialog" aria-labelledby="dialog-title" aria-describedby="dialog-description">
      <div class="dialog-content" style="text-align: justify; line-height: 1.6;">
        <span class="close-button" @click="closeDialog" aria-label="Close">&times;</span>
        <h2 id="dialog-title">Understanding Normative Inflation</h2>
        
        <p id="dialog-description">
          Normative Inflation describes the accumulation of legal norms that remain unprocessed within the judicial system.
          It results from an imbalance between the rate at which norms are created and the rate at which they are reviewed and resolved by judicial institutions.
          If the <strong>Normative Density (ND)</strong> (norms introduced per day) exceeds the <strong>Processing Rate (PR)</strong> (norms resolved per day),
          the <strong>Backlog (Bₜ)</strong> grows over time, leading to systemic delays. The <strong>Temporal Gap (TG)</strong> measures the average time it
          takes for a norm to be processed, reflecting judicial efficiency.
        </p>

        <h3 style="margin-top: 20px;">1. Normative Density (ND)</h3>
        <p>
          The rate at which new norms enter the legal system. This metric captures the inflow of legal norms,
          reflecting how frequently new regulations, statutes, or legislative instruments are introduced over time.
        </p>
        <p style="text-align: center;" class="katex-formula">
          ND_t = \text{Number of new norms at time } t
        </p>

        <h3 style="margin-top: 20px;">2. Processing Rate (PR)</h3>
        <p>
          The rate at which norms are processed, meaning the frequency with which legal norms are explicitly referenced,
          cited, or applied in court decisions. Unlike ND, which measures introduction, PR focuses on how frequently
          legal norms are engaged in judicial proceedings.
        </p>
        <p style="text-align: center;" class="katex-formula">
          PR_t = \text{Number of norms processed at time } t
        </p>

        <h3 style="margin-top: 20px;">3. Backlog (Bₜ)</h3>
        <p>
          The accumulation of unresolved norms over time. It represents the difference between ND and PR,
          reflecting the extent to which norms accumulate without being processed in courts.
          A growing backlog signals a potential legal inflation problem, where norms outpace
          the judicial system's ability to engage with them.
        </p>
        <p style="text-align: center;" class="katex-formula">
          B_t = B_{t-1} + (ND_t - PR_t)
        </p>
        <p style="text-align: center;">
          where B_0 = 0 means no initial backlog.
        </p>

        <h3 style="margin-top: 20px;">4. Temporal Gap (TG)</h3>
        <p>
          The average time delay between the introduction of a norm and its processing.
          This metric helps assess judicial efficiency, revealing how long it takes for newly introduced norms
          to be referenced or applied in legal decisions.
          A high TG suggests delays in judicial engagement with legislation, while a low TG
          indicates that norms are quickly integrated into legal reasoning.
        </p>
        <p style="text-align: center;" class="katex-formula">
          TG = \frac{\sum_{i=1}^{N_p} (\text{Resolved Time}_i - \text{Created Time}_i)}{N_p}
        </p>
        <p style="text-align: center;">
          where Np represents the number of norms that have been processed.
        </p>

        <h3 style="margin-top: 20px;">Hypothesis</h3>
        <ul>
          <li><strong>If TG is high</strong>, norms accumulate without being processed, suggesting a growing backlog and potential bottlenecks in norm application.</li>
          <li><strong>If TG is low</strong>, norms are efficiently referenced in legal proceedings, ensuring a responsive and adaptive judicial system.</li>
          <li><strong>If ND > PR</strong>, backlog accumulates, leading to normative inflation and possible legal uncertainty as unprocessed norms pile up.</li>
          <li><strong>If ND ≈ PR</strong>, the system maintains equilibrium, ensuring that new norms are effectively integrated into legal practice.</li>
        </ul>
      </div>
    </div>
      <!-- Charts Section -->
      <div class="chart-box">
        <h3>Accepted vs Rejected Decisions</h3>
        <canvas id="decisionChart"></canvas>
      </div>
      <div class="charts-container">
        <div class="chart-box">
          <h3>Cases Chart</h3>
          <canvas id="caseTypesChart"></canvas>
        </div>
        <div class="chart-box">
          <h3>Case Resolution Timeline</h3>
          <canvas id="resolutionTimelineChart"></canvas>
        </div>
        <div class="chart-box">
          <h3>System Trends</h3>
          <canvas id="trendsChart"></canvas>
        </div>
        <h2>Still not fully functional charts but coming soon</h2>
        <br><br><br>
        <div class="chart-box">
          <h3>Stacked Bar Chart</h3>
          <canvas id="stackedBarChart"></canvas>
        </div>
        <div class="chart-box">
          <h3>Bubble Chart</h3>
          <canvas id="bubbleChart"></canvas>
        </div>
        <div class="chart-box">
          <h3>Area Chart</h3>
          <canvas id="areaChart"></canvas>
        </div>
        <div class="chart-box">
          <h3>Scatter Plot</h3>
          <canvas id="scatterPlot"></canvas>
        </div>
        <div class="chart-box">
          <h3>Heatmap</h3>
          <canvas id="heatmap"></canvas>
        </div>
        <div class="chart-box">
          <h3>Funnel Chart</h3>
          <canvas id="funnelChart"></canvas>
        </div>
        <div class="chart-box">
          <h3>Radar Chart</h3>
          <canvas id="radarChart"></canvas>
        </div>
        <div class="chart-box">
          <h3>Box Plot</h3>
          <canvas id="boxPlot"></canvas>
        </div>
        <div class="chart-box">
          <h3>Geographic Heatmap</h3>
          <canvas id="geoHeatmap"></canvas>
        </div>
        <div class="chart-box">
          <h3>Norms Validity Distribution</h3>
          <canvas id="normsValidityChart"></canvas>
        </div>
      </div>
    </main>

    <footer>
      © 2024 Optimus Interface - Enhancing Rule of Law through Systems Interaction
    </footer>
  </div>
</template>
<script>
import { Chart, registerables } from 'chart.js';
import katex from 'katex';
import 'katex/dist/katex.min.css';

// Register all the components that Chart.js provides
Chart.register(...registerables);

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "https://optimus-software.onrender.com";

export default {
  name: 'StatisticsDashboard',
  data() {
    return {
      loading: false,
      error: null,
      intervals: {
        statistics: null,
        inflation: null
      },
      chartInstances: {
        caseTypes: null,
        resolution: null,
        trends: null,
        decisionChart: null,
        stackedBarChart: null,
        bubbleChart: null,
        areaChart: null,
        scatterPlot: null,
        heatmap: null,
        funnelChart: null,
        radarChart: null,
        boxPlot: null,
        geoHeatmap: null,
        normsValidityChart: null
      }
    };
  },
  mounted() {
    this.initializeData();
    this.startPolling();
  },
  beforeDestroy() {
    this.cleanup();
  },
  methods: {
    async initializeData() {
      await this.fetchStatistics();
      await this.fetchNormativeInflation();
    },
    startPolling() {
      this.intervals.statistics = setInterval(this.fetchStatistics, 30000);
      this.intervals.inflation = setInterval(this.fetchNormativeInflation, 30000);
    },
    cleanup() {
      Object.values(this.intervals).forEach(interval => {
        if (interval) clearInterval(interval);
      });

      Object.values(this.chartInstances).forEach(chart => {
        if (chart) chart.destroy();
      });
    },
    async fetchStatistics() {
      this.loading = true;
      this.error = null;

      try {
        const [statsResponse, solvedResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/api/get_statistics`),
          fetch(`${API_BASE_URL}/api/get_solved_cases`)
        ]);

        if (!statsResponse.ok) throw new Error(`Statistics failed with status ${statsResponse.status}`);
        if (!solvedResponse.ok) throw new Error(`Solved cases failed with status ${solvedResponse.status}`);

        const data = await statsResponse.json();
        const solvedData = await solvedResponse.json();

        // Mise à jour des compteurs de l'interface
        this.updateElementText('pending-count', data?.cases?.pending ?? 0);
        this.updateElementText('solved-count', data?.cases?.solved ?? 0);
        this.updateElementText('total-cases', data?.cases?.total ?? 0);
        this.updateElementText('valid-norms', data?.norms?.valid ?? 0);
        this.updateElementText('invalid-norms', data?.norms?.invalid ?? 0);
        this.updateElementText('total-norms', data?.norms?.total ?? 0);

        const resolutionRate = data?.cases?.total
          ? Math.round((data.cases.solved / data.cases.total) * 100)
          : 0;
        this.updateElementText('resolution-rate', `${resolutionRate}%`);

        // Compter les décisions Accepted / Rejected
        const acceptedCount = solvedData.solved_cases.filter(c => c.decision === "Accepted").length;
        const rejectedCount = solvedData.solved_cases.filter(c => c.decision === "Rejected").length;

        // Mise à jour des graphiques
        this.updateResolutionTimeline(solvedData?.solved_cases ?? []);
        this.updateTrendsChart(
          data?.cases?.total ?? 0,
          data?.cases?.solved ?? 0,
          data?.cases?.pending ?? 0
        );
        this.updateCaseTypesChart(
          data?.cases?.pending ?? 0,
          data?.cases?.solved ?? 0
        );
        this.updateDecisionChart(acceptedCount, rejectedCount);
        this.updateStackedBarChart(data?.cases);
        this.updateBubbleChart(data?.cases);
        this.updateAreaChart(data?.cases);
        this.updateScatterPlot(data?.cases);
        this.updateHeatmap(data?.cases);
        this.updateFunnelChart(data?.cases);
        this.updateRadarChart(data?.cases);
        this.updateBoxPlot(data?.cases);
        this.updateGeoHeatmap(data?.cases);
        this.updateNormsValidityChart(data?.norms);
      } catch (error) {
        this.error = error.message;
        console.error("Error fetching statistics:", error);
      } finally {
        this.loading = false;
      }
    },

    async fetchNormativeInflation() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/get_normative_inflation`);
        if (!response.ok) throw new Error(`Failed with status ${response.status}`);

        const data = await response.json();

        this.updateElementText('normative-density', data?.inflation_data?.normative_density ?? 0);
        this.updateElementText('processing-rate', data?.inflation_data?.processing_rate ?? 0);
        this.updateElementText('backlog', data?.inflation_data?.backlog ?? 0);
        this.updateElementText('temporal-gap', data?.inflation_data?.temporal_gap ?? "N/A");
      } catch (error) {
        console.error("Error fetching normative inflation metrics:", error);
      }
    },

    updateElementText(id, value) {
      const element = document.getElementById(id);
      if (element) {
        element.textContent = value;
      } else {
        console.warn(`Element with ID '${id}' not found.`);
      }
    },

    updateCaseTypesChart(pending, solved) {
      const ctx = document.getElementById('caseTypesChart')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for caseTypesChart not found.");
        return;
      }

      if (this.chartInstances.caseTypes) {
        this.chartInstances.caseTypes.destroy();
      }

      this.chartInstances.caseTypes = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Pending Cases', 'Solved Cases'],
          datasets: [{
            data: [pending, solved],
            backgroundColor: ['#FFCE56', '#36A2EB'],
            borderWidth: 1,
            borderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            }
          },
          cutout: '70%'
        }
      });
    },

    updateResolutionTimeline(solvedCases) {
      const ctx = document.getElementById('resolutionTimelineChart')?.getContext('2d');
      if (!ctx) {
        console.warn("⚠️ Canvas for resolutionTimelineChart not found.");
        return;
      }

      if (this.chartInstances.resolution) {
        console.log("🔄 Destroying previous chart before creating a new one...");
        this.chartInstances.resolution.destroy();
      }

      if (!Array.isArray(solvedCases) || solvedCases.length === 0) {
        console.warn("⚠️ No solved cases data available for timeline.");
        return;
      }

      const resolutionData = {};
      solvedCases.forEach(caseItem => {
        if (caseItem.resolved_at) {
          const date = caseItem.resolved_at.split('T')[0];
          resolutionData[date] = (resolutionData[date] || 0) + 1;
        }
      });

      const sortedDates = Object.keys(resolutionData).sort();
      const resolvedCounts = sortedDates.map(date => resolutionData[date]);

      this.chartInstances.resolution = new Chart(ctx, {
        type: 'line',
        data: {
          labels: sortedDates,
          datasets: [{
            label: 'Cases Resolved Over Time',
            data: resolvedCounts,
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            tension: 0.4,
            fill: true,
            pointBackgroundColor: '#fff',
            pointBorderColor: '#4CAF50',
            pointBorderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 1 }
            },
            x: {
              title: { display: true, text: 'Date' }
            }
          },
          plugins: {
            legend: { display: true, position: 'top' },
            tooltip: {
              callbacks: {
                title: context => `Date: ${context[0].label}`,
                label: context => `Cases Resolved: ${context.raw}`
              }
            }
          }
        }
      });
    },

    updateTrendsChart(totalCases, solvedCases, pendingCases) {
      const ctx = document.getElementById('trendsChart')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for trendsChart not found.");
        return;
      }

      if (this.chartInstances.trends) {
        this.chartInstances.trends.destroy();
      }

      this.chartInstances.trends = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Cases Overview'],
          datasets: [
            {
              label: 'Total Cases',
              data: [totalCases],
              backgroundColor: '#FF6384'
            },
            {
              label: 'Solved Cases',
              data: [solvedCases],
              backgroundColor: '#36A2EB'
            },
            {
              label: 'Pending Cases',
              data: [pendingCases],
              backgroundColor: '#FFCE56'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true
            }
          },
          plugins: {
            legend: {
              position: 'top'
            }
          }
        }
      });
    },

    updateDecisionChart(accepted, rejected) {
      const ctx = document.getElementById('decisionChart')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for decisionChart not found.");
        return;
      }

      if (this.chartInstances.decisionChart) {
        this.chartInstances.decisionChart.destroy();
      }

      this.chartInstances.decisionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Accepted', 'Rejected'],
          datasets: [{
            data: [accepted, rejected],
            backgroundColor: ['#4CAF50', '#FF5733'],
            borderWidth: 1,
            borderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
            }
          },
          cutout: '70%'
        }
      });
    },

    updateStackedBarChart(cases) {
      const ctx = document.getElementById('stackedBarChart')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for stackedBarChart not found.");
        return;
      }

      if (this.chartInstances.stackedBarChart) {
        this.chartInstances.stackedBarChart.destroy();
      }

      const data = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
          label: 'Pending Cases',
          data: [cases.pending, cases.pending, cases.pending, cases.pending, cases.pending, cases.pending, cases.pending],
          backgroundColor: '#FFCE56'
        }, {
          label: 'Solved Cases',
          data: [cases.solved, cases.solved, cases.solved, cases.solved, cases.solved, cases.solved, cases.solved],
          backgroundColor: '#36A2EB'
        }]
      };

      this.chartInstances.stackedBarChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,
            },
            y: {
              stacked: true
            }
          }
        }
      });
    },

    updateBubbleChart(cases) {
      const ctx = document.getElementById('bubbleChart')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for bubbleChart not found.");
        return;
      }

      if (this.chartInstances.bubbleChart) {
        this.chartInstances.bubbleChart.destroy();
      }

      const data = {
        datasets: [{
          label: 'Cases',
          data: [
            { x: 10, y: 20, r: cases.pending },
            { x: 20, y: 30, r: cases.solved }
          ],
          backgroundColor: '#FF6384'
        }]
      };

      this.chartInstances.bubbleChart = new Chart(ctx, {
        type: 'bubble',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              beginAtZero: true
            },
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },

    updateAreaChart(cases) {
      const ctx = document.getElementById('areaChart')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for areaChart not found.");
        return;
      }

      if (this.chartInstances.areaChart) {
        this.chartInstances.areaChart.destroy();
      }

      const data = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
          label: 'Total Cases',
          data: [cases.total, cases.total, cases.total, cases.total, cases.total, cases.total, cases.total],
          fill: true,
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
        }]
      };

      this.chartInstances.areaChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              stacked: true,
            },
            y: {
              stacked: true
            }
          }
        }
      });
    },

    updateScatterPlot(cases) {
      const ctx = document.getElementById('scatterPlot')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for scatterPlot not found.");
        return;
      }

      if (this.chartInstances.scatterPlot) {
        this.chartInstances.scatterPlot.destroy();
      }

      const data = {
        datasets: [{
          label: 'Cases',
          data: [{ x: 1, y: cases.pending }, { x: 2, y: cases.solved }],
          backgroundColor: 'rgba(54, 162, 235, 0.2)'
        }]
      };

      this.chartInstances.scatterPlot = new Chart(ctx, {
        type: 'scatter',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              type: 'linear',
              position: 'bottom'
            }
          }
        }
      });
    },

    updateHeatmap(cases) {
      const ctx = document.getElementById('heatmap')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for heatmap not found.");
        return;
      }

      if (this.chartInstances.heatmap) {
        this.chartInstances.heatmap.destroy();
      }

      const data = {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        datasets: [{
          label: 'Cases',
          data: [cases.pending, cases.solved, cases.total, cases.pending, cases.solved],
          backgroundColor: function(context) {
            const value = context.dataset.data[context.dataIndex];
            return value > 50 ? 'red' : 'green';
          }
        }]
      };

      this.chartInstances.heatmap = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              beginAtZero: true
            },
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },

    updateFunnelChart(cases) {
      const ctx = document.getElementById('funnelChart')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for funnelChart not found.");
        return;
      }

      if (this.chartInstances.funnelChart) {
        this.chartInstances.funnelChart.destroy();
      }

      const data = {
        labels: ['Opened', 'In Progress', 'Resolved'],
        datasets: [{
          label: 'Case Funnel',
          data: [cases.total, cases.pending, cases.solved],
          backgroundColor: ['#FF6384', '#FFCE56', '#36A2EB']
        }]
      };

      this.chartInstances.funnelChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          scales: {
            x: {
              beginAtZero: true
            }
          }
        }
      });
    },

    updateRadarChart(cases) {
      const ctx = document.getElementById('radarChart')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for radarChart not found.");
        return;
      }

      if (this.chartInstances.radarChart) {
        this.chartInstances.radarChart.destroy();
      }

      const data = {
        labels: ['Pending', 'Solved', 'Total'],
        datasets: [{
          label: 'Case Radar',
          data: [cases.pending, cases.solved, cases.total],
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      };

      this.chartInstances.radarChart = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              angleLines: {
                display: false
              },
              suggestedMin: 0,
              suggestedMax: 100
            }
          }
        }
      });
    },

    updateBoxPlot(cases) {
      const ctx = document.getElementById('boxPlot')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for boxPlot not found.");
        return;
      }

      if (this.chartInstances.boxPlot) {
        this.chartInstances.boxPlot.destroy();
      }

      const data = {
        labels: ['Cases'],
        datasets: [{
          label: 'Case Distribution',
          data: [
            { min: 0, max: cases.total, median: cases.solved, q1: cases.pending, q3: cases.total }
          ],
          borderColor: 'rgba(54, 162, 235, 1)',
          showLine: true
        }]
      };

      this.chartInstances.boxPlot = new Chart(ctx, {
        type: 'boxplot',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              beginAtZero: true
            }
          }
        }
      });
    },

    updateGeoHeatmap(cases) {
      const ctx = document.getElementById('geoHeatmap')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for geoHeatmap not found.");
        return;
      }

      if (this.chartInstances.geoHeatmap) {
        this.chartInstances.geoHeatmap.destroy();
      }

      const data = {
        labels: ['Region A', 'Region B', 'Region C'],
        datasets: [{
          label: 'Geographic Distribution',
          data: [cases.pending, cases.solved, cases.total],
          backgroundColor: ['#FF6384', '#FFCE56', '#36A2EB']
        }]
      };

      this.chartInstances.geoHeatmap = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              beginAtZero: true
            },
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },

    updateNormsValidityChart(norms) {
      const ctx = document.getElementById('normsValidityChart')?.getContext('2d');
      if (!ctx) {
        console.warn("Canvas for normsValidityChart not found.");
        return;
      }

      if (this.chartInstances.normsValidityChart) {
        this.chartInstances.normsValidityChart.destroy();
      }

      const data = {
        labels: ['Valid Norms', 'Invalid Norms'],
        datasets: [{
          label: 'Norms Validity',
          data: [norms.valid, norms.invalid],
          backgroundColor: ['#36A2EB', '#FF6384']
        }]
      };

      this.chartInstances.normsValidityChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },

    openDialog() {
      const dialog = document.getElementById('math-dialog');

      // Show the dialog
      dialog.style.display = 'block';

      // Render all KaTeX formulas
      this.renderKatexFormulas();
    },

    renderKatexFormulas() {
      // Select all elements with class 'katex-formula'
      const formulas = document.querySelectorAll('.katex-formula');

      // Render each formula with KaTeX
      formulas.forEach(element => {
        try {
          katex.render(element.textContent, element, {
            displayMode: true,
            throwOnError: false
          });
        } catch (err) {
          console.error("KaTeX rendering error:", err);
          // Fallback - display the raw formula if rendering fails
          element.textContent = element.textContent;
        }
      });
    },

    closeDialog() {
      const dialog = document.getElementById('math-dialog');
      const overlay = document.querySelector('.dialog-overlay');

      if (dialog) {
        dialog.style.display = 'none';
      }
      if (overlay) {
        overlay.remove();
      }
    }
  }
};
</script>
<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary: #2563eb;
  --secondary: #6b7280;
  --text-color: #374151;
  --bg-light: #f9fafb;
  --bg-white: #ffffff;
  --border-color: #e5e7eb;
  --sidebar-width: 280px;
  --header-height: 60px;
  --transition-speed: 0.2s;
  --shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  --border-radius: 8px;
  --font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

body {
  font-family: var(--font-family);
  background: var(--bg-light);
  color: var(--text-color);
}

header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: var(--header-height);
  background: var(--bg-white);
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  z-index: 20;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.sidebar {
  position: fixed;
  top: var(--header-height);
  left: 0;
  width: var(--sidebar-width);
  height: calc(100vh - var(--header-height));
  background: var(--bg-white);
  border-right: 1px solid var(--border-color);
  padding: 1.5rem;
  overflow-y: auto;
  box-shadow: 1px 0 4px rgba(0, 0, 0, 0.05);
}

.sidebar h3 {
  color: var(--secondary);
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 1.5rem 0 0.75rem;
}

.sidebar ul {
  list-style: none;
  margin-bottom: 1rem;
}

.sidebar a {
  color: var(--text-color);
  text-decoration: none;
  display: block;
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  transition: background-color var(--transition-speed), color var(--transition-speed);
}

.sidebar a:hover {
  background: #f3f4f6;
  color: var(--primary);
}

.main-content {
  margin-left: var(--sidebar-width);
  margin-top: var(--header-height);
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.stats-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  flex: 1;
  min-width: 280px;
  background: var(--bg-white);
  padding: 1.5rem;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  text-align: center;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.chart-box {
  background: var(--bg-white);
  padding: 1rem;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100%;
  max-height: 400px;
  overflow: hidden;
}

.chart-box h3 {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--text-color);
}

.chart-box canvas {
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  max-height: 300px;
}

.dialog {
  display: none;
  position: fixed;
  z-index: 1000;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background-color: var(--bg-white);
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.dialog-content {
  padding: 1rem;
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--secondary);
  background: none;
  border: none;
  transition: color var(--transition-speed);
}

.close-button:hover {
  color: red;
}

.dialog-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

footer {
  margin-left: var(--sidebar-width);
  padding: 1.5rem;
  text-align: center;
  color: var(--secondary);
  border-top: 1px solid var(--border-color);
}

.katex-formula {
  overflow-x: auto;
  padding: 8px 0;
}

.main-content h2 {
  margin-bottom: 40px;
}

@media (max-width: 1024px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform var(--transition-speed);
  }

  .sidebar.active {
    transform: translateX(0);
  }

  .main-content, footer {
    margin-left: 0;
  }

  .stats-summary, .charts-container {
    grid-template-columns: 1fr;
  }
}
</style>
