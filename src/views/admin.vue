<template>
    <div id = 'admin'>
        <h1 class = 'about'>管理员系统</h1>
        <router-link to="/administrator/queryuserinfo">信息管理</router-link>  | 
        <router-link to="/administrator/changeuserinfo">信息修改</router-link> | 
        <router-link to="/administrator/opencourses">已开课程</router-link> |
        <router-link to="/administrator/addnewcourse">新增课程</router-link> | 
        <router-link to="/administrator/opencourse">新开课程</router-link>

        <br/>
        <router-view/>
        
    </div>

    
</template>

<script>
export default {
    name:'admin',
    components:{
    },
    data(){
        return {
            
        }
    },
    methods:{
    }
}
</script>

<style>
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
table{
    margin: 0 auto;
}

</style>
