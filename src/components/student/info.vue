<template>
  <div id="sinfo">
    <p> 个人信息 </p>
    <div id = 'display-info'>
        <ul id="dis-info">
            <li v-for="(val, key) in info">
                {{ key }} : {{ val }}
            </li>
        </ul>
    </div>
  </div>
</template>

<script>
import display from "@/components/display.vue";
// import { constants } from 'crypto';
// import { toASCII } from 'punycode';
export default {
    components:{
        display
    },
    data(){
        return{
            info: {},
            changeinfo: {}
        }
    },
    methods:{
        get_info() {
            let that = this;
            that.info = JSON.parse(localStorage.getItem("user_info"));
            that.changeinfo = that.info;
        }
    },
    created:function(){
        this.get_info();
    }
}
</script>

<style>
</style>
