<template>
  <div class="chart">
    <horizontal-bar-chart :chart-data="datacollection" :options="options" :height="100"></horizontal-bar-chart>
  </div>
</template>

<script>
import HorizontalBarChart from './HorizontalBarChart.js'

export default {
  components: {
    HorizontalBarChart
  },
  data () {
    return {
      options: {
        legend: {
          display: false
        },
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    }
  },
  computed: {
    datacollection: function () {
      return {
        labels: this.labels,
        datasets: [
          {
            backgroundColor: '#b2b2b2',
            data: this.chartData
          }
        ]
      }
    }
  },
  props: {
    chartData: {
      type: Array
    },
    labels: {
      type: Array
    }
  },
  methods: {
    getRandomInt () {
      return Math.floor(Math.random() * (50 - 5 + 1)) + 5
    }
  }
}
</script>

<style>
  .chart {
    margin-top: 40px;
  }
</style>
