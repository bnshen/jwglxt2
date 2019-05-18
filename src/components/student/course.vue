<template>
  <div id="scourse">
    <div id="scourse_table">
        <p> 已选课程 </p>
        <div id = 'display-scoure_table'>
            <table border="1" id = 'display-table' v-if = "elective[0]">
                <tr>
                    <th v-for = "(value,key) in elective[0]" v-bind:key = "key"> 
                        {{key}}
                    </th> 
                    <th> 
                        退课
                    </th> 
                </tr>
                <tr v-for = "(value, key) in elective" v-bind:key = "key">
                    <td v-for = "(val ,keyitem) in value" v-bind:key = "keyitem">
                        {{val}}
                    </td>
                    <td>
                        <button @click="delete_course(value.openc_id)"> 删课 </button>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    
    <div id="scourse_timetable">
        <p> 课程表 </p>
        <div id = 'display-scoure_table'>
            <table border="1" id = 'display-table' v-if = "timetable2">
                <tr>
                    <th v-for = "(value,key) in timetable2[0]" v-bind:key = "key"> 
                        {{key}}
                    </th> 
                </tr>
                <tr v-for = "(value, key) in timetable2" v-bind:key = "key">
                    <td v-for = "(val ,keyitem) in value" v-bind:key = "keyitem">
                        {{val}}
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
// import qs from "qs"
export default {
    // components:{
    //     display
    // },
    inject: ['reload'],
    data(){
        return{
            elective: {},
            timetable: {},
            timetable2: {}
        }
    },
    methods:{
        get_elective() {
            for(var i = 0; i <= 12; i ++) {
                this.timetable[i] = {};
                this.timetable[i].Class = (i+1).toString();
                this.timetable[i].Mon = "";
                this.timetable[i].Tue = "";
                this.timetable[i].Wed = "";
                this.timetable[i].Thu = "";
                this.timetable[i].Fri = "";
                this.timetable[i].Sat = "";
                this.timetable[i].Sun = "";
            };
            let that = this;
            let get_elective_api = "Student/Elective";
            that.axios({
                method: "get",
                url: get_elective_api,
                headers: { Authorization: localStorage.getItem("token") }
                }).then(res => {
                if(res.data.status == 200) {
                    var alp = 65;
                    var p;
                    that.elective = res.data.data.Elective;
                    for(var key in that.elective) {
                        // console.log(that.elective[key]);
                        p = String.fromCharCode(alp++);
                        that.elective[key].order = p;
                        var time = that.elective[key].openc_time.split(" ");
                        for(var i = Number(time[1]); i <= Number(time[3]); i ++) {
                            this.timetable[i-1][time[0]] = that.elective[key].order
                        }
                    };
                    this.timetable2 = this.timetable
                }
                else {
                    alert(res.data.status + ": " + res.data.msg)
                }
                console.log(res.data.status + ": " + res.data.msg)
                })
        },
        delete_course(openc_id) {
            console.log(openc_id)
            let that = this;
            let get_elective_api = "Student/Elective";
            var form = new FormData();
            form.append("openc_id", openc_id);
            that.axios({
                method: "delete",
                url: get_elective_api,
                headers: { Authorization: localStorage.getItem("token")},
                data: form
                }).then(res => {
                if(res.data.status == 200) {
                    alert(res.data.status + ": " + res.data.msg)
                    this.get_elective();
                    this.reload();
                }
                else {
                    alert(res.data.status + ": " + res.data.msg)
                }
                console.log(res.data.status + ": " + res.data.msg)
                })
        }
    },
    created:function(){
        this.get_elective();
    }
}
</script>

<style>
</style>
