<template>
  <v-row no-gutters>
    <div class="col-sm-12 text-center mt-3">
      <div class="mx-5">
        <span class="text-h6 grey--text text--lighten-2 font-weight-bold">
          Amazon Rekognition
        </span>
        <span class="text-subtitle-1 grey--text text--lighten-1">
          allows you to easily detect and identify objects or scenes from images
          or videos. To know more, visit
        </span>
        <a
          href="https://aws.amazon.com/rekognition/"
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
      <div class="mx-5 d-flex justify-space-between">
        <v-file-input
          :rules="rules"
          show-size
          label="Image"
          accept="image/*"
          @change="onImageSelect"
        ></v-file-input>
        <div class="mx-2 my-auto">
          <v-btn outlined color="warning" :disabled="!url" @click="analyse">
            Analyze
          </v-btn>
        </div>
      </div>
      <div v-if="url" class="col-sm-12 my-2">
        <v-img :src="url" alt="Preview Image" />
      </div>
    </div>
    <div class="d-sm-none col-sm-12 my-3">
      <v-divider></v-divider>
    </div>
    <div class="col-sm-6">
      <div class="text-h6 mx-5">Results:</div>
      <div class="mx-5">
        <v-row no-gutters>
          <v-col
            v-for="(result, i) in results"
            :key="i"
            class="d-flex justify-center"
            xs="6"
          >
            <v-card elevation="5" width="125" class="ma-2">
              <v-card-title
                class="blue darken-4 d-flex justify-center text-subtitle-2"
              >
                <span>{{ result.Name }}</span>
              </v-card-title>
              <v-card-text class="text-center mt-4">
                <span>{{ result.Score.toFixed(2) }} %</span>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>
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
    imageFile: null,
    imageFilename: null,
    rules: [
      (imageFile) =>
        !imageFile ||
        imageFile.size < 10e6 ||
        'Image size should be less than 10 MB!',
    ],
    url: null,
    results: [],
    response: null,
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
      })
      .catch((err) => {
        this.errorText = err.message
      })
  },
  methods: {
    onImageSelect(e) {
      if (e !== null && e !== undefined && e.size < 10e6) {
        this.imageFile = e
        this.imageFilename = e.name
        this.url = URL.createObjectURL(this.imageFile)
      } else {
        this.url = null
      }
      this.results = []
    },
    async upload() {
      await this.$axios.setHeader('Authorization', '')
      await this.$axios.setHeader('Content-Type', 'image/*')
      await this.$axios
        .put(`/uploadImage/${this.imageFilename}`, this.imageFile)
        .then((res) => {
          this.errorText = null
        })
        .catch((err) => {
          this.errorText = err.message
          this.snackbar = true
        })
    },
    async analyse() {
      await this.upload()

      const data = {
        username: this.username,
        image: this.imageFilename,
        detection: 'Object Detection',
      }

      await this.$axios.setHeader('Authorization', this.idToken)
      await this.$axios.setHeader('Content-Type', 'application/json')
      await this.$axios
        .post('/rekognition', data)
        .then((res) => {
          if (!res.data.errorMessage) {
            this.response = res.data
            this.$store.commit('SET_apiCount', res.data.apiCount)
          } else {
            this.response = null
            this.errorText = res.data.errorMessage
            this.snackbar = true
          }
        })
        .catch((err) => {
          this.response = null
          this.errorText = err.message
          this.snackbar = true
        })

      if (this.response) {
        await this.resultHandler()
      }
    },
    resultHandler() {
      this.results = []
      if (this.response.Labels.length === 0) {
        this.errorText = 'No Object is detected'
        this.snackbar = true
      } else {
        for (let j = 0; j < this.response.Labels.length; j++) {
          this.results.push({
            Score: this.response.Labels[j].Confidence,
            Name: this.response.Labels[j].Name,
          })
        }
      }
    },
  },
}
</script>
