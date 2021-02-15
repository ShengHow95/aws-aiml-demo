<template>
  <v-row no-gutters>
    <div class="col-sm-12 text-center mt-3">
      <div class="mx-5">
        <span class="text-h6 grey--text text--lighten-2 font-weight-bold">
          Amazon Comprehend
        </span>
        <span class="text-subtitle-1 grey--text text--lighten-1">
          allows you to discover insights and relationships in text. To know
          more, visit
        </span>
        <a
          href="https://aws.amazon.com/comprehend/"
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
    <div class="col-sm-12 px-5">
      <v-form v-model="isFormValid">
        <v-textarea
          v-model="inputText"
          counter="200"
          clearable
          filled
          auto-grow
          clear-icon="$vuetify.icons.mdiCloseCircle"
          label="Input Text"
          placeholder="Type Something Here..."
          :rules="rules"
        >
        </v-textarea>
      </v-form>
      <div>
        <v-select
          v-model="detection"
          :items="detections"
          label="Detection"
          class="ma-auto"
          @change="resultIterators = []"
        ></v-select>
      </div>
      <div class="d-flex">
        <v-select
          v-if="detection === 'Syntax Detection'"
          v-model="languageCode"
          :items="posLanguages"
          item-text="name"
          item-value="code"
          label="Language"
          class="ma-auto"
        ></v-select>
        <v-select
          v-if="detection !== 'Syntax Detection'"
          v-model="languageCode"
          :items="languages"
          item-text="name"
          item-value="code"
          label="Language"
          :disabled="detection === 'Dominant Language Detection'"
          class="ma-auto"
        ></v-select>
        <v-btn
          class="mt-2 mx-2"
          outlined
          color="warning"
          :disabled="!isFormValid"
          @click="detect"
        >
          Detect
        </v-btn>
      </div>
    </div>
    <div class="col-sm-12">
      <v-divider></v-divider>
    </div>
    <div class="col-sm-12 px-5 my-3 font-weight-medium text-h6">Results:</div>
    <div class="col-sm-12">
      <v-row>
        <v-col
          v-for="(result, i) in resultIterators"
          :key="i"
          class="d-flex justify-center"
          xs="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card elevation="5" width="250" class="ma-2">
            <v-card-title class="blue darken-4 d-flex justify-center">
              <span>
                <div>{{ result.Text }}</div>
              </span>
            </v-card-title>
            <v-card-text class="text-center mt-4">
              <span v-if="detection == 'Dominant Language Detection'">
                <div>Score: {{ (result.Score * 100).toFixed(2) }} %</div>
              </span>
              <span v-if="detection == 'Entities Detection'">
                <div>Score: {{ (result.Score * 100).toFixed(2) }} %</div>
                <div>Type: {{ result.Type }}</div>
              </span>
              <span v-if="detection == 'Key Phrases Detection'">
                <div>Score: {{ (result.Score * 100).toFixed(2) }} %</div>
              </span>
              <span v-if="detection == 'PII Entities Detection'">
                <div>Score: {{ (result.Score * 100).toFixed(2) }} %</div>
                <div>Type: {{ result.Type }}</div>
              </span>
              <span v-if="detection == 'Sentiment Detection'">
                <div>
                  Positive Score:
                  {{ (result.PositiveScore * 100).toFixed(2) }} %
                </div>
                <div>
                  Negative Score:
                  {{ (result.NegativeScore * 100).toFixed(2) }} %
                </div>
                <div>
                  Neutral Score:
                  {{ (result.NeutralScore * 100).toFixed(2) }} %
                </div>
                <div>
                  Mixed Score:
                  {{ (result.MixedScore * 100).toFixed(2) }} %
                </div>
              </span>
              <span v-if="detection == 'Syntax Detection'">
                <div>Score: {{ (result.Score * 100).toFixed(2) }} %</div>
                <div>POS: {{ result.PartOfSpeech }}</div>
              </span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
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
    detections: [
      'Dominant Language Detection',
      'Entities Detection',
      'Key Phrases Detection',
      'PII Entities Detection',
      'Sentiment Detection',
      'Syntax Detection',
    ],
    detection: 'Dominant Language Detection',
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
    posLanguages: [
      { name: 'English', code: 'en' },
      { name: 'Spanish', code: 'es' },
      { name: 'German', code: 'de' },
      { name: 'Italian', code: 'it' },
      { name: 'Portuguese', code: 'pt' },
      { name: 'French', code: 'fr' },
    ],
    languageCode: 'en',
    response: null,
    resultIterators: [],
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
    async detect() {
      if (this.userSignedIn) {
        const data = {
          text: this.inputText,
          username: this.username,
          detection: this.detection,
          languageCode: this.languageCode,
        }

        await this.$axios
          .post('/comprehend', data)
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
      } else {
        this.errorText = 'Please Sign In or Sign Up before using the services'
        this.snackbar = true
      }
    },
    resultHandler() {
      this.resultIterators = []
      if (this.detection === 'Dominant Language Detection') {
        for (let j = 0; j < this.response.Languages.length; j++) {
          const index = this.languages.findIndex(
            (x) => x.code === this.response.Languages[j].LanguageCode
          )
          this.resultIterators.push({
            Score: this.response.Languages[j].Score,
            Text: this.languages[index].name,
          })
        }
      } else if (this.detection === 'Entities Detection') {
        if (this.response.Entities.length === 0) {
          this.errorText = 'No Entity is detected'
          this.snackbar = true
        } else {
          this.resultIterators = this.response.Entities
        }
      } else if (this.detection === 'Key Phrases Detection') {
        if (this.response.KeyPhrases.length === 0) {
          this.errorText = 'No Key Phrase is detected'
          this.snackbar = true
        } else {
          this.resultIterators = this.response.KeyPhrases
        }
      } else if (this.detection === 'PII Entities Detection') {
        if (this.response.Entities.length === 0) {
          this.errorText = 'No PII Entity is detected'
          this.snackbar = true
        } else {
          for (let j = 0; j < this.response.Entities.length; j++) {
            this.response.Entities[j].Text = this.inputText.substring(
              this.response.Entities[j].BeginOffset,
              this.response.Entities[j].EndOffset
            )
          }
          this.response.Entities.Text = this.inputText.substring(
            this.response.Entities.BeginOffset,
            this.response.Entities.EndOffset
          )
          this.resultIterators = this.response.Entities
        }
      } else if (this.detection === 'Sentiment Detection') {
        this.resultIterators.push({
          Text: this.response.Sentiment,
          PositiveScore: this.response.SentimentScore.Positive,
          NegativeScore: this.response.SentimentScore.Negative,
          NeutralScore: this.response.SentimentScore.Neutral,
          MixedScore: this.response.SentimentScore.Mixed,
        })
      } else if (this.detection === 'Syntax Detection') {
        if (this.response.SyntaxTokens.length === 0) {
          this.errorText = 'No Syntax is detected'
          this.snackbar = true
        } else {
          this.response.SyntaxTokens.forEach((syntax) => {
            let tag = null
            if (syntax.PartOfSpeech.Tag === 'ADJ') {
              tag = 'Adjective'
            } else if (syntax.PartOfSpeech.Tag === 'ADP') {
              tag = 'Adposition'
            } else if (syntax.PartOfSpeech.Tag === 'ADV') {
              tag = 'Adverb'
            } else if (syntax.PartOfSpeech.Tag === 'ADP') {
              tag = 'Auxiliary'
            } else if (syntax.PartOfSpeech.Tag === 'AUX') {
              tag = 'Adposition'
            } else if (syntax.PartOfSpeech.Tag === 'CCONJ') {
              tag = 'Coordinating Conjunction'
            } else if (syntax.PartOfSpeech.Tag === 'DET') {
              tag = 'Determiner'
            } else if (syntax.PartOfSpeech.Tag === 'INTJ') {
              tag = 'Interjection'
            } else if (syntax.PartOfSpeech.Tag === 'NOUN') {
              tag = 'Noun'
            } else if (syntax.PartOfSpeech.Tag === 'NUM') {
              tag = 'Numeral'
            } else if (syntax.PartOfSpeech.Tag === 'O') {
              tag = 'Other'
            } else if (syntax.PartOfSpeech.Tag === 'PART') {
              tag = 'Particle'
            } else if (syntax.PartOfSpeech.Tag === 'PRON') {
              tag = 'Pronoun'
            } else if (syntax.PartOfSpeech.Tag === 'PROPN') {
              tag = 'Proper Noun'
            } else if (syntax.PartOfSpeech.Tag === 'PUNCT') {
              tag = 'Punctuation'
            } else if (syntax.PartOfSpeech.Tag === 'SCONJ') {
              tag = 'Subordinating Conjunction'
            } else if (syntax.PartOfSpeech.Tag === 'SYM') {
              tag = 'Symbol'
            } else if (syntax.PartOfSpeech.Tag === 'VERB') {
              tag = 'Verb'
            }
            this.resultIterators.push({
              Text: syntax.Text,
              PartOfSpeech: tag,
              Score: syntax.PartOfSpeech.Score,
            })
          })
        }
      }
    },
  },
}
</script>
