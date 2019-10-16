<template>
  <!-- <v-container text-xs-center grid-list-md fluid> -->
  <v-layout justify-center>
    <v-flex xs10>
    <v-slide-y-transition mode="out-in">
      <v-card tile>
      <v-container fluid grid-list-md>
        <v-layout align-center justify-space-around>
          <v-text-field
              light
              placeholder="Buscar"
              v-model="pagefilt"
              align-center
              v-on:keyup.enter="gotarticle"
          ></v-text-field>

          <v-btn icon @click.stop="gotarticle">
            <v-icon>fas fa-search</v-icon>
          </v-btn>
        </v-layout>
      <v-layout row wrap>
        <v-flex v-for="(article, index) in articles" class="is-flex" :key="index" xs12  sm6 md4 lg3 >
          <v-card fill-height fluid pa-2>
            <v-container fill-height fluid pa-2>
            <v-layout row wrap fill-height>
              <v-flex  lg12 md12 sm12 xs12 >
<span class="grey--text centerv">
                  {{article.media}}
                </span>
              </v-flex>
              <v-flex  lg12 md12 sm12 xs12 >
                <span class="grey--text">
                  Publicado: {{ article.pub_date | moment('calendar') }}
                </span><br>
                <span class="grey--text">
                  Actualizado: {{ article.last_update | moment('from', 'now') }}
                </span>
              </v-flex>
              <v-flex  lg12 md12 sm12 xs12 >
                <v-img :src="article.img?article.img:getmedia(article.media)" max-height="200"></v-img>
              </v-flex>

              <v-card-title>
                <div>
                  <a text-align="center" class="headline" @click="getpage(article.id)">{{article.title}}</a>
                </div>
              </v-card-title>
              <v-card-actions>
                <v-btn flat color="purple" @click="gotosite(article.url)">Ver En&nbsp;&nbsp;
  <svg v-if="getmedian(article.media)==0"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:cc="http://creativecommons.org/ns#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:svg="http://www.w3.org/2000/svg"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
    xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
    version="1.0"
    width="32px"
    height="32px"
    viewBox="0 0 469.000000 448.000000"
    preserveAspectRatio="xMidYMid meet"
    id="svg4075"
    sodipodi:docname="cubadebate.svg"
    inkscape:version="0.92.4 (5da689c313, 2019-01-14)">
    <defs
      id="defs4079" />
    <sodipodi:namedview
      pagecolor="#ffffff"
      bordercolor="#666666"
      borderopacity="1"
      objecttolerance="10"
      gridtolerance="10"
      guidetolerance="10"
      inkscape:pageopacity="0"
      inkscape:pageshadow="2"
      inkscape:window-width="3840"
      inkscape:window-height="2053"
      id="namedview4077"
      showgrid="false"
      inkscape:snap-midpoints="true"
      inkscape:snap-to-guides="false"
      inkscape:snap-grids="false"
      inkscape:snap-page="true"
      inkscape:snap-text-baseline="true"
      inkscape:zoom="2.9748884"
      inkscape:cx="241.23542"
      inkscape:cy="298.66667"
      inkscape:window-x="0"
      inkscape:window-y="55"
      inkscape:window-maximized="1"
      inkscape:current-layer="svg4075" />
    <metadata
      id="metadata4063">
  Created by potrace 1.14, written by Peter Selinger 2001-2017
  <rdf:RDF>
    <cc:Work
      rdf:about="">
      <dc:format>image/svg+xml</dc:format>
      <dc:type
        rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
      <dc:title></dc:title>
    </cc:Work>
  </rdf:RDF>
  </metadata>
    <g
      transform="translate(0.000000,448.000000) scale(0.100000,-0.100000)"
      id="g4073"
      stroke="none"
      fill="#000000"
      style="image-rendering:optimizeQuality">
      <path
        d="M2117 4339 c-94 -10 -308 -56 -387 -81 -564 -181 -1017 -568 -1269 -1081 -79 -162 -120 -275 -161 -451 -26 -110 -51 -288 -41 -299 4 -4 334 -6 734 -5 l726 3 -179 204 c-99 112 -180 205 -180 207 0 2 80 4 178 3 l177 0 55 -66 c30 -36 60 -71 66 -77 27 -29 184 -208 224 -256 25 -30 67 -79 94 -110 27 -30 51 -57 53 -59 1 -2 3 464 3 1037 0 828 -3 1042 -12 1041 -7 -1 -44 -5 -81 -10z"
        id="path4065"
        style="fill:#ea2222;fill-opacity:1" />
      <path
        d="M2520 3308 l1 -1043 27 31 c15 18 128 147 252 288 l224 256 174 0 173 0 -28 -34 c-15 -18 -75 -87 -133 -152 -58 -66 -127 -145 -154 -176 l-48 -58 737 0 737 0 -7 63 c-12 109 -54 305 -91 420 -238 736 -885 1292 -1654 1421 -47 8 -113 17 -147 21 l-63 7 0 -1044z"
        id="path4067" />
    </g>
    <path
      inkscape:connector-curvature="0"
      d="m 211.7,427.7 c -9.4,-1 -30.79999,-5.6 -38.7,-8.1 C 116.60001,401.5 71.300003,362.8 46.100003,311.5 c -7.9,-16.2 -12.000001,-27.5 -16.1,-45.1 -2.6,-11 -5.1,-28.8 -4.1,-29.9 0.4,-0.4 33.399999,-0.6 73.399997,-0.5 l 72.6,0.3 -17.9,20.4 c -9.9,11.2 -18,20.5 -18,20.7 0,0.2 8,0.4 17.8,0.3 h 17.7 l 5.50001,-6.6 c 3,-3.6 6,-7.1 6.6,-7.7 2.7,-2.9 18.39999,-20.8 22.39999,-25.6 2.50001,-3 6.70001,-7.9 9.40001,-11 2.7,-3 5.1,-5.7 5.29999,-5.9 0.10001,-0.2 0.3,46.4 0.3,103.7 0,82.8 -0.3,104.2 -1.2,104.1 -0.7,-0.1 -4.39999,-0.5 -8.1,-1 z"
      id="path4065-3"
      style="fill:#ea2222;fill-opacity:1;stroke-width:0.09999999;image-rendering:optimizeQuality" />
    <path
      inkscape:connector-curvature="0"
      style="stroke-width:0.09999999;image-rendering:optimizeQuality"
      d="m 252,325.8 0.1,-104.3 2.7,3.1 c 1.5,1.8 12.8,14.7 25.2,28.8 l 22.4,25.6 h 17.4 17.3 l -2.8,-3.4 c -1.5,-1.8 -7.5,-8.7 -13.3,-15.2 -5.8,-6.6 -12.7,-14.5 -15.4,-17.6 l -4.8,-5.8 h 73.7 73.7 l -0.7,6.3 c -1.2,10.9 -5.4,30.5 -9.1,42 -23.8,73.6 -88.5,129.2 -165.4,142.1 -4.7,0.8 -11.3,1.7 -14.7,2.1 l -6.3,0.7 z"
      id="path4067-6" />
  </svg>
