<template>
  <div id="app">
    <div id="nav">
      <button class = "btn btn-primary" id = 'logout' @click="logout()"> 安全退出 </button>
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'Login',
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
