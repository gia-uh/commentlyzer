<template>
     <v-data-table :headers="headers"
               :items="items"
               item-key="id"
               :loading="loading"
               hide-actions
               expand
               class="elevation-1">
  <template slot="headerCell" slot-scope="props">
      <v-tooltip bottom>
        <span slot="activator" :class="props.header.class" style="font-size: 20px;">
          {{ props.header.text }}
        </span>
        <span class="props.header.class" style="font-size: 20px;">
          {{ props.header.text }}
        </span>
      </v-tooltip>
    </template>
  <template slot="items" slot-scope="props">
    <tr >
      <td class="text-xs-left">{{ props.item.name }}</td>
      <td class="text-xs-right align-content-right">
        <span>
        {{ props.item.count.total }}
        <peity :type="'pie'" :options="pcolors" :data="lineData(props.item.count)"></peity>
        </span>
      </td>
    </tr>
  </template>
 </v-data-table>
</template>


<script>
import Peity from 'vue-peity';
import {color_scheme_pie} from '../main.js';
//import VueChartkick from 'vue-chartkick'
export default {
  components: {
    Peity
  },
  name: "relevantEntities",
  props: ["items"],
  data() {
    return {
      headers: [
        { text: "Entidad", value: "name", sortable: false, style:"font-size: 20px;", class: "text-xs-left" },
        { text: "Menciones", value: "count", sortable: false, align: "right", style:"font-size: 20px;", class: "text-xs-right"},
        // { text: "Actions", value: "id", sortable: false }
      ],
      loading: false,
      pcolors: { 'fill': color_scheme_pie}
    };
  },
  methods: {
    lineData (data) {
      return `${data.Negativo},${data.Neutro},${data.Objetivo},${data.Positivo},`

      //return "5,5,5";
    }
  },
  created() {
  }
};
</script>

<style scoped>
table.v-table thead th {
    font-size: 15px;
    font-weight: 500;
}
</style>
