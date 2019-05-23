<template>
  <div id="login" class="about">
    <h1 id = "logintitle">上海大学教务管理系统</h1>
    <br/>
    <div id="login-outer-box">
        <!--
      <div>
        <div class="form-check">
          <input class="form-check-input" name="login-options" type="radio">
          <label class="form-check-label">学生登陆</label>
        </div>
        <div class="form-check">
          <input class="form-check-input" name="login-options" type="radio">
          <label class="form-check-label">教师登陆</label>
        </div>
        <div class="form-check">
          <input class="form-check-input" name="login-options" type="radio">
          <label class="form-check-label">管理员登陆</label>
        </div>
      </div>
      -->
      <div class = "container">
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text" id="basic-addon1">学号/工号</span>
        </div>
        <input
          type="text"
          class="form-control"
          placeholder="Username"
          aria-label="Username"
          aria-describedby="basic-addon1"
          v-model="login_username"
        >
      </div>
      <div class="input-group mb-3">
        <div class="input-group-prepend">
          <span class="input-group-text" id="basic-addon1">密码</span>
        </div>
        <input
          type="text"
          class="form-control"
          placeholder="Password"
          aria-label="Username"
          aria-describedby="basic-addon1"
          v-model="login_password"
        >
      </div>
      </div>
      <button class="btn btn-outline-secondary" type="button" @click="_login()">登陆</button>
    </div>
  </div>
</template>


<script>
export default {
  name: "login",
  data() {
    return {
      login_username: "",
      login_password: ""
    };
  },
  methods: {
    _login: function() {
      let api = "login";
      let _this = this;
      this.axios
        .post(api, {
          user_name: this.login_username,
          password: this.login_password
        })
        .then(function(response) {
          if (response.data.status != 200) alert("用户名或密码错误！");
          else {
            // console.log(response.data.data);
            alert("登陆成功！");
            _this.$store.commit("addRoles", {
              roles: response.data.data.catagory_name
            });
            localStorage.setItem(
              "user_info",
              JSON.stringify(response.data.data.user_info)
            );
            localStorage.setItem("token", response.data.data.token);
            localStorage.setItem("roles", response.data.data.catagory_name);
            console.log(response);
            window.location.href = "/#/" + response.data.data.catagory_name.toLowerCase();
          }
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>


<style>
div {
  text-align: center;
}

input {
  position: relative;
  margin: auto;
  padding: auto;
}

#login-outer-box
{
    margin: 0 auto;
    padding: 0 auto;
    width: 50%;
}
#logintitle{
  margin-top: 20%; 
}
</style>
