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
      </div>
    </div>
    <display v-if ="stuscore" :display_data="stuscore"/>
    <!-- 
      <visualize v-if="final_scores.length > 0" :display_data="final_scores" 
      :labels="final_scores"/>
      -->

    <div id="new-score-outter" v-if="stuscore.length">
      修改分数
      <div class="container">
      <table class="table" border="1" id="new-score-table" v-if="stuscore">
        <tr>
          <th>elective_id</th>
          <th>elevtive_final_exam_grade</th>
          <th>elevtive_regular_grade</th>
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
          <td v-if="key == stuscore.length-1">
            <button @click="update_score()">全部提交</button>
          </td>
        </tr>
      </table>
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
      final_scores:[]
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
</style>
