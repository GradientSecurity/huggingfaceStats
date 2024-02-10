<template>
    <div>
        Monthly Growth
    </div>
    <div>
        <canvas ref="modelsBarChart"></canvas>
    </div>
</template>


<script>
import {Chart, registerables} from 'chart.js';

Chart.register(...registerables);

export default {
    name: 'ModelsBarChart',
    props: {
        modelsData: {
            type: Object,
            required: true
        }
    },
    mounted() {
        this.renderModelsBarChart();
    },
    methods: {
        renderModelsBarChart() {
            const months = Object.keys(this.modelsData);
            const modelsCount = Object.values(this.modelsData);

            const ctx = this.$refs.modelsBarChart.getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'New Models',
                        data: modelsCount,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Models'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Month'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: false // Set to true if you want to display the label
                        }
                    },
                    responsive: true,
                    maintainAspectRatio: false,
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