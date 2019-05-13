<template>
    <div id = 'login' class = 'about'>
        <h1>this is the login page</h1>
    

    <div id = 'login-outer-box'>
        <div>
            <label>
                <input name = 'login-options' type="radio"/>
                学生登陆
            </label>
            <label>
                <input name = 'login-options' type="radio"/>
                教师登陆
            </label>
            <label>
                <input name = 'login-options' type="radio"/>
                管理员登陆
            </label>
        </div>
        <input class = 'login-input' placeholder="username" v-model="login_username"/>
        <br/>
        <input class = 'login-input' placeholder="password" v-model="login_password"/>
        <br/>
        <button class = 'login-button' type="button" @click="_login()">login</button>
    </div>

    </div>
</template>


<script>
export default {
    name: "login",
    data(){
        return{
            login_username:"",
            login_password:"",
        }
    },
    methods:{
        _login:function(){
            let api = "login";
            let _this = this;
            this.axios.post(api, {
                user_name:this.login_username,
                password:this.login_password
            })
            .then(function (response) {
                if(response.data.status != 200)
                    alert('用户名或密码错误！')
                else
                {
                alert('登陆成功！');
                _this.$store.commit('addRoles', {
                    roles: response.data.data.catagory_name
                    });
                localStorage.setItem('token',response.data.data.token)
                localStorage.setItem('roles',response.data.data.catagory_name)
                console.log(response);
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }

}
</script>


<style>
div{
    text-align: center;
}

.login-input .login-button{
    position: relative;
    margin: auto;
    padding: auto;
}
</style>
