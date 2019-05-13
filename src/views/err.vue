<template>
    <div id = 'err'>
        <h1> Seems you come to the wrong page :) </h1>
        <br/>
        <h2> Please go to <router-link to="/login">login</router-link> page first</h2>
        
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
