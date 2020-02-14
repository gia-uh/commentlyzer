import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@fortawesome/fontawesome-free/css/all.css'
import VueLodash from 'vue-lodash'
import Chart from 'chart.js'
import VueMoment from 'vue-moment'

var SocialSharing = require('vue-social-sharing');
Vue.use(SocialSharing);

// Moment init
const moment = require('moment')
require('moment/locale/es')
Vue.use(VueMoment, {
    moment
})

export const color_scheme = ['red', 'green', 'gray','blue','orange'];
export const color_scheme_pie = [color_scheme[3], color_scheme[0], color_scheme[4], color_scheme[1]];

Vue.use(VueLodash) // options is optional
import VueChartkick from 'vue-chartkick'
import EntitiesTable from './components/EntitiesTable.vue'
VueChartkick.options = {colors: color_scheme};

Vue.use(VueChartkick, { adapter: Chart })
Vue.config.productionTip = false
Vue.component("entities", EntitiesTable)

import wordcloud from './components/WordCloud.vue'
Vue.component("wordcloud", wordcloud)

const development = process.env.NODE_ENV === 'development';
export const baseUrl = development ? 'http://localhost:8000/api' : '/api';
export const baseUrl2 = development ? 'http://localhost:8000/api' : '/api';
export var data = { url: "" }
export const eventBus = new Vue();

export function getdata(url) {

    return fetch(baseUrl + url).then(response => {

        if (response.status != 200) {
            //console.log("Error Do stuff here");
            //console.log(response)
        }

        return response.json().then(json => {
            //console.log(json)
            return json;
        });
    });
}

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')