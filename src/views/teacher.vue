<template>
  <div id="teacher" class="about">
    <div id="nav">
    <h4 id = "t_welcome">欢迎来到教师系统</h4>

    <router-link to="/teacher/tcourse">课程管理</router-link> |
    <router-link to="/teacher/tscore">分数登记</router-link> 
    </div>
    <hr/>
    <div id = "outter-box">
    <router-view> </router-view>
    </div>
    
  </div>
</template>

<script>
import { constants } from "crypto";

export default {
  name: "teacher",
  components: {
  },
  data() {
    return {
    };
  },
  methods: {

  },
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
#t_welcome{
  float: left;
}
#outter-box{
  padding: 0 auto;
  padding-top: 5%;
  margin: 0 auto;
}
</style>

