<template>
  <v-app>
    <div v-if="error.statusCode === 404" class="ma-10">
      <v-row justify="center">
        <div class="text-h2 font-weight-bold pa-5">ERROR</div>
      </v-row>
      <v-row justify="center">
        <div class="text-h1 font-weight-bold px-1 pa-5">4</div>
        <div
          class="red--text text--darken-3 text-h1 font-weight-bold px-1 pa-5"
        >
          0
        </div>
        <div class="text-h1 font-weight-bold px-1 pa-5">4</div>
      </v-row>
      <v-row justify="center">
        <div class="text-h4 text-center font-weight-bold mt-2">
          Page Not Found!
        </div>
      </v-row>
      <v-row justify="center">
        <v-img
          alt="Webpage Not Found!"
          src="https://icon-library.com/images/not-found-icon/not-found-icon-24.jpg"
          max-height="200"
          max-width="200"
          class="mt-10"
        ></v-img>
      </v-row>
    </div>
    <div v-else>
      <v-row justify="center">
        <div class="text-h4 font-weight-bold">An Error Occurred!</div>
      </v-row>
    </div>
    <v-btn class="ma-10" color="error" nuxt to="/"> Home Page </v-btn>
  </v-app>
</template>

<script>
export default {
  layout: 'empty',
  props: {
    error: {
      type: Object,
      default: null,
    },
  },
  head() {
    const title =
      this.error.statusCode === 404 ? this.pageNotFound : this.otherError
    return {
      title,
    }
  },
}
</script>
