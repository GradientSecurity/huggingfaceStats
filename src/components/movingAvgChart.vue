<template>
    <div>
        Moving Average
    </div>
    <div>
        <canvas ref="movingAvgChart"></canvas>
    </div>
</template>


<script>
import {Chart, registerables} from 'chart.js';

Chart.register(...registerables);

export default {
    name: 'MovingAverageChart',
    props: {
        movingAvgData: {
            type: Object,
            required: true
        }
    },
    mounted() {
        this.renderMovingAverageChart();
    },
    methods: {
        renderMovingAverageChart() {
            const dates = Object.keys(this.movingAvgData);
            const movingAverages = Object.values(this.movingAvgData);

            const ctx = this.$refs.movingAvgChart.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Moving Average',
                        data: movingAverages,
                        borderColor: 'rgb(255, 159, 64)',
                        tension: 0.1,
                        fill: false,
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: false,
                            title: {
                                display: true,
                                text: 'Value'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true
                        }
                    }
                }
            });
        }
    }
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