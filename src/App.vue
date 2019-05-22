<template>
  <div id="app">
    <div id="nav">
      <router-link to="/login">登陆</router-link> |
      <router-link to="/student">学生</router-link> |
      <router-link to="/teacher">教师</router-link> |
      <router-link to="/administrator">管理员</router-link>
      <button id = 'logout' @click="logout()"> 安全退出 </button>
       
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  provide(){
    return{
      reload:this.reload
    }
  },
  data(){
    return{
      isRouterAlive:true
    }
  },
  methods:{
      reload(){
      this.isRouterAlive=false;
      this.$nextTick(function(){
        this.isRouterAlive=true;
      })
    },
    logout(){
      localStorage.setItem('roles','anonymous');
      localStorage.setItem('token','');
      this.$store.commit("addRoles", {
              roles: 'anonymous'
            });
      alert('退出成功');
      window.location.href ="/";

    }
  }
    
}
</script>

<style lang="scss">
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
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
#logout{
  float: right
}
</style>
