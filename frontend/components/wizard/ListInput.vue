<template>
  <div>
    <v-row no-gutters>
      <v-col cols="9">
        <v-text-field
          v-model="newItem"
          label="Add item"
          :type="number_list ? 'number': 'text'"
        />
      </v-col>
      <v-col cols="3">
        <v-btn
          color="primary"
          class="mt-3"
          fab
          small
          :disabled="newItem.length===0"
          @click="addItem"
        >
          <v-icon>mdi-plus-thick</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <label>{{ label }}: </label>
    <v-alert
      v-if="value.length === 0"
      dense
      prominent
      color="error"
    >
      List is empty ...
    </v-alert>
    <v-chip
      v-for="(item, id) in value"
      :key="id"
      class="ma-2"
      color="pink"
      label
      close
      @click:close="removeItem(id)"
    >
      {{ item }}
    </v-chip>
  </div>
</template>

<script>
export default {
  name: 'ListInput',
  props: {
    value: {},
    label: {},
    number_list: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      newItem: ''

    }
  },
  methods: {
    updateDate () {
      this.$emit('input', this.value)
    },
    removeItem (index) {
      this.value.splice(index, 1)
      this.updateDate()
    },
    addItem () {
      this.value.push(this.newItem)
      this.newItem = ''
      this.updateDate()
    }
  }
}
</script>

<style scoped>

</style>
