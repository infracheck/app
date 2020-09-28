<template>
  <v-card-text>
    <v-list
      dense
    >
      <v-list-group
        v-for="(value, key) in docs"
        :key="key"
      >
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title v-text="key" />
          </v-list-item-content>
        </template>

        <v-list-item
          class="ml-3"
          @click="$emit('active', value)"
        >
          <v-list-item-icon>
            <v-icon>mdi-toy-brick</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Description</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
          v-for="(subValue, subKey) in value.modules"
          :key="subKey"
          class="ml-3"
          @click="$emit('active', subValue)"
        >
          <v-list-item-icon>
            <v-icon>mdi-view-module-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="subKey" />
          </v-list-item-content>
        </v-list-item>
      </v-list-group>
    </v-list>
  </v-card-text>
</template>

<script>
export default {
  name: 'DocMenu',
  props: {
    docs: Object,
    activeElem: Object
  },
  data: () => ({
    active: [],
    files: {
      plugin: 'mdi-toy-brick',
      module: 'mdi-view-module-outline'
    },
    search: '',
    tree: []
  }),
  computed: {},
  methods: {}
}
</script>

<style scoped>

</style>