<svg v-if="getmedian(article.media)==1"
   version="1.0"
   width="64px"
   height="32px"
   viewBox="0 0 269.000000 81.000000"
   preserveAspectRatio="none"
   sodipodi:docname="granma.svg"
   inkscape:version="0.92.4 (5da689c313, 2019-01-14)">
    <g transform="translate(0.000000,81.000000) scale(0.100000,-0.100000)"
    fill="#ea2222" stroke="none">
    <path d="M299 687 c-150 -56 -276 -236 -295 -421 l-7 -66 37 -35 c21 -19 49
    -38 63 -41 31 -8 95 21 147 67 42 36 54 34 33 -8 -8 -15 -18 -38 -21 -50 -6
    -20 -5 -21 21 -13 85 25 98 36 117 97 10 32 31 82 46 111 l28 52 -28 15 c-19
    10 -58 15 -108 15 -74 0 -81 -2 -96 -25 -9 -13 -16 -27 -16 -30 0 -3 25 -5 55
    -5 30 0 55 -4 55 -9 0 -23 -153 -141 -183 -141 -14 0 -15 74 -3 131 35 163
    155 311 239 295 18 -3 43 -13 55 -22 l23 -16 -20 -32 -20 -33 35 -16 c19 -9
    37 -17 39 -17 2 0 24 26 49 58 l44 58 -35 29 c-65 52 -187 76 -254 52z"/>
    <path d="M545 427 c-22 -39 -41 -75 -43 -79 -2 -3 7 -9 18 -13 17 -5 31 1 59
    29 34 33 71 48 71 27 0 -4 -15 -28 -34 -52 -32 -43 -90 -148 -84 -154 35 -28
    94 -65 106 -65 8 0 36 15 62 34 l47 34 44 -34 c24 -18 51 -34 60 -34 9 0 35
    14 58 30 l42 31 48 -35 48 -36 47 36 46 35 39 -30 c21 -17 42 -31 47 -31 4 0
    45 40 92 90 46 49 88 90 93 90 5 0 -4 -27 -21 -59 l-30 -60 39 -30 c21 -17 45
    -31 53 -31 8 0 34 14 56 30 23 17 45 30 49 30 5 0 26 -14 47 -30 22 -17 44
    -30 50 -30 6 0 21 15 33 33 31 45 141 152 149 144 4 -3 -8 -31 -25 -61 l-30
    -55 38 -30 c21 -17 42 -31 46 -31 4 0 46 40 92 90 47 50 89 90 94 90 5 0 -5
    -27 -22 -61 -16 -34 -29 -62 -27 -63 2 -2 19 -15 39 -29 20 -15 42 -27 49 -27
    7 0 35 16 61 35 27 19 52 35 55 35 3 0 26 -18 51 -40 l46 -40 36 22 c20 12 46
    28 57 35 19 12 25 11 50 -9 65 -52 57 -52 115 -7 93 72 130 111 118 125 -8 10
    -26 3 -80 -33 -38 -25 -71 -44 -73 -42 -3 2 25 56 60 119 l65 115 -22 17 c-23
    20 -45 23 -54 9 -3 -6 -18 -6 -38 0 -17 5 -52 9 -78 9 -56 0 -103 -36 -177
    -138 -35 -47 -68 -78 -111 -105 -33 -20 -61 -35 -61 -32 0 3 27 56 60 118 33
    63 60 118 60 124 0 6 -13 16 -30 23 -35 15 -40 12 -160 -86 -44 -35 -80 -62
    -80 -59 0 4 16 33 35 66 l34 59 -31 16 c-39 20 -50 15 -158 -75 -46 -38 -86
    -69 -87 -67 -2 2 12 27 32 57 19 29 35 59 35 65 0 11 -57 41 -64 33 -1 -2 -37
    -47 -79 -101 -56 -70 -92 -106 -136 -132 -32 -20 -61 -36 -64 -36 -3 0 23 52
    59 115 35 63 64 119 64 124 0 5 -13 14 -29 21 -37 15 -44 11 -155 -80 -47 -39
    -86 -68 -86 -66 0 3 16 31 35 63 l35 58 -23 17 c-12 10 -27 18 -33 18 -6 0
    -44 -44 -84 -97 -52 -71 -89 -109 -131 -137 -33 -21 -62 -37 -65 -34 -2 3 10
    32 29 64 19 33 48 85 66 116 l32 57 -31 16 c-23 12 -35 13 -45 5 -9 -7 -21 -7
    -39 0 -15 5 -50 10 -77 10 -47 0 -53 -3 -107 -57 -32 -32 -71 -78 -88 -103
    -28 -41 -137 -120 -149 -108 -9 8 54 123 90 165 19 23 35 43 35 46 0 3 -16 15
    -35 27 -29 18 -40 20 -72 11 -41 -12 -51 -8 -35 12 9 11 6 16 -14 25 -14 7
    -28 12 -32 12 -4 0 -25 -33 -47 -73z m500 -21 c17 -12 18 -17 7 -38 -37 -68
    -162 -181 -180 -163 -11 10 56 130 97 174 42 45 48 47 76 27z m1458 3 c12 -7
    24 -13 26 -15 5 -5 -45 -71 -88 -117 -38 -40 -99 -83 -107 -75 -8 9 28 83 72
    145 37 52 52 67 72 72 2 1 13 -4 25 -10z"/>
    </g>
  </svg>
