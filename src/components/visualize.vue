
  <div id="visualize">
      <canvas id="myChart" width="400" height="400"></canvas>
  </div>


<script>
import { Bar } from 'vue-chartjs'
export default {
  name: "visualize",
  props: ['display_data','labels'],
  extends: Bar,
  methods: {
  },
  mounted () {
    // Overwriting base render method with actual data.
    console.log(1);
    this.renderChart({
      labels: [1,2,3], 
      datasets: [
        {
          label: 'GitHub Commits',
          backgroundColor: '#f87979',
          data: [1.5,2,3]
        }
      ]
    })
  }
};
</script>

<style>
</style>
