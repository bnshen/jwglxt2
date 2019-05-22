<template>
    <div id = 'err'>
        <h1> 你并无权限访问此页 </h1>
        <br/>
        <h2> 请先 <router-link to="/login">登陆</router-link></h2>
        
    </div> 
</template>

<script>
export default {
    name:'err'
}
</script>

<style>
h1{
    text-align:  center;
}
</style>
