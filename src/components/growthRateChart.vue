<template>

    <div>
        Daily Growth Rate
    </div>
    <div>
        <canvas ref="growthRateChart"></canvas>
    </div>
</template>

<script>
import {Chart, registerables} from 'chart.js';

Chart.register(...registerables);

export default {
    name: 'GrowthRateChart',
    props: {
        growthData: {
            type: Object,
            required: true
        }
    },
    mounted() {
        this.renderGrowthRateChart();
    },
    methods: {
        renderGrowthRateChart() {
            const growthDates = Object.keys(this.growthData);
            const growthRates = Object.values(this.growthData);

            const ctx = this.$refs.growthRateChart.getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: growthDates,
                    datasets: [{
                        label: 'Growth Rate',
                        data: growthRates,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Growth Rate (%)'
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