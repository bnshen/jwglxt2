<template>
    <div id = 'display'>
    <div id = 'display-outter'>
        <div class="container">
        <table class = "table" border="1" id = 'display-table' v-if = "display_data">
            <tr>
               <th v-for = "(value,key) in display_data[0]" v-bind:key = "key"> 
                   <span v-if="e2c != undefined">
                        {{e2c[key]}}
                    </span>
                    <span v-else>
                        {{key}}
                    </span>
                </th> 
            </tr>
            <tr v-for = "(item1, key1) in display_data" v-bind:key = "key1">
                <td v-for = "(c,key) in item1" v-bind:key = "key">
                    {{c}}
                </td>
            </tr>
        </table>
        </div>
    </div>
    </div>
</template>

<script>
export default {
    name:'display',
    props: {
        display_data:Object,
        e2c:Object
    },
    methods: {
        test() {
            console.log(this.display_data)
        }
    }
}
</script>

<style>

</style>
