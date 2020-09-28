<template>

  <v-row
    no-gutters
    class="fill-height"
  >
    <v-col
      cols="12"
      md="9"
      sm="7"
    >
      <DocContent :documentation="getDocItem"/>
    </v-col>
    <v-col
      cols="12"
      md="3"
      sm="5"
    >
      <v-card
        class="pa-2 fill-height"
        outlined
        tile
      >
        <v-card-title>Browse Plugins</v-card-title>
        <DocMenu :docs="pluginDocs" @active="onChildClick"/>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>

import DocContent from '@/components/documentation/Content'
import DocMenu from '@/components/documentation/Menu'

export default {
  components: {
    DocContent,
    DocMenu
  },
  async asyncData ({ $axios }) {
    const pluginDocs = await $axios.$get('/api/plugins')
    return { pluginDocs }
  },
  data () {
    return {
      activeMenu: null
    }
  },
  computed: {
    getDocItem () {
      return this.activeMenu ? this.activeMenu : this.pluginDocs[Object.keys(this.pluginDocs)[0]]
    }
  },
  methods: {
    onChildClick (value) {
      this.activeMenu = value
    }
  }
}
</script>
