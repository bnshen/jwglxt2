<template>
  <div id="changeuserinfo">
    <div>
      <label>
        <input id = 'studentinfo' type="radio" name="usertype" @click="changeuser('Student')">学生信息
      </label>
      <label>
        <input type="radio" name="usertype" @click="changeuser('Teacher')">教师信息
      </label>
    </div>
    <table border="1" v-if="catagory_id != 0">
      <tr>
        <th>信息</th>
        <th>值</th>
      </tr>
      <tr>
        <td>catagory_id</td>
        <td>{{catagory_id}}</td>
      </tr>
      <tr v-if="catagory_id == 2" v-for="value in teacher_info" v-bind:key="value">
        <td>{{value}}</td>
        <td>
          <input type="text" :name="value" :id="value">
        </td>
      </tr>
      <tr v-if="catagory_id == 3" v-for="value in student_info" v-bind:key="value">
        <td>{{value}}</td>
        <td>
          <input type="text" :name="value" :id="value">
        </td>
      </tr>
      <tr>
        <button v-if="catagory_id != 0" @click="changeinfo">提交</button>
      </tr>
    </table>
  </div>
</template>

<script>
import teacherVue from "../../views/teacher.vue";
export default {
  name: "changeuserinfo",
  data() {
    return {
      catagory_id: 0,
      teacher_info: [
        "teacher_no",
        "teacher_name",
        "teacher_sex",
        "teacher_birthtime",
        "teacher_education",
        "teacher_salary",
        "department_id",
        "teacher_workaddress",
        "password"
      ],
      student_info: [
        "student_no",
        "student_name",
        "student_sex ",
        "student_grade",
        "student_class",
        "student_birthtime",
        "student_birthaddress",
        "student_tel",
        "department_id",
        "password"
      ]
    };
  },
  methods: {
    changeuser: function(type) {
      if (type == "Student") this.catagory_id = 3;
      if (type == "Teacher") this.catagory_id = 2;
    },
    changeinfo: function() {
      let api = "Admin/userinfo";
      let _data = new FormData();
      _data.set("catagory_id", this.catagory_id);
      let cur_info;
      if (this.catagory_id == 2) cur_info = this.teacher_info;
      else cur_info = this.student_info;
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
  },
  mounted:function(){
        document.getElementById('studentinfo').click();
    }
};
</script>

<style>
</style>
