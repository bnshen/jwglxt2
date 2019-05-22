<template>
  <div id="sgrade">
    <p> 成绩 </p>
    <div id="sgrade_table">
        <display :display_data = "grade"/>
    </div>
    <visualize/>
  </div>
</template>

<script>
import display from "@/components/display.vue";
import visualize from "@/components/visualize.vue"
// import { constants } from 'crypto';
// import { toASCII } from 'punycode';
export default {
    components:{
        display,
        visualize
    },
    data(){
        return{
            grade: {}
        }
    },
    methods:{
        get_grade() {
            let that = this;
            let get_grade_api = "Student/scores";
            that.axios({
                method: "get",
                url: get_grade_api,
                headers: { Authorization: localStorage.getItem("token") }
                }).then(res => {
                if(res.data.status == 200) {
                    console.log("get_grade_success");
                    that.grade = res.data.data.scores;
                    console.log(res.data.data.scores)
                }
                else {
                    console.log("get_elective_fail: " + res.data.status)
                }})
        }
    },
    created:function(){
        this.get_grade();
    }
}
</script>

<style>
</style>
