<template>
  <v-app style="background: #242c3c">
    <v-card width="350" class="ma-auto blue darken-4">
      <v-card-title class="text-h4 justify-center my-5">
        {{ title }}
      </v-card-title>
      <v-card-text class="grey darken-4">
        <div class="text-center pt-3">
          {{ text }}
        </div>
        <v-btn block color="primary" class="mt-3" to="/signin"> Sign In </v-btn>
      </v-card-text>
    </v-card>
  </v-app>
</template>

<script>
export default {
  layout: 'empty',
  data: () => ({
    title: 'Account Created',
    text:
      'Your account has been created. Please proceed to sign in and try out the demo services.',
  }),
  head() {
    return {
      title: this.title,
    }
  },
}
</script>
