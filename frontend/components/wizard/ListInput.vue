<template>
  <div>
    <v-row no-gutters>
      <v-col cols="7">
        <v-text-field
          outlined
          hide-details
          dense
          v-model="newItem"
          color="accent"
          :label="label"
          :type="number_list ? 'number': 'text'"
        />
      </v-col>
      <v-col cols="5">
        <v-btn
          block
          color="accent"
          class="py-5"
          :disabled="newItem.length===0"
          @click="addItem"
        >
          <v-icon>mdi-plus-thick</v-icon>
          Add
        </v-btn>
      </v-col>
    </v-row>
    <v-alert
      v-if="value.length === 0"
      dense
      prominent
    >
      List is empty ...
    </v-alert>
    <v-chip
      v-for="(item, id) in value"
      :key="id"
      class="ma-2"
      color="primary"
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
    input: {},
    label: {},
    number_list: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      newItem: '',
      value: this.input

    }
  },
  methods: {
    update() {
      this.$emit('input', this.value)
    },
    removeItem(index) {
      this.value.splice(index, 1)
      this.update()
    },
    addItem() {
      this.number_list ? this.value.push(Number(this.newItem)) : this.value.push(this.newItem)
      this.newItem = ''
      this.update()
    }
  }
}
</script>

<style scoped>

</style>
