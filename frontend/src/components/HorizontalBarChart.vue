<template>
  <div class="chart">
    <horizontal-bar-chart :chart-data="datacollection" :options="options" :height="height" :styles="myStyles"></horizontal-bar-chart>
  </div>
</template>

<script>
import HorizontalBarChart from './HorizontalBarChart.js'

export default {
  components: {
    HorizontalBarChart
  },
  data () {
    var labelsWidth = this.labelsWidth
    var titleChart = this.titleChart
    return {
      options: {
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            ticks: {
              beginAtZero: true
            }
          }],
          yAxes: [{
            afterFit: function (scaleInstance) {
              scaleInstance.width = labelsWidth // sets the width to 100px
            }
          }]
        },
        maintainAspectRatio: false,
        barPercentage: 0.5,
        title: {
          display: true,
          text: titleChart
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
    },
    height: function () {
      return 30 * this.labels.length + 60
    },
    myStyles () {
      return {
        height: `${this.height}px`,
        position: 'relative'
      }
    }
  },
  props: {
    chartData: {
      type: Array
    },
    labels: {
      type: Array
    },
    labelsWidth: {
      type: Number
    },
    titleChart: {
      type: String
    }
  }
}
</script>

<style>
  .chart {
    margin-top: 40px;
  }
</style>
