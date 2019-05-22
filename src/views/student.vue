<template>
  <div id="student" class="about">
    <div id = 'nav'>
    <h4 id ="s-welcome">欢迎学生：{{ username }} </h4>
    <router-link to="/student/course">查看课程</router-link> |
    <router-link to="/student/elective">选课and删课</router-link> |
    <router-link to="/student/info">个人信息管理</router-link> |
    <router-link to="/student/grade">查看成绩表</router-link>
    </div>
    <hr/>
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

<style lang="scss">
#course-table {
  border: "8";
}
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
#s-welcome{
    float: left;
}
</style>

