<template>
  <div id="addnewcourse">
    <div id="addnewcourse_outter">
      <table border="1">
        <tr>
          <th>信息</th>
          <th>值</th>
        </tr>
        <tr v-for="value in newcourse_info" v-bind:key="value">
          <td>{{value}}</td>
          <td>
            <input type="text" :name="value" :id="value">
          </td>
        </tr>
        <tr>
          <button @click="add">提交</button>
        </tr>
      </table>
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
      ]
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
