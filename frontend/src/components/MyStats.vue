
<template>

  <h2>Sections and Book count</h2>
    
    <Bar
      id="my-chart-id"
      :options="chartOptions"
      :data="chartData"
    />
  </template>
  
  <script>
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  export default {
    name: 'BarChart',
    components: { Bar },
    data() {
      return {
        chartData: {
          labels: [ 'January', 'February', 'March' ],
          datasets: [ { data: [400, 20, 12] } ]
        },
        chartOptions: {
          responsive: true
        }
      }
    },
    methods:{
        async fetch_barchart_data(){
            const response = await fetch('http://127.0.0.1:5000/get_barchart_data',
            {
                method: 'GET',
                headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Authentication-Token': localStorage.getItem('auth-token')
          },
            }
        );
            if (!response.ok) {
              throw new Error('Failed to fetch bar chart data');
            }
            const data = await response.json();
            this.chartData = data;
        }
    },
    mounted() {
      this.fetch_barchart_data();
    }
   
  }
  </script>