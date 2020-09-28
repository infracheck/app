<template>
  <v-card outlined>
    <v-card-title>
      Meta data
    </v-card-title>
    <v-card-text>
      <v-text-field
        v-model="data.name"
        :rules="[() => !!data.name || 'This field is required']"
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
