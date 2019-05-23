<template>
  <div id="sinfo">
    <p> 个人信息 </p>
    <div id = 'display-info'>
        <div class='container'>
        <table class="table table-borderless" border="1" >
        <tr id="dis-info" v-for="(val, key) in info" v-bind:key="key">
            <td >
                {{ e2c[key] }}
            </td>
            <td>
                {{val}}
                </td>
        </tr>
        </table>
        </div>
    </div>
  </div>
</template>

<script>
import display from "@/components/display.vue";
// import { constants } from 'crypto';
// import { toASCII } from 'punycode';
export default {
    components:{
        
    },
    data(){
        return{
            info: {},
            changeinfo: {},
            e2c:{
                'department_id':'院系号',
                'department_name':'院系名',
                'student_birthaddress':'出生地',
                'student_birthtime':'出生日期',
                'student_class':'班级号',
                'student_grade':'当前年级',
                'student_name':'姓名',
                'student_no':'学号',
                'student_sex':'性别',
                'student_tel':'联系方式',
                'student_user_id':'student_user_id'
            }
        }
    },
    methods:{
        get_info() {
            let that = this;
            that.info = JSON.parse(localStorage.getItem("user_info"));
            that.changeinfo = that.info;
        }
    },
    created:function(){
        this.get_info();
    }
}
</script>

<style>
</style>
