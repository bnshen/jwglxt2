<template>
  <div id="addnewcourse">
    <div id="addnewcourse_outter">
      <div class="container">
      <table border="1" class="table">
        <tr>
          <th>信息</th>
          <th>值</th>
        </tr>
        <tr v-for="value in newcourse_info" v-bind:key="value">
          <td>{{e2c[value]}}</td>
          <td>
            <input type="text" :name="value" :id="value">
          </td>
        </tr>
      </table>
      </div>
      <br/>
       <button class = "btn btn-primary" @click="add">提交</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "addnewcourse",
  data() {
    return {
      newcourse_info: [
        "course_no",
        "course_name",
        "course_credit",
        "course_hour",
        "department_id",
        "course_final_exam_precentage",
        "course_grade",
        "course_catagory"
      ],
       e2c:{
                'course_credit':'学分',
                'course_hour':'学时',
                'course_name':'课程名',
                'course_no':'课程号',
                'openc_QA_time':'答疑时间',
                'openc_address':'上课地点',
                'openc_available':'是否可选',
                'openc_curnum':'当前人数',
                'openc_id':'课程id',
                'openc_maxnum':'最大人数',
                'openc_time':'上课时间',
                'teacher_id':'教师号',
                'teacher_name':'教师姓名',
                'order':'顺序',
                'course_catagory':'课程类别',
                'department_id':'院系号',
                'course_final_exam_precentage':'期末成绩比例',
                'course_grade':'选课年级'
            }
    }
  },
  methods:{
      add: function() {
      let api = "Admin/courses";
      let _data = new FormData();
      let cur_info = this.newcourse_info;
      for (let i = 0; i < cur_info.length; i++) {
        _data.set(cur_info[i], document.getElementById(cur_info[i]).value);
      }
      this.axios({
        method: "post",
        url: api,
        headers: {
          Authorization: localStorage.getItem("token"),
          "Content-Type": "multipart/form-data"
        },
        data: _data
      }).then(function(response) {
        console.log(response);
      });
    }
  }
};
</script>

<style>
</style>
