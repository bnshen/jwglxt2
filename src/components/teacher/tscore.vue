<template>
  <div id="tscore">
    <div>
      <div class='container'>
      <select class="custom-select" id="openc_select">
        <option v-for="openc_id in openc_ids" v-bind:key="openc_id">
            {{id2no[openc_id]}}
        </option>
      </select>
      <br/>
      <div class='container'>
      <button id = "score_btn" class="btn btn-primary" @click="score()">查询分数</button>
      </div>
      <br/>
      <h1 v-if="final_scores_grouped.length == 0">
        课程人数为0
      </h1>
      </div>
    </div>
    
    <display v-if ="stuscore" :display_data="stuscore" :e2c="e2c"/>
    <hr/>
    <visualize v-if="final_scores_grouped.length > 0" :display_data="final_scores_grouped" 
      :labels="final_scores"/>
    
    <hr/>
    <div id="new-score-outter" v-if="stuscore.length">
      修改分数
      <div class="container">
      <table class="table" border="1" id="new-score-table" v-if="stuscore">
        <tr>
          <th>选课号</th>
          <th>期末成绩</th>
          <th>平时成绩</th>
        </tr>
        <tr v-for="(value,key) in stuscore" v-bind:key="key">
          <td>
            <input class="eid" :value="value['elective_id']">
          </td>
          <td>
            <input class="efeg" :value="value['elevtive_final_exam_grade']">
          </td>
          <td>
            <input class="erg" :value="value['elevtive_regular_grade']">
          </td>
        </tr>
      </table>
      <button  class="btn btn-primary" @click="update_score()">全部提交</button>
      <br/>
      <br/>
      </div>
    </div>
  </div>
</template>

<script>
import display from "@/components/display.vue";
import visualize from "@/components/visualize.vue";
export default {
  name: "tscore",
  components: {
    display,
    visualize
  },
  computed:{
  },
  data() {
    return {
      stuscore: {},
      openc_ids: [],
      no2id:{},
      id2no:{},
      final_scores:[],
      final_scores_grouped:[],
      e2c:{
          'elective_id':'选课号',
          'elevtive_final_exam_grade'	:'期末成绩',
          'elevtive_regular_grade':'平时成绩',
          'elevtive_total_grade':'总评成绩',
          'student_grade':'学生信息',
          'student_name':'姓名',
          'student_no':'学号',
          'student_sex'	:'性别',
          'student_tel':'联系方式'
      }
    };
  },
  methods: {
    course: function() {
      let that = this;
      let api = "Teacher/courses";
      that.axios({
        method: "get",
        url: api,
        headers: { Authorization: localStorage.getItem("token") }
      }).then(function(response) {
        console.log(response);
        let _openC = response.data.data.OpenC;
        for(let index in _openC)
        {
          that.openc_ids.push(_openC[index]['openc_id']);
          that.no2id[_openC[index]['course_name'] + 
            '|' + _openC[index]['openc_time']] = _openC[index]['openc_id'];
          that.id2no[_openC[index]['openc_id']] = _openC[index]['course_name'] + 
            '|' + _openC[index]['openc_time']
        }
      });
    },
    score: function() {
      this.final_scores_grouped=[];
      let _index = document.getElementById("openc_select").selectedIndex;
      let _options = document.getElementById("openc_select").options;
      let _openc_id = _options[_index].value;
      _openc_id = this.no2id[_openc_id];
      let that = this;
      let api = "Teacher/courses/scores";
      this.axios({
        method: "get",
        url: api,
        headers: { Authorization: localStorage.getItem("token") },
        params: {
          openc_id: _openc_id
        }
      }).then(function(response) {
        console.log(response);
        that.stuscore = response.data.data.scores;
        let _final_scores = [];
        for(let index=0;index<that.stuscore.length;index++)
        {
          _final_scores.push(that.stuscore[index]['elevtive_final_exam_grade']);
        }
        that.final_scores = _final_scores;
        //group final_scores
        let _grouped = {
          'A':0,
        'B':0,
        'C':0,
        'D':0,
        'F':0
        };
        for(let index in _final_scores){
          let cur = _final_scores[index];
          if(cur >= 90){
            _grouped['A'] += 1;
          }
          else if(cur >=80)
            _grouped['B'] += 1;
          else if(cur >=70)
            _grouped['C'] +=1;
          else if (cur >=60)
            _grouped['D'] +=1;
          else 
            _grouped['F'] +=1;
        }
        if (_final_scores.length > 0){
        that.final_scores_grouped[0] = _grouped['A'];
        that.final_scores_grouped[1] = _grouped['B'];
        that.final_scores_grouped[2] = _grouped['C'];
        that.final_scores_grouped[3] = _grouped['D'];
        that.final_scores_grouped[4] = _grouped['F'];
        }

      });
      
    },
    update_score: function() {
      let eid = document.getElementsByClassName("eid");
      let efeg = document.getElementsByClassName("efeg");
      let erg = document.getElementsByClassName("erg");
      let _eid = [],
        _efeg = [],
        _erg = [];
      for (let i = 0; i < eid.length; i++) {
        if (eid[i].value == "")
          _eid.push("0");
        else 
          _eid.push(eid[i].value);
        if (efeg[i].value == "")
          _efeg.push("0");
        else 
          _efeg.push(efeg[i].value);
        if (erg[i].value == "")
          _erg.push("0");
        else 
          _erg.push(erg[i].value);
      }
      let that = this;
      let api = "Teacher/courses/scores";
      this.axios({
        method: "put",
        url: api,
        headers: { Authorization: localStorage.getItem("token") },
        data: {
          elective_id: _eid,
          elevtive_regular_grade: _erg,
          elevtive_final_exam_grade: _efeg
        }
      }).then(function(response) {
        if (response.data.status == 200) alert("修改成功！");
        that.score();
        console.log(response);
      });
    }
  },
  created:function(){
    this.course();
  }
};
</script>

<style>
#openc_select{
  margin-top: 2%;
}
#score_btn{
  padding: 0 auto;
  margin:  0 auto;
  margin-top: 2%;
}
</style>
