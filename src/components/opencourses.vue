<template>
    <div id = 'opencourses'>
        <display :display_data = "openC"/>
    </div>
</template>

<script>
import display from "@/components/display.vue";
export default {
    name:'opencourses',
    data(){
        return{
            openC:{}
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
