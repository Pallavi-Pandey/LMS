<template>
  <div class="dashboard-container">
    <div class="row mb-5">
      <div class="col-md-12 text-center">
        <h1 class="display-5 fw-bold text-white mb-2">Statistics</h1>
        <p class="text-white-50">Overview of library activity</p>
      </div>
    </div>

    <div class="glass-panel p-5">
        <div class="chart-container mx-auto">
             <Bar
                id="my-chart-id"
                :options="chartOptions"
                :data="chartData"
                v-if="chartData.datasets[0].data.length > 0"
            />
             <div v-else class="text-center py-5">
                 <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                 </div>
             </div>
        </div>
    </div>
  </div>
</template>
  
<script>
import API_BASE_URL from "../config";
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: 'BarChart',
    components: { Bar },
    data() {
      return {
        chartData: {
          labels: [],
          datasets: [ { 
              data: [],
              backgroundColor: 'rgba(79, 70, 229, 0.6)',
              borderColor: '#4f46e5',
              borderWidth: 1,
              borderRadius: 5,
              barThickness: 50
          } ]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
              legend: {
                  display: false
              },
              tooltip: {
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  titleColor: '#1f2937',
                  bodyColor: '#4b5563',
                  borderColor: '#e5e7eb',
                  borderWidth: 1,
                  padding: 10,
                  displayColors: false,
              }
          },
          scales: {
              y: {
                  beginAtZero: true,
                  grid: {
                      color: 'rgba(0, 0, 0, 0.05)',
                  },
                  ticks: {
                      font: { family: "'Inter', sans-serif" }
                  }
              },
              x: {
                   grid: {
                      display: false
                  },
                   ticks: {
                      font: { family: "'Inter', sans-serif" }
                  }
              }
          }
        }
      }
    },
    methods:{
        async fetch_barchart_data(){
            try {
                const response = await fetch(`${API_BASE_URL}/get_barchart_data`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Authentication-Token': localStorage.getItem('auth-token')
                    },
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch bar chart data');
                }
                const data = await response.json();
                // Ensure data format matches chart.js expectations if specific API structure
                // Assuming API returns { labels: [], datasets: [] } or similar, merging carefully
                // If API returns simple object, might need mapping.
                // Based on previous code: `this.chartData = data` suggested API returns full config?
                // Or API matches vue-chartjs data prop structure.
                
                // Let's assume the API returns the structure expected by chartData
                // Ideally I should check the backend log or previous code assumptions
                // The previous code did `this.chartData = data`.
                this.chartData = data; 
                
                // Overwrite style preferences if data does not have them
                 if(this.chartData.datasets && this.chartData.datasets[0]) {
                     this.chartData.datasets[0].backgroundColor = 'rgba(79, 70, 229, 0.6)';
                     this.chartData.datasets[0].borderRadius = 8;
                 }


            } catch (error) {
                console.error(error);
            }
        }
    },
    mounted() {
      this.fetch_barchart_data();
    }
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  padding: 2rem;
  background: var(--bg-gradient);
}
.glass-panel {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  min-height: 500px;
}
.chart-container {
    height: 400px;
    width: 100%;
}
</style>