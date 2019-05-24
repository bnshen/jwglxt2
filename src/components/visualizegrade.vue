<template>
  <div id="visualizegrade">
    <div id="main" style="width: 60vw;height:60vh;"></div>
  </div>
</template>

<script>
import echarts from "echarts";
export default {
  name: "visualizegrade",
  props: ["display_data", "labels","title"],
  methods: {},
  mounted() {
    var myChart = echarts.init(document.getElementById("main"));

    // 指定图表的配置项和数据
    var option = {
      title:{
        text:'成绩柱状图'
      },
      xAxis: {
        type: "category",
        data: this.labels,
      },
      yAxis: {
        type: "value"
      },
      series: [
        {
          data: this.display_data,
          type: "bar"
        }
      ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
  }
};
</script>

<style>
#main{
  margin: 0 auto;
  padding: 0 auto;
}
</style>
