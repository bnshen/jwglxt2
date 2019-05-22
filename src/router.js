import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home";
import login from "./views/login";
import student from "./views/student";
import teacher from "./views/teacher";
import admin from "./views/admin";
import scourse from "@/components/student/course";
import selective from "@/components/student/elective";
import sinfo from "@/components/student/info";
import sgrade from "@/components/student/grade";
import tcourse from "@/components/teacher/tcourse.vue";
import tscore from "@/components/teacher/tscore.vue";
import queryuserinfo from "@/components/admin/queryuserinfo.vue";
import changeuserinfo from "@/components/admin/changeuserinfo.vue";
import opencourses from "@/components/opencourses.vue";
import addnewcourse from "@/components/admin/addnewcourse.vue";
import opencourse from "@/components/admin/opencourse.vue";
import err from "@/views/err.vue"
Vue.use(Router);


let routerMap = [
    {
      path: "/",
      name: "home",
      component: login,
      meta:['Teacher','Student','Administrator','anonymous']
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/About.vue"),
      meta:['Teacher','Student','Administrator','anonymous']
    },
    {
      path: "/login",
      name: "login",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/login.vue"),
      meta:['Teacher','Student','Administrator','anonymous']
    },
    {
      path: "/student",
      name: "student",
      component: student,
      meta: ['Student'],
      children: [
        {
          path: "course",
          component: scourse,
          meta: ['Student'],
        },
        {
          path: "elective",
          component: selective,
          meta: ['Student'],
        },
        {
          path: "info",
          component: sinfo,
          meta: ['Student'],
        },
        {
          path: "grade",
          component: sgrade,
          meta: ['Student'],
        }
      ]
    },
    {
      path:"/teacher",
      name:"teacher",
      component:teacher,
      meta:['Teacher'],
      children: [
        {
          // 当 /user/:id/profile 匹配成功，
          // UserProfile 会被渲染在 User 的 <router-view> 中
          path: 'tcourse',
          component: tcourse,
          meta:['Teacher']
        },
        {
          // 当 /user/:id/posts 匹配成功
          // UserPosts 会被渲染在 User 的 <router-view> 中
          path: 'tscore',
          component: tscore,
          meta:['Teacher']
        }
      ]
    },
    {
      path:"/administrator",
      name:"admin",
      component:admin,
      meta:['Administrator'],
      children:[
        {
          path:'queryuserinfo',
          component:queryuserinfo,
          meta:['Administrator']
        },
        {
          path:'changeuserinfo',
          component:changeuserinfo,
          meta:['Administrator']
        },
        {
          path:'opencourses',
          component:opencourses,
          meta:['Administrator']
        },
        {
          path:'addnewcourse',
          component:addnewcourse,
          meta:['Administrator']
        },
        {
          path:'opencourse',
          component:opencourse,
          meta:['Administrator']
        }
      ]
    },
    {
      path: '/error',
      name: 'error',
      component: err,
      meta: ['Teacher', 'Student', 'Administrator','anonymous']
    },

  ]
let route =  new Router({
    routes: routerMap
  })


route.beforeEach((to, from, next) => {
  //获取用户权限信息，为空即没登录，跳转至登录页
  if (to.path === '/login') {
    next();
  } else {
    let role = window.localStorage['roles'] || route.app.$options.store.state.roles;
    console.log(role);
    if (role === '') {
      next('/login');
    } else {
      if(to.matched.every(item => item.meta.indexOf(role) > -1)) {
        next();
      } else {
        next('/error');
      }
    }
  }
});
export default route;