<template>
    <div class="title">Huggingface Stats</div>
    <div class="summarized_stats" v-if="summaryStats">
        <div class="stat" v-for="statName in Object.keys(summaryStats)" :key="statName">
            <div class="stat-name">{{ statName.replaceAll("_", " ").replace("avg", "Average") }}:</div>
            <div class="stat-value">{{ getSummaryValue(statName) }}</div>
        </div>
    </div>
    <modelsByDate :raw-data="models" v-if="models"></modelsByDate>
    <forecastChart :forecast-data="forecastForMonth" :time-period="30" v-if="forecastForMonth"></forecastChart>
    <forecastChart :forecast-data="forecastForYear" :time-period="365" v-if="forecastForYear"></forecastChart>
    <growthRateChart :growth-data="growthRateStats" v-if="growthRateStats"></growthRateChart>
    <movingAvgChart :moving-avg-data="movingAvgData" v-if="movingAvgData"></movingAvgChart>
    <monthlyGrowthChart :modelsData="monthlyGrowthData" v-if="monthlyGrowthData"></monthlyGrowthChart>
</template>

<script>
import modelsByDate from './components/ModelsByDate.vue'
import forecastChart from './components/forecastChart.vue'
import growthRateChart from "@/components/growthRateChart";
import movingAvgChart from "@/components/movingAvgChart";
import monthlyGrowthChart from "@/components/monthlyGrowthChart";
import modelsOverTime from '../public/models_over_time.json'
import forecastMonth from '../public/forecast_30_days_ahead.json'
import forecastYear from '../public/forecast_365_days_ahead.json'
import growthRate from '../public/growth_rates.json'
import movingAvg from '../public/moving_averages.json'
import mothlyGrowth from '../public/monthly_growth.json'
import summaryAvg from '../public/summary_stats.json'


export default {
    name: 'App',
    components: {
        modelsByDate,
        forecastChart,
        growthRateChart,
        movingAvgChart,
        monthlyGrowthChart
    },
    data() {
        return {
            models: null,
            forecastForMonth: null,
            forecastForYear: null,
            growthRateStats: null,
            movingAvgData: null,
            monthlyGrowthData: null,
            summaryStats: null
        }
    },
    methods: {
        getSummaryValue(value) {
            if (value === 'avg_daily_growth') {
                return `${this.summaryStats[value].toLocaleString()}%`;
            } else if (value === 'avg_growth_rate') {
                return `${this.summaryStats[value]}%`;
            }
            return this.summaryStats[value].toLocaleString();
        }
    },
    mounted() {
        try {
            this.models = modelsOverTime;
            this.forecastForMonth = forecastMonth;
            this.forecastForYear = forecastYear;
            this.growthRateStats = growthRate;
            this.movingAvgData = movingAvg;
            this.monthlyGrowthData = mothlyGrowth;
            this.summaryStats = summaryAvg;
        } catch (e) {
            console.error(e);
        }
    }
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}

.summarized_stats {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 20px 0;
}

.stat {
    display: flex;
    flex-direction: row;
}

.title {
    font-size: 1.5em;
    margin: 20px 0;
    font-weight: bold;
}
</style>