</v-btn>
                <v-spacer></v-spacer>
                <v-btn flat @click="updateart(article)">Actualizar</v-btn>
              </v-card-actions>
            </v-layout>

            </v-container>
          </v-card>
        </v-flex>
      </v-layout>
      </v-container>
         <v-container class="text-xs-center"> <v-pagination
              v-model="page"
              :length="totalpage"
              :total-visible="7"
              color="#42b983"
              prev-icon="fas fa-caret-left"
              next-icon="fas fa-caret-right"
            ></v-pagination></v-container>
      </v-card>
    </v-slide-y-transition>
    </v-flex>
  </v-layout>
  <!-- </v-container> -->
</template>



<script>
import { eventBus, baseUrl } from "../main.js";

export default {
  name: "Home",
  data() {
    return {
      page: 1,
      totalpage: 1,
      url: "",
      waiting: false,
      articles: [],
      loading: true,
      pagefilt: ""
    };
  },
  methods: {
    gotosite(producturl){
      window.open(producturl, '_blank');
    },
    getpage: function(id) {
      this.$router.push("/articles/" + id);
    },
    gotarticle: function() {
        this.loading = false;
        this.page=1;
        fetch(baseUrl + '/article/paginate?page='+ `${this.page}` + '&filter='+ `${this.pagefilt}`).then(response => {

        if (response.status != 200) {
            // eslint-disable-next-line
            console.log("Error Do stuff here");
            // eslint-disable-next-line
            console.log(response);
        }

        return response.json().then(json => {
            this.totalpage = json.pages;
            this.articles = json.articles;
            // return json;
        });
      });
    },
    getmedia: function(med) {
      if (med == "CubaDebate") {
        return require("@/assets/cubadebate.png");
      } else if(med == "Granma"){
        return require("@/assets/granma.png");
      } else {
        return "";
      }
    },
    getmedian: function(med) {
      if (med == "CubaDebate") {
        return 0;
      } else if(med == "Granma"){
        return 1;
      } else {
        return 0;
      }
    },
    updateart: function(art) {
      eventBus.$emit("refreshdialog", art);
    }
  },
  created() {
    eventBus.$on("getpage", url => {
      this.url = url;
      this.waiting = true;
    });
    eventBus.$on("onretrive", json => {
      this.$router.replace("/articles/" + json.id);
    });
    this.urlsearch = "";
    this.gotarticle();
  },
  watch: {
        // eslint-disable-next-line
        'page': function(val, oldVal){
            fetch(baseUrl + '/article/paginate?page='+ `${this.page}` + '&filter='+ `${this.pagefilt}`).then(response => {

        if (response.status != 200) {
            // eslint-disable-next-line
            console.log("Error Do stuff here");
            // eslint-disable-next-line
            console.log(response);
        }

        return response.json().then(json => {
            // console.log(json);
            if( this.totalpage != json.pages){
            this.totalpage = json.pages;
            }
            if( this.page > this.totalpage){
              this.page=1;
            }
            this.articles = json.articles;
            // return json;
        });
    });
        }
  },
  mounted (){
    this.$router.push('/')
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
  text-decoration: none;
}

table.v-table tbody td {
  font-size: 15px;
  font-weight: 400;
}

table.v-table thead th {
  font-size: 20px;
}

.is-flex {
  display: flex;
}

.headline {
  font-size: 20px!important;
}

.centerv{
  position: relative;
  top: -25%;
}
</style>
