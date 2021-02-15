<template>
  <v-app style="background: #242c3c">
    <v-card width="350" class="ma-auto blue darken-4">
      <v-card-title class="text-h4 justify-center my-5"> Sign Up </v-card-title>
      <v-card-text class="grey darken-4">
        <div class="text-center pt-3">
          Please sign up before trying out demo services
        </div>
        <v-form v-model="validForm" class="pt-3">
          <v-text-field
            v-model="username"
            :rules="[rules.required]"
            label="Username"
            outlined
            rounded
          ></v-text-field>
          <v-text-field
            v-model="email"
            :rules="[rules.required, rules.validEmail]"
            label="Email"
            outlined
            rounded
          ></v-text-field>
          <v-text-field
            v-model="password"
            :append-icon="
              showPassword1
                ? '$vuetify.icons.mdiEye'
                : '$vuetify.icons.mdiEyeOff'
            "
            :rules="[rules.required, rules.validPassword]"
            :type="showPassword1 ? 'text' : 'password'"
            label="Password"
            hint="Min 8 characters"
            outlined
            rounded
            @click:append="showPassword1 = !showPassword1"
          ></v-text-field>
          <v-text-field
            v-model="confirmPassword"
            :append-icon="
              showPassword2
                ? '$vuetify.icons.mdiEye'
                : '$vuetify.icons.mdiEyeOff'
            "
            :rules="[rules.required, rules.validPassword, passwordMatch]"
            :type="showPassword2 ? 'text' : 'password'"
            label="Confirm Password"
            hint="Min 8 characters"
            outlined
            rounded
            @click:append="showPassword2 = !showPassword2"
          ></v-text-field>
        </v-form>
        <v-btn
          block
          color="primary"
          :disabled="!validForm"
          class="mb-3"
          @click="signup"
        >
          Sign Up
        </v-btn>
        <div class="d-flex justify-end mb-1">
          Already have an account? &nbsp;
          <a href="/signin" rel="noreferrer"> Sign In here! </a>
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
    title: 'Sign Up',
    validForm: false,
    username: null,
    password: null,
    email: null,
    confirmPassword: null,
    showPassword1: false,
    showPassword2: false,
    rules: {
      required: (v) => !!v || 'Required',
      validPassword: (v) => !v || v.length >= 8 || 'Min 8 characters',
      validEmail: (v) =>
        /.+@.+\..+/.test(v) || 'Email must be valid (e.g. example@domain.com)',
    },
    timeout: 5000,
    snackbar: false,
    errorText: null,
  }),
  head() {
    return {
      title: this.title,
    }
  },
  computed: {
    passwordMatch() {
      return () =>
        this.password === this.confirmPassword ||
        'Password entered does not match'
    },
  },
  methods: {
    async signup() {
      const user = {
        username: this.username,
        password: this.password,
        attributes: {
          email: this.email,
        },
      }
      await Auth.signUp(user)
        .then((res) => {
          this.$router.push('/confirmsignup')
        })
        .catch((err) => {
          if (err.message === 'User already exists') {
            this.errorText = 'Username is already taken.'
            this.snackbar = true
          } else {
            this.errorText = err.message
            this.snackbar = true
          }
        })
    },
  },
}
</script>
