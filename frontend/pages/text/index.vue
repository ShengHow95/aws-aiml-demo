<template>
  <v-container fluid>
    <v-tabs
      v-model="tab"
      centered
      center-active
      show-arrows
      color="orange lighten-1"
    >
      <v-tab href="#tab-1"> Comprehend </v-tab>
      <v-tab href="#tab-2"> Translate </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item value="tab-1" style="min-height: calc(100vh - 200px)">
        <Comprehend></Comprehend>
      </v-tab-item>
      <v-tab-item value="tab-2" style="min-height: calc(100vh - 200px)">
        <Translate></Translate>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
export default {
  components: {},
  data: () => ({
    title: 'Text Analytics',
    tab: null,
  }),
  head() {
    return {
      title: this.title,
    }
  },
}
</script>
