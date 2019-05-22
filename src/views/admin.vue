<template>
    <div id = 'admin'>
        <div id='nav'>
        <h4 id='a-welcome'>管理员系统</h4>
        <router-link to="/administrator/queryuserinfo">信息管理</router-link>  | 
        <router-link to="/administrator/changeuserinfo">信息修改</router-link> | 
        <router-link to="/administrator/opencourses">已开课程</router-link> |
        <router-link to="/administrator/addnewcourse">新增课程</router-link> | 
        <router-link to="/administrator/opencourse">新开课程</router-link>

        </div>
        <hr/>
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

<style lang='scss'>
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
#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
#a-welcome{
    float: left;
}
</style>
