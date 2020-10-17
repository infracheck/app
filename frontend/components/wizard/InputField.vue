<template>
  <div>
    <v-text-field
      outlined
      hide-details
      color="accent"
      v-if="field_documentation.type ==='Type.String'"
      v-model="value"
      @input="update"
      type="text"
      :label="field_label"
    />
    <v-text-field
      outlined
      hide-details
      color="accent"
      v-else-if="field_documentation.type ==='Type.Password'"
      v-model="value"
      @input="update"
      type="password"
      :label="field_label"
    />
    <v-text-field
      outlined
      hide-details
      color="accent"
      v-else-if="field_documentation.type ==='Type.Number'"
      v-model="value"
      @input="update"
      type="number"
      :label="field_label"
    />
    <v-switch
      color="accent"
      v-else-if="field_documentation.type ==='Type.Boolean'"
      v-model="value"
      @change="update"
      :label="field_label"
    />
    <ListInput
      v-else-if="['Type.StringArray','Type.NumberArray'].includes(field_documentation.type)"
      :input.sync="value"
      :number_list="field_documentation.type !=='Type.StringArray'"
      :label="field_label"
    />
    <!--DEBUG ONLY <pre>CHILD: {{ value }}</pre>-->
  </div>
</template>

<script>
import ListInput from '@/components/wizard/ListInput'

export default {
  name: 'InputField',
  components: {ListInput},
  props: ['field_label', 'input', 'field_documentation'],
  data() {
    return {
      value: this.input
    }
  },
  methods: {
    update() {
      this.$emit('update:input', this.value);
    }
  },
  beforeMount() {
    if (!this.value || this.value === '') {
      // Set default value
      this.value = this.field_documentation.default
      if (this.field_documentation.type === 'Type.Boolean') {
        this.value = false
      }
      this.update()
    }
  },
  beforeUpdate() {
    // Set default value
    if (!this.value || this.value === '') {
      this.value = this.field_documentation.default
      if (this.field_documentation.type === 'Type.Boolean') {
        this.value = Boolean(this.field_documentation.default)
      }
      this.update()
    }
  }
}
</script>
<style scoped>

</style>
