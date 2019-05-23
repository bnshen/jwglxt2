<template>
  <div id="opencourse">
    <display :display_data="courseinfo" :e2c='e2c'/>
    <br/>
    <div id="opencourse_outter">
      <div class="container">
      <table border="1" class="table">
        <tr>
          <th>信息</th>
          <th>值</th>
        </tr>
        <tr>
          
            <td>
              课程号
          </td>
          <td>
            <select id = "course_cur_no">
            <option v-for="course in courseinfo" v-bind:key="course" :value="course.course_no">
              {{course.course_no}}
            </option>
          </select>
          </td>
      
        </tr>

        <tr v-for="value in opencourse_info" v-bind:key="value" v-if="value!='course_id'">
          <td>{{e2c[value]}}</td>
          <td>
            <input type="text" :name="value" :id="value">
          </td>
        </tr>
      </table>
      </div>
      <br/>
      <button class="btn btn-primary" @click="add">提交</button>
    </div>
  </div>
</template>

<script>
import display from "@/components/display.vue";
export default {
  name: "opencourse",
  components:{
        display
    },
  computed:{

  },
  data() {
    return {
      opencourse_info: [
        'course_id',
        'teacher_id',
        'openc_time',
        'openc_address',
        'openc_maxnum',
        'openc_QA_time',
        'openc_QA_address'
      ],
       e2c:{
                'course_credit':'学分',
                'course_hour':'学时',
                'course_name':'课程名',
                'course_no':'课程号',
                'openc_QA_time':'答疑时间',
                'openc_address':'上课地点',
                'openc_available':'是否可选',
                'openc_curnum':'当前人数',
                'openc_id':'课程id',
                'openc_maxnum':'最大人数',
                'openc_time':'上课时间',
                'teacher_id':'教师号',
                'teacher_name':'教师姓名',
                'order':'顺序',
                'course_catagory':'课程类别',
                'department_id':'院系号',
                'course_final_exam_precentage':'期末成绩比例',
                'course_grade':'选课年级',
                'course_id':'课程id',
                'openc_QA_address':'答疑地点'
            },
      courseinfo : {},
      course_no2id:{}
    }
  },
  methods:{
      get_id_from_no:function(course_no){
        console.log(course_no);
        for(var course in this.courseinfo)
          if(course.course_no == course_no)
            {
              document.getElementById('course_id').value = course.course_id;
              break;
            }
      },
      add: function() {
      this.get_dict();
      let api = "Admin/openc";
      let _data = new FormData();
      let cur_info = this.opencourse_info;
      for (let i = 1; i < cur_info.length; i++) {
        _data.set(cur_info[i], document.getElementById(cur_info[i]).value);
      }
      let ctx = document.getElementById('course_cur_no').options
      let index = ctx.selectedIndex;
     
      _data.set('course_id',this.course_no2id[ctx[index].value]);
      this.axios({
        method: "post",
        url: api,
        headers: {
          Authorization: localStorage.getItem("token"),
          "Content-Type": "multipart/form-data"
        },
        data: _data
      }).then(function(response) {
        console.log(response);
      });
    },
    query:function(){
      let _this = this;
      let api = "Admin/courses";
      this.axios({
        method:"get",
        url:api,
        headers:{
          Authorization:localStorage.getItem("token")
        }
      }).then(function(response){
        console.log(response);
        _this.courseinfo = response.data.data.courseinfo;
      });
    },
    get_dict:function(){
      console.log(this.courseinfo);
      for(var index in this.courseinfo)
        {
          this.course_no2id[this.courseinfo[index].course_no] = this.courseinfo[index].course_id;
        }
    }
  },
  created:function()
  {
    this.query();
  }
};
</script>

<style>
</style>
