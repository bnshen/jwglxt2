<template>
    <div id = 'queryuserinfo'>
        <div>
            <label>
            <input id = 'studentinfo' type="radio" name="usertype" @click="userinfo('Student')">学生信息
            </label>
            <label>
            <input type="radio" name="usertype" @click="userinfo('Teacher')">教师信息
            </label>
        </div>
        <display :display_data="users"></display>
        
    </div>
</template>

<script>
import display from "@/components/display.vue";
export default {
    name:'queryuserinfo',
    components:{
        display
    },
    data(){
        return{
            users:{},
        }
    },
    methods:{
        userinfo:function(type){
            let that = this;
            let api = "Admin/userinfo";
            this.axios({
            method: "get",
            url: api,
            headers: { Authorization: localStorage.getItem("token") },
            params:{
                catagory_name:type
            }
            }).then(function(response) {
            console.log(response);
            that.users = response.data.data.userinfo;
        });
        },
    },
    mounted:function(){
        document.getElementById('studentinfo').click();
    }
}
</script>

<style>

</style>
