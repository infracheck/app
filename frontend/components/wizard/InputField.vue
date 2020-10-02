<template>
  <div>
    <v-text-field
      v-if="field_documentation.type ==='Type.String'"
      v-model="props[field_label]"
      type="text"
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
    <v-switch
      v-else-if="field_documentation.type ==='Type.Boolean'"
      v-model="props[field_label]"
      inset
      :label="field_label"
    />
    <ListInput
      v-else-if="['Type.StringArray','Type.NumberArray' ].includes(field_documentation.type)"
      v-model="props[field_label]"
      :number_list="field_documentation.type !=='Type.StringArray'"
      :label="field_label"
    />
  </div>
</template>

<script>
import ListInput from '@/components/wizard/ListInput'

export default {
  name: 'InputField',
  components: { ListInput },
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
