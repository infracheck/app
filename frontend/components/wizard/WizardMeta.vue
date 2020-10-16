<template>
  <div>
    <v-row>
      <v-col lg="6" md="12">
        <h2>
          Metadata
        </h2>
        <p>
          Define meta data to identify or categorize your test afterwards.
          Both, the name and the description have no impact on the actual test.
        </p>
      </v-col>
    </v-row>
    <v-row>
      <v-col lg="6" md="12">
        <v-text-field
          outlined
          color="accent"
          v-model="data.label"
          label="Name"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col lg="6" md="12">
        <v-textarea
          outlined
          color="accent"
          v-model="data.description"
          label="Description"
          auto-grow
          rows="3"
        />
      </v-col>
    </v-row>

  </div>
</template>

<script>
export default {
  name: 'WizardMeta',
  props: ['data']
}
</script>

<style scoped>

</style>
