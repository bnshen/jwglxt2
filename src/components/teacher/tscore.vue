<template>
<div id = 'tscore'>
    <div>
      <input id="openc_id" placeholder="课程号">
      <button @click="score()">查询分数</button>
    </div>
    <display :display_data="stuscore"/>
    <div id="new-score-outter" v-if ="stuscore.length">
      修改分数
      <table border="1" id="new-score-table" v-if="stuscore">
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
</template>

<script>
import display from "@/components/display.vue";
export default {
    name : 'tscore',
    components:{
        display
    },
    data(){
        return{
            stuscore:[]
        }
    },
    methods:{
            score: function() {
      let _openc_id = document.getElementById("openc_id").value;
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
        _eid.push(eid[i].value);
        _efeg.push(efeg[i].value);
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
          elevtive_regular_grade: _efeg,
          elevtive_final_exam_grade: _erg
        }
      }).then(function(response) {
        console.log(response);
      });
    }
    }
}
</script>

<style>

</style>
