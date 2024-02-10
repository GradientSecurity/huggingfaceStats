<template>

    <div>Models Overtime</div>
    <LineChart v-if="preparedChartData" :chartData="preparedChartData"/>
</template>

<script>
import LineChart from './LineChart.vue';

export default {
    components: {
        LineChart
    },
    props: {
        rawData: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            preparedChartData: null
        }
    },
    mounted() {
        console.log(this.rawData)
        this.preparedChartData = this.prepareChartData(this.rawData);
    },
    methods: {
        prepareChartData(dataObject) {
            const labels = [];
            const values = [];

            Object.entries(dataObject).forEach(([key, value]) => {
                labels.push(key);
                values.push(value.models);
            });
            console.log({labels, values})
            return {labels, values};
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