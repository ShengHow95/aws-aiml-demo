<template>
  <v-row no-gutters>
    <div class="col-sm-12 text-center mt-3">
      <div class="mx-5">
        <span class="text-h6 grey--text text--lighten-2 font-weight-bold">
          Amazon Translate
        </span>
        <span class="text-subtitle-1 grey--text text--lighten-1">
          provides fluent and accurate machine translation for many languages.
          To know more, visit
        </span>
        <a
          href="https://aws.amazon.com/translate/"
          target="_blank"
          rel="noreferrer"
        >
          here
        </a>
      </div>
    </div>
    <div class="col-sm-12 my-3">
      <v-divider></v-divider>
    </div>
    <div class="col-sm-6">
      <div class="d-flex mx-5">
        <span class="text-subtitle-1 my-auto">Translate From</span>
        <v-spacer></v-spacer>
        <v-select
          v-model="sourceLanguageCode"
          :items="languages"
          item-text="name"
          item-value="code"
          label="Language"
          class="mt-2"
          style="max-width: 150px"
        ></v-select>
      </div>
      <v-form v-model="isFormValid">
        <v-textarea
          v-model="inputText"
          counter="200"
          clearable
          filled
          auto-grow
          clear-icon="$vuetify.icons.mdiCloseCircle"
          label="Input Text"
          :rules="rules"
          placeholder="Type Something Here..."
          class="mx-5"
        >
        </v-textarea>
      </v-form>
    </div>
    <div class="col-sm-6">
      <div class="d-flex mx-5">
        <span class="text-subtitle-1 my-auto">Translate To</span>
        <v-spacer></v-spacer>
        <v-select
          v-model="targetLanguageCode"
          :items="languages"
          item-text="name"
          item-value="code"
          label="Language"
          class="mt-2"
          style="max-width: 150px"
        ></v-select>
      </div>
      <v-textarea
        v-model="result"
        filled
        auto-grow
        label="Result"
        readonly
        class="mx-5"
      >
      </v-textarea>
    </div>
    <div class="col-sm-12 px-5 mb-3 d-flex justify-end">
      <v-btn
        outlined
        color="warning"
        :disabled="!isFormValid"
        @click="translate"
      >
        Translate
      </v-btn>
    </div>
    <v-snackbar
      v-model="snackbar"
      :timeout="timeout"
      bottom
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
  </v-row>
</template>

<script>
import Auth from '@aws-amplify/auth'

export default {
  components: {},
  data: () => ({
    isFormValid: false,
    inputText: null,
    rules: [
      (inputText) =>
        inputText == null || inputText.length <= 200 || 'Max 200 characters',
    ],
    languages: [
      { name: 'English', code: 'en' },
      { name: 'Spanish', code: 'es' },
      { name: 'German', code: 'de' },
      { name: 'Italian', code: 'it' },
      { name: 'Portuguese', code: 'pt' },
      { name: 'French', code: 'fr' },
      { name: 'Japanese', code: 'ja' },
      { name: 'Korean', code: 'ko' },
      { name: 'Hindi', code: 'hi' },
      { name: 'Arabic', code: 'ar' },
      { name: 'Chinese (Simplified)', code: 'zh' },
      { name: 'Chinese (Traditional)', code: 'zh-TW' },
    ],
    sourceLanguageCode: 'en',
    targetLanguageCode: 'es',
    result: '',
    userSignedIn: false,
    username: null,
    idToken: null,
    timeout: 5000,
    snackbar: false,
    errorText: null,
  }),
  async mounted() {
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
  },
  methods: {
    async translate() {
      if (this.userSignedIn) {
        const data = {
          text: this.inputText,
          username: this.username,
          sourceLanguageCode: this.sourceLanguageCode,
          targetLanguageCode: this.targetLanguageCode,
        }

        await this.$axios
          .post('/translate', data)
          .then((res) => {
            if (!res.data.errorMessage) {
              this.result = res.data.TranslatedText
              this.$store.commit('SET_apiCount', res.data.apiCount)
            } else {
              this.result = null
              this.errorText = res.data.errorMessage
              this.snackbar = true
            }
          })
          .catch((err) => {
            this.errorText = err.message
            this.snackbar = true
          })
      } else {
        this.errorText = 'Please Sign In or Sign Up before using the services'
        this.snackbar = true
      }
    },
  },
}
</script>
