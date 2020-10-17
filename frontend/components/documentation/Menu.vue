<template>
  <v-card-text>
    <v-list
      dense
    >
      <v-list-group
        :value="search !== ''"
        v-for="(pluginData, plugin_id) in docs"
        :key="plugin_id"
      >
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title v-text="plugin_id"/>
          </v-list-item-content>
        </template>

        <v-list-item
          class="ml-3"
          exact
          :to="`/documentation/${plugin_id}/`"
          nuxt
        >
          <v-list-item-icon>
            <v-icon>mdi-toy-brick</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Description</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
          exact
          v-for="module_id in pluginData.modules"
          :key="module_id"
          class="ml-3"
          :to="`/documentation/${plugin_id}/${module_id}`"
          nuxt
        >
          <v-list-item-icon>
            <v-icon>mdi-view-module-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="module_id"/>
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
  computed: {
    documentationArray() {
      let res = Object.keys(this.docs).map(plugin => {
        return {
          label: plugin,
          url: `/documentation/${plugin}`
        }
      })
      // res = res.map(plugin => {
      //   return this.docs[plugin].modules.map(module => {
      //     return {
      //       label: module,
      //       url: `/documentation/${plugin}/${module}`
      //     }
      //   })
      // })
      return res
    }
  },
  methods: {}
}
</script>

<style scoped>

</style>
