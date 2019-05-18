<template>
  <div id="selective">
    <div id="course_query">
        <p> 模糊查询 </p>
        <div id="display-query">
            课程号:  <input v-model="query.course_no" placeholder="课程号">
            课程名:  <input v-model="query.course_name" placeholder="课程名">
            教师号:  <input v-model="query.teacher_no" placeholder="教师号">
            教师名:  <input v-model="query.teacher_name" placeholder="教师名">
            学分数:  <input v-model="query.course_credit" placeholder="学分数">
        </div>
        <button @click="course_query()"> 查询 </button>
    </div>

    <div id="course_OpenC" v-if="query.exist">
        <p> 查询结果 </p>
        <div id = 'display-OpenC_table'>
            <table border="1" id = 'display-table' v-if = "OpenC">
                <tr>
                    <th v-for = "(value,key) in OpenC[0]" v-bind:key = "key"> 
                        {{key}}
                    </th> 
                    <th> 
                        选课
                    </th> 
                </tr>
                <tr v-for = "(value, key) in OpenC" v-bind:key = "key">
                    <td v-for = "(val ,keyitem) in value" v-bind:key = "keyitem">
                        {{val}}
                    </td>
                    <td>
                        <button @click="course_elective(value.openc_id)"> 选课 </button>
                    </td>
                </tr>
            </table>
        </div>
    </div>
  </div>
</template>

<script>
// import display from "@/components/display.vue";
// import { constants } from 'crypto';
// import { toASCII } from 'punycode';
export default {
    // components:{
    //     display
    // },
    inject: ['reload'],
    data(){
        return{
            query: {
                exist : false,
                course_no : "",
                course_name : "",
                teacher_no : "",
                teacher_name : "",
                course_credit : "",
            },
            OpenC: {}
        }
    },
    methods:{
        course_query() {
            let that = this;
            let get_elective_api = "OpenC/query";
            that.axios({
                method: "get",
                url: get_elective_api,
                headers: { Authorization: localStorage.getItem("token") },
                params: that.query
                }).then(res => {
                if(res.data.status == 200) {
                    that.query.exist = true,
                    that.OpenC = res.data.data.OpenC;
                    alert(res.data.status + ": " + res.data.msg),
                    this.reload()
                }
                else {
                    alert(res.data.status + ": " + res.data.msg)
                }
                console.log(res.data.status + ": " + res.data.msg)
                })
        },
        course_elective (openc_id) {
            console.log(openc_id)
            let that = this;
            let get_elective_api = "Student/Elective";
            var form = new FormData();
            form.append("openc_id", openc_id);
            that.axios({
                method: "post",
                url: get_elective_api,
                headers: { Authorization: localStorage.getItem("token")},
                data: form
                }).then(res => {
                if(res.data.status == 200) {
                    alert(res.data.status + ": " + res.data.msg)
                }
                else {
                    alert(res.data.status + ": " + res.data.msg)
                }
                console.log(res.data.status + ": " + res.data.msg)
                })
        }
    },
    // created:function(){
    //     this.get_elective();
    // }
}
</script>

<style>
</style>
