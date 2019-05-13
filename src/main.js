import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import axios from 'axios'
import VueAxios from 'vue-axios'
axios.defaults.baseURL = 'http://lz-legal-aid.cn:5000/';
Vue.config.productionTip = false;
Vue.use(VueAxios, axios);


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
