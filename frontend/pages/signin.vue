<template>
  <v-app style="background: #242c3c">
    <v-card width="350" class="ma-auto blue darken-4">
      <v-card-title class="text-h4 justify-center my-5"> Sign In </v-card-title>
      <v-card-text class="grey darken-4">
        <div class="text-center pt-3">
          Please sign in before trying out the demo services
        </div>
        <v-form v-model="validForm" class="pt-3">
          <v-text-field
            v-model="username"
            label="Username"
            outlined
            rounded
          ></v-text-field>
          <v-text-field
            v-model="password"
            :append-icon="
              showPassword
                ? '$vuetify.icons.mdiEye'
                : '$vuetify.icons.mdiEyeOff'
            "
            :rules="[rules.validPassword]"
            :type="showPassword ? 'text' : 'password'"
            label="Password"
            hint="Min 8 characters"
            outlined
            rounded
            @click:append="showPassword = !showPassword"
          ></v-text-field>
        </v-form>
        <v-btn
          block
          color="primary"
          :disabled="!validForm"
          class="mb-3"
          @click="signIn"
        >
          Sign In
        </v-btn>
        <div class="d-flex justify-end mb-1">
          Don't have an account? &nbsp;
          <a href="/signup" rel="noreferrer"> Sign Up here! </a>
        </div>
      </v-card-text>
    </v-card>
    <v-snackbar
      v-model="snackbar"
      :timeout="timeout"
      top
      centered
      rounded
      color="red"
    >
      <span class="text-subtitle-1">{{ errorText }}</span>
      <template #action="{ attrs }">
        <v-btn color="black" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import { Auth } from '@aws-amplify/auth'

export default {
  layout: 'empty',
  data: () => ({
    title: 'Sign In',
    validForm: false,
    username: null,
    email: null,
    password: null,
    showPassword: false,
    rules: {
      required: (v) => !!v || 'Required',
      validPassword: (v) => !v || v.length >= 8 || 'Min 8 characters',
      validEmail: (v) =>
        /.+@.+\..+/.test(v) || 'Email must be valid (e.g. example@domain.com)',
    },
    snackbar: false,
    errorText: null,
    timeout: 5000,
  }),
  head() {
    return {
      title: this.title,
    }
  },
  methods: {
    async signIn() {
      await Auth.signIn(this.username, this.password)
        .then((data) => {
          this.$router.push({ path: '/' })
        })
        .catch((err) => {
          this.errorText = err.message
          this.snackbar = true
        })
    },
  },
}
</script>
