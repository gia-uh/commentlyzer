<template>
  <v-app>
    <v-toolbar
      app
      :clipped-left="clipped"
      class="hidden-sm-and-down white--text"
      color="rgba(66, 185, 131,1)"
    >
      <v-layout row class="text-xs-center" justify-center align-center>
        <v-toolbar-title style="cursor: pointer;" @click.stop="$router.replace('/')" v-text="title"></v-toolbar-title>

        <v-spacer></v-spacer>
        <v-text-field
          class="custom-placeholer-color"
          light
          placeholder="Coloca la Url aqui"
          v-model="urlsearch"
          align-end
        ></v-text-field>
        <v-btn icon @click.stop="getpage">
          <v-icon color="white">fas fa-paper-plane</v-icon>
        </v-btn>
      </v-layout>
    </v-toolbar>
    <v-card elevation-24 class="hidden-md-and-up white--text" color="rgba(66, 185, 131,1)">
      <v-layout column class="text-xs-center" align-center>
        <v-toolbar-title style="cursor: pointer;" @click.stop="$router.replace('/')" v-text="title"></v-toolbar-title>
        <v-layout row>
          <v-text-field
            light
            placeholder="Coloca la Url aqui"
            class="custom-placeholer-color"
            v-model="urlsearch"
            align-end
          ></v-text-field>
          <v-btn icon @click.stop="getpage">
            <v-icon color="white">fas fa-paper-plane</v-icon>
          </v-btn>
        </v-layout>
      </v-layout>
    </v-card>
    <v-content class="hidden-sm-and-down">
      <router-view />
    </v-content>
    <v-content class="hidden-md-and-up pt-0">
      <router-view />
    </v-content>
    <!-- <v-footer :fixed="fixed" app >
      <span >&copy; {{year}}

      <v-btn  flat color="#42b983" small >Acerca de nosotros</v-btn>
      </span>
    </v-footer>-->

    <v-footer dark height="auto" fixed>
      <v-card class="flex" flat tile>
        <v-card-actions class="grey darken-3 justify-end">&copy;{{year}}</v-card-actions>
      </v-card>
    </v-footer>

    <v-btn
      color="#42b983"
      dark
      small
      left
      bottom
      fab
      ripple
      fixed
      @click.stop="aboutUs.activate=true"
    >
      <v-icon small centered align-content-center>fa fa-users</v-icon>
    </v-btn>

    <v-dialog v-model="aboutUs.activate" width="500">
      <v-card>
        <v-card-title class="grey darken-3 justify-center" style="color:white">Nosotros</v-card-title>
        <v-card-text>{{aboutUs.text}}</v-card-text>
        <v-card-actions></v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialog" width="800px">
      <v-card>
        <v-card-title
          class="grey lighten-4 py-4 title"
        >Desea Actualizar el contenido de esta noticia</v-card-title>
        <v-container grid-list-sm class="pa-4">
          <v-layout row wrap>
            <v-flex xs12 align-center justify-space-between>
              <v-layout align-center>
                El artículo "{{article.title}}" fue actualizado por
                última vez el {{article.last_update | moment('from', 'now')}}. Desea
                actualizar la información sobre la noticia
              </v-layout>
            </v-flex>
          </v-layout>
        </v-container>
        <v-card-actions>
          <v-btn flat color="red" @click="updatePage(); dialog=false;">Actualizar Contenido</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            flat
            color="primary"
            @click.stop="$router.replace('/articles/' + article.id); dialog=false; urlsearch=''; "
          >Continuar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="dialoge" width="800px">
      <v-card>
        <v-card-title class="grey lighten-4 py-4 title">Error</v-card-title>
        <v-container grid-list-sm class="pa-4">
          <v-layout row wrap>
            <v-flex lg12 md12 sm12 xs12 align-center justify-space-between>
              <v-layout align-center>{{ errormsg }}</v-layout>
            </v-flex>
          </v-layout>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            flat
            color="primary"
            @click.stop="$router.replace('/');dialoge=false; urlsearch=''; "
          >Continuar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<style >
.custom-placeholer-color input::placeholder {
  color: white !important;
  opacity: 1;
}
</style>
<script>
import { eventBus, baseUrl, data } from "./main.js";

export default {
  name: "App",
  data() {
    return {
      aboutUs: {
        activate: false,
        text:
          "Commentlyzer está desarrollado por el Grupo de Inteligencia Artificial de la Universidad de la Habana (GIA) . El grupo está dirigido por el Doctor en Ciencias Yudivián Almeida. \n",
        links: [
          // {
          //   icon:"fab fa-github",
          //   name:"Github"
          // },
          // {
          //   icon:"fab fa-linkedin",
          //   name:"Linkedin"
          // }
        ]
      },
      year: 1995,
      article: {
        title: "SI ESTAS LEYENDO ESTO ES QUE ALGO SALIÓ MAL",
        last_update: "5-5-2014",
        id: "1",
        media: "esa talla toca",
        comments: 12345
      },
      windowHeight: "",
      dialog: false,
      dialoge: false,
      clipped: false,
      drawer: false,
      fixed: false,
      urlsearch: "",
      errormsg: "",
      items: [
        {
          icon: "fas fa-shapes",
          title: "Inspire"
        }
      ],
      miniVariant: false,
      right: false,
      title: "Comment Analyzer"
    };
  },
  methods: {
    getpage() {
      data.url = this.urlsearch;
      // eslint-disable-next-line
      console.log(this.urlsearch);
      fetch(baseUrl + "/getpage", {
        method: "post",
        body: JSON.stringify({ url: this.urlsearch }),
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json"
        }
      }).then(response => this.process_response(response));
    },

    updatePage() {
      // eslint-disable-next-line
      console.log("Updating site");
      fetch(baseUrl + "/article/update/" + this.article.id, {
        method: "get",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json"
        }
      }).then(response => this.process_response(response));
    },

    process_response(response) {
      // if (response.status < 200 || response.status >= 300) {
      //   this.$router.replace("/error/" + response.status);
      //   return;
      // }
      // eslint-disable-next-line
      console.log(response);
      // eslint-disable-next-line
      console.log(response.status === 202);

      if (response.status === 202) {
        response.json().then(json => {
          // console.log('La tiza');
          // eslint-disable-next-line
          console.log(json.id);
          // console.log('La tiza');
          this.$router.push("/wait/" + json.id);
          return;
          // this.article = json;
          // this.dialog = true;
          // this.$router.replace("/articles/" + json.id)
        });
        return;
      } else if (response.status === 200) {
        response.json().then(json => {
          if (json.location) {
            this.$router.push("/wait/" + json.id);
            return;
          }
          this.article = json;
          this.dialog = true;
          // this.$router.replace("/articles/" + json.id)
        });
        return;
      }

      return response.json().then(json => {
        this.$router.push("/wait/" + json.id);
      });
    }
  },

  beforeMount() {
    if (data.url !== "") {
      this.urlsearch = data.url;
    }
  },
  mounted() {
    this.year = new Date().getFullYear();
    this.windowHeight = window.innerHeight;
  },
  created() {
    if (data.url !== "") {
      this.urlsearch = data.url;
    }
    eventBus.$on("urlchange", url => {
      if (url !== undefined) {
        this.urlsearch = url;
      }
    });
    eventBus.$on("refreshdialog", article => {
      if (article !== undefined) {
        this.article = article;
        this.dialog = true;
      }
    });
    eventBus.$on("errordialog", respond => {
      this.errormsg = respond.message;
      this.dialoge = true;
    });
  }
};
</script>
