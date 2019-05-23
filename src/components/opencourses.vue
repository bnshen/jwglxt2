<template>
    <div id = 'opencourses'>
        <display :display_data = "openC" :e2c="e2c"/>
    </div>
</template>

<script>
import display from "@/components/display.vue";
export default {
    name:'opencourses',
    data(){
        return{
            openC:{},
             e2c:{
                'course_credit':'学分',
                'course_hour':'学时',
                'course_name':'课程名',
                'course_no':'课程号',
                'openc_QA_time':'答疑时间',
                'openc_address':'上课地点',
                'openc_available':'是否可选',
                'openc_curnum':'当前人数',
                'openc_id':'课程id',
                'openc_maxnum':'最大人数',
                'openc_time':'上课时间',
                'teacher_id':'教师号',
                'teacher_name':'教师姓名',
                'order':'顺序'
            }
        }
    },
    components:{
        display
    },
    methods:{
        getopenC:function(){
            let api = 'OpenC/query';
            let that = this;
            this.axios({
                method:'get',
                url: api
            }).then(function(Response)
            {
                that.openC = Response.data.data.OpenC;
            });
        }
    },
    created:function(){
        this.getopenC();
    }
}
</script>

<style>

</style>
