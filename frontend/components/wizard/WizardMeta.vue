<template>
  <v-card outlined>
    <v-card-title>
      Meta data
    </v-card-title>
    <v-card-text>
      <p>
        Define meta data to identify or categorize your test afterwards.
        Both, the name and the description have no impact on the actual test.
      </p>
      <v-text-field
        v-model="data.label"
        :rules="[() => !!data.label || 'This field is required']"
        label="Name"
      />
      <v-textarea
        v-model="data.description"
        :rules="[() => !!data.description || 'This field is required']"
        label="Description"
        auto-grow
        rows="3"
      />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'WizardMeta',
  props: ['data']
}
</script>

<style scoped>

</style>
