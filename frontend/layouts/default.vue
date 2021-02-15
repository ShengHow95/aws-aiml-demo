<template>
  <v-app dark>
    <!-- Navigation Drawer -->
    <v-navigation-drawer v-model="drawer" fixed app color="#242c3c">
      <v-list-item>
        <v-list-item-content>
          <v-img src="/aws-logo.png" alt="aws-logo"></v-img>
          <v-list-item-title class="text-h6 text-center mt-2">
            AI/ML Services in AWS
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider class="ma-2"></v-divider>

      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- App Bar -->
    <v-app-bar fixed app color="#242c3c" height="65">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title class="d-none d-sm-flex" v-text="title" />
      <v-spacer />
      <div v-if="!userSignedIn">
        <v-btn text to="/signin">Sign In</v-btn>
        <v-btn outlined to="/signup">Sign Up</v-btn>
      </div>
      <div v-else>
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <v-chip
              color="green darken-2"
              text-color="white"
              class="mx-2"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>$vuetify.icons.mdiApi</v-icon>
              <v-avatar right class="green darken-4">
                {{ $store.state.apiCount }}
              </v-avatar>
            </v-chip>
          </template>
          <span>API Calls left</span>
        </v-tooltip>
        <v-btn outlined @click="signout">Sign Out</v-btn>
      </div>
    </v-app-bar>

    <!-- Main Contain -->
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app class="d-flex justify-center" height="35">
      &copy; {{ year }} — Made with 💜 by Jeff Kong
    </v-footer>
  </v-app>
</template>

<script>
import { Auth } from '@aws-amplify/auth'

export default {
  data: () => ({
    year: new Date().getFullYear(),
    drawer: false,
    items: [
      {
        icon: '$vuetify.icons.mdiHome',
        title: 'Home',
        to: '/',
      },
      {
        icon: '$vuetify.icons.mdiAlphabeticalVariant',
        title: 'Text Analytics',
        to: '/text',
      },
      {
        icon: '$vuetify.icons.mdiImageOutline',
        title: 'Image Analytics',
        to: '/image',
      },
    ],
    title: null,
    userSignedIn: false,
    idToken: null,
    username: null,
  }),
  watch: {
    $route() {
      if (this.$route.name.startsWith('text')) {
        this.title = 'Text Analytics'
      } else if (this.$route.name.startsWith('image')) {
        this.title = 'Image Analytics'
      } else {
        this.title = 'Home'
      }
    },
  },
  async mounted() {
    if (this.$route.name.startsWith('text')) {
      this.title = 'Text Analytics'
    } else if (this.$route.name.startsWith('image')) {
      this.title = 'Image Analytics'
    } else {
      this.title = 'Home'
    }

    await Auth.currentAuthenticatedUser()
      .then((res) => {
        this.userSignedIn = true
        this.username = res.username
        this.idToken = res.signInUserSession.idToken.getJwtToken()
        this.$axios.setHeader('Authorization', this.idToken)
        this.$axios.setHeader('Content-Type', 'application/json')
      })
      .catch((err) => {
        this.errorText = err.message
      })

    if (this.userSignedIn) {
      await this.$axios
        .get('/apicount?username=' + this.username)
        .then((res) => {
          this.$store.commit('SET_apiCount', res.data.apiCount)
        })
        .catch((err) => {
          this.errorText = err.message
          this.snackbar = true
        })
    } else {
      this.$store.commit('SET_apiCount', 0)
    }
  },
  methods: {
    signout() {
      Auth.signOut()
      window.location.reload()
    },
  },
}
</script>
