<template>
  <div id="tcourse">
    <display :display_data="openC"/>
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
            openC:{}
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
