import Vue from "vue";
import App from "./App.vue";
import Login from "./Login.vue"
import router from "./router";
import store from "./store";

import axios from 'axios'
import VueAxios from 'vue-axios'
let _mode = 'p';
if (_mode == 'd')
  axios.defaults.baseURL = 'http://localhost:5000/';
else if(_mode == 'p')
  axios.defaults.baseURL = 'http://lz-legal-aid.cn:5000/';

Vue.config.productionTip = false;
Vue.use(VueAxios, axios);

import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

new Vue({
  router,
  store,
  render: h => h(Login)
}).$mount("#app");
