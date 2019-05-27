<template>
  <div id="sgrade">
    <p> 成绩 </p>
    <div id="sgrade_table">
        <display :display_data = "grade"/>
    </div>
    
  
    <div id="sgradelist">
        <visualizegrade v-if="gradelist.length > 0" :display_data="gradelist" 
        :labels="labels"/>
    
    </div>
  </div>
</template>

<script>
import display from "@/components/display.vue";
import visualizegrade from "@/components/visualizegrade.vue"
// import { constants } from 'crypto';
// import { toASCII } from 'punycode';
export default {
    components:{
        display,
        visualizegrade
        
    },
    data(){
        return{
            grade: {},
            gradelist : [],
            labels : [],
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
                    console.log(that.grade);
                    let _labels = [];
                    let _gradelist = [];
                    for(let i in this.grade)
                    {
                        _labels.push(this.grade[i][1]);
                        _gradelist.push(this.grade[i][2]);
                    }
                    that.labels = _labels;
                    that.gradelist = _gradelist;
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
