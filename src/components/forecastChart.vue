<template>
    <div>
        {{ timePeriod }} Days Forecast
    </div>
    <div>
        <canvas ref="forecastChart"></canvas>
    </div>
</template>

<script>
import {Chart, registerables} from 'chart.js';

Chart.register(...registerables);

export default {
    name: 'ForecastChart',
    props: {
        forecastData: {
            type: Object,
            required: true
        },
        timePeriod: {
            type: String,
            required: true
        }
    },
    mounted() {
        try {
            this.renderChart();
        } catch (e) {
            console.error(e);
        }
    },
    methods: {
        renderChart() {
            const ctx = this.$refs.forecastChart.getContext('2d');
            const labels = this.forecastData['ds'].map(data => data.split(' ')[0]); // Fixed to use .map
            const yhatValues = this.forecastData['yhat'];
            const yhatLowerValues = this.forecastData['yhat_lower'];
            const yhatUpperValues = this.forecastData['yhat_upper'];

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Lower Bound',
                            data: yhatLowerValues,
                            borderColor: 'rgba(255, 99, 132, 0.2)',
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            fill: false,
                            borderWidth: 0,
                            pointRadius: 1,
                        },
                        {
                            label: 'Upper Bound',
                            data: yhatUpperValues,
                            borderColor: 'rgba(54, 162, 235, 0.2)',
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            fill: '-1',
                            borderWidth: 0,
                            pointRadius: 0,
                        },
                        {
                            label: 'Forecast',
                            data: yhatValues,
                            borderColor: "#c319ee",
                            backgroundColor: "#c319ee",
                            tension: 0.4,
                            pointRadius: 0,
                            fill: false,
                        }
                    ]
                },
                options: {
                    plugins: {
                        legend: {
                            display: true
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            grid: {
                                drawTicks: false,
                                display: false,
                            },
                        },
                        x: {
                            grid: {
                                drawTicks: false,
                                display: false,
                            },
                        }

                    },
                }
            });
        }
    },
}
</script>

<style scoped>
.main_chart {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 20px 0;
}

</style>