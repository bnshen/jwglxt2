<template>
  <div id="student" class="about">
    <h1>欢迎学生：{{ username }} </h1>
    <router-link to="/student/course">查看课程</router-link> |
    <router-link to="/student/elective">选课and删课</router-link> |
    <router-link to="/student/info">个人信息管理</router-link> |
    <router-link to="/student/grade">查看成绩表</router-link>
    <br/>
    <router-view> </router-view>
    
  </div>
</template>

<script>
// import { constants } from "crypto";

export default {
  name: "student",
  components: {
  },
  data() {
    return {
      username: ""
    };
  },
  methods: {
    get_username() {
      let info = JSON.parse(localStorage.getItem("user_info"));
      this.username = info["student_name"];
    }
  },
  created: function(){
    this.get_username();
  }
};
</script>

<style>
#course-table {
  border: "8";
}
</style>

