<template>
  <v-container fluid>
    <div class="my-2 text-center text-h4">AWS AI/ML Services</div>
    <v-sheet>
      <v-img src="/ai-services.png"></v-img>
    </v-sheet>
    <v-row no-gutters class="my-2 justify-space-around">
      <v-btn outlined color="warning" class="my-2" to="/text">
        Text Analytics Demo
      </v-btn>
      <v-btn outlined color="warning" class="my-2" to="/image">
        Image Analytics Demo
      </v-btn>
    </v-row>
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
  </v-container>
</template>

<script>
export default {
  components: {},
  data: () => ({
    title: 'Home',
    snackbar: false,
    timeout: 5000,
    errorText: null,
  }),
  head() {
    return {
      title: this.title,
    }
  },
  mounted() {},
}
</script>
