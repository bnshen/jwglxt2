<template>
  <div id="teacher" class="about">
    <h1>教师系统</h1>
    <router-link to="/teacher/tcourse">课程管理</router-link> |
    <router-link to="/teacher/tscore">分数登记</router-link> 
    <br/>
    <router-view> </router-view>
    
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

<style>
#course-table {
  border: "8";
}
</style>

