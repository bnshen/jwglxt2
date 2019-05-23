<template>
  <div id="tcourse">
    <display :display_data="openC" :e2c="e2c"/>
  </div>
</template>

<script>
import display from "@/components/display.vue";
export default {
    name:'tcourse',
    components:{
        display
    },
    data(){
        return{
            openC:{},
            e2c:{
            'course_credit':'学分',
            'course_final_exam_precentage':'期末成绩比例',
            'course_hour'	:'学时',
            'course_name'	:'课程名',
            'course_no'	:'课程号',
            'openc_QA_time'	:'答疑时间',
            'openc_address'	:'上课地点',
            'openc_curnum'	:'当前人数',
            'openc_id'	:'openc_id',
            'openc_maxnum':'最大人数',
            'openc_time':'上课时间',
            'semester_name':'开课学期'
            }
        }
    },
    methods:{
      course: function() {
      let that = this;
      let api = "Teacher/courses";
      that.axios({
        method: "get",
        url: api,
        headers: { Authorization: localStorage.getItem("token") }
      }).then(function(response) {
        console.log(response);
        let _openC = response.data.data.OpenC;
        that.openC = _openC;
      })
    }
  },
  created:function(){
    this.course();
  }


}
</script>

<style>
</style>
