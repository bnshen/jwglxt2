<template>
  <div id="teacher" class="about">
    <h1>this is teacher's page</h1>
    <router-link to="/teacher/tcourse">course</router-link> |
    <router-link to="/teacher/tscore">score</router-link> 

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

