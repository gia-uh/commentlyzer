<template>
  <v-container fluid>
    <v-slide-y-transition mode="out-in">
      <v-layout column align-center centered>


    <v-progress-circular
      :size="70"
      :width="7"
      color="purple"
      indeterminate
    ></v-progress-circular>
    <br>
    <h4>
      El artículo está siendo actualizado
      por favor espere, puede demorar unos minutos
      </h4>

      </v-layout>
    </v-slide-y-transition>
  </v-container>
</template>

<script>
import { eventBus, baseUrl } from "../main.js";

export default {
  name: "Wait",
  data() {
    return {
      url: "",
      id: '',
      waiting: false
    };
  },
  methods: {
    gotomain: function() {
      this.$router.replace("/articles/79");
    },
    getData: function() {
      console.log('checking status')
      fetch(baseUrl + "/status/" + this.id).then(response => {

        console.log(response)
        if (response.status === 202) {
          setTimeout(this.getData(), 5000);
          return;
        }

        if (response.status === 200) {
            response.json().then(json => {
            this.$router.replace("/articles/" + json.id)

        });
          return;
        }
        if (response.status === 502) {
            response.json().then(json => {
            eventBus.$emit("errordialog", json);

        });
          return;
        }
        console.log('ERROR ERROR')

      });
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
  },
  beforeMount() {
    console.log('ID');
    console.log(this.$route.params.id);
    this.id=this.$route.params.id;
    this.getData();
  },
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
}

.loader,
.loader:before,
.loader:after {
  border-radius: 50%;
}
.loader {
  color: #fc0808;
  font-size: 11px;
  text-indent: -99999em;
  margin: 55px auto;
  position: relative;
  width: 10em;
  height: 10em;
  box-shadow: inset 0 0 0 1em;
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
}
.loader:before,
.loader:after {
  position: absolute;
  content: "";
}
.loader:before {
  width: 5.2em;
  height: 10.2em;
  background: #100dc5;
  border-radius: 10.2em 0 0 10.2em;
  top: -0.1em;
  left: -0.1em;
  -webkit-transform-origin: 5.2em 5.1em;
  transform-origin: 5.2em 5.1em;
  -webkit-animation: load2 2s infinite ease 1.5s;
  animation: load2 2s infinite ease 1.5s;
}
.loader:after {
  width: 5.2em;
  height: 10.2em;
  background: #616361;
  border-radius: 0 10.2em 10.2em 0;
  top: -0.1em;
  left: 5.1em;
  -webkit-transform-origin: 0px 5.1em;
  transform-origin: 0px 5.1em;
  -webkit-animation: load2 2s infinite ease;
  animation: load2 2s infinite ease;
}
@-webkit-keyframes load2 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@keyframes load2 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
</style>
