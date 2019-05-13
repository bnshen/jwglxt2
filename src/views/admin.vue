<template>
    <div id = 'admin'>
        <h1 class = 'about'> this is admin page</h1>
        <router-link to="/admin/queryuserinfo">queryuserinfo</router-link>  | 
        <router-link to="/admin/changeuserinfo">changeuserinfo</router-link> | 
        <router-link to="/admin/opencourses">opencourses</router-link> |
        <router-link to="/admin/addnewcourse">addnewcourse</router-link> | 
        <router-link to="/admin/opencourse">openNEWcourse</router-link>
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

</style>
