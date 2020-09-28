<template>
  <div>
    <v-text-field
      v-if="field_documentation.type ==='Type.String'"
      v-model="props[field_label]"
      :label="field_label"
    />
    <v-text-field
      v-else-if="field_documentation.type ==='Type.Password'"
      v-model="props[field_label]"
      type="password"
      :label="field_label"
    />
    <v-text-field
      v-else-if="field_documentation.type ==='Type.Number'"
      v-model="props[field_label]"
      type="number"
      :label="field_label"
    />
  </div>
</template>

<script>
export default {
  name: 'InputField',
  props: ['field_label', 'props', 'field_documentation'],
  beforeMount () {
    if (!this.props[this.field_label]) {
      // Set default value
      this.props[this.field_label] = this.field_documentation.default
    }
  },
  beforeUpdate () {
    if (!this.props[this.field_label]) {
      // Set default value
      this.props[this.field_label] = this.field_documentation.default
    }
  }
}
</script>
<style scoped>

</style>
