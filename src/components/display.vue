<template>
    <div id = 'display'>
    <div id = 'display-outter'>
        <table border="1" id = 'display-table' v-if="display_data">
            <tr>
               <th v-for = "(value,key) in display_data[0]" v-bind:key="key"> 
                   {{key}}
                </th> 
            </tr>
            <tr v-for="index in display_data" v-bind:key="index">
                <td v-for="c in index" v-bind:key="c">
                    {{c}}
                </td>
            </tr>
        </table>
    </div>
    </div>
</template>

<script>
export default {
    name:'display',
    props: {
    display_data:Object
  }
}
</script>

<style>

</style>
