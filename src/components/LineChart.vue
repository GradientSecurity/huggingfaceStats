<template>
  <div>
    <canvas ref="chart"></canvas>
  </div>
</template>

<script>
import {Chart, registerables} from 'chart.js';

Chart.register(...registerables);

export default {
  name: 'LineChart',
  props: {
    chartData: {
      type: Object,
      required: true
    }
  },
  mounted() {
    this.createChart();
  },
  methods: {
    createChart() {
      const ctx = this.$refs.chart.getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.chartData.labels,
          datasets: [{
            label: 'Models',
            data: this.chartData.values,
            fill: false,
            borderColor: "#c319ee",
            backgroundColor: "#c319ee",
            tension: 0.4,
            pointRadius: 0,
          }]
        },
        options: {
          scales: {
            y: {
              ticks: {
                color: "#b6baca",
              },
              grid: {
                drawTicks: false,
                display: false,
              },
              border: {
                dash: [5, 10],
              },
            },
            x: {
              ticks: {
                color: "#b6baca",
              },
              grid: {
                display: false,
              },
              border: {
                display: false,
              },
            },
          },
          plugins: {
            legend: {
              display: false // This will hide the legend
            }
          },
        }
      });
    },

  },

}
</script>
