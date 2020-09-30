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
      <v-breadcrumbs :items="breads">
        <template v-slot:item="{ item }">
          <v-breadcrumbs-item
            nuxt
            :to="item.href"
            exact
          >
            {{ item.text }}
          </v-breadcrumbs-item>
        </template>
      </v-breadcrumbs>
      <PluginCards v-if="!activeDoc" :plugins="plugins"></PluginCards>
      <DocContent v-else :documentation="activeDoc"/>
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
        <DocMenu :docs="plugins" @active="onChildClick"/>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>

import DocMenu from '@/components/documentation/Menu'
import DocContent from '@/components/documentation/Content'
import PluginCards from '@/components/documentation/PluginCards'

export default {
  components: {
    PluginCards,
    DocContent,
    DocMenu
  },
  async asyncData ({ $axios, params }) {
    const plugins = await $axios.$get('/plugins/flat')
    const pluginId = params.pluginId
    const moduleId = params.moduleId
    let activeDoc = null
    if (pluginId && moduleId) {
      activeDoc = await $axios.$get(`/plugins/${pluginId}/${moduleId}`)
    } else if (pluginId) {
      activeDoc = await $axios.$get(`/plugins/${pluginId}`)
    }

    return {
      plugins,
      activeDoc
    }
  },
  data () {
    return {
      activeDoc: null
    }
  },
  computed: {
    breads () {
      const res = [
        {
          text: 'Documentation',
          href: '/documentation'
        }
      ]
      const pluginId = this.$route.params.pluginId
      const moduleId = this.$route.params.moduleId
      if (pluginId) {
        res.push({
          text: pluginId,
          href: `/documentation/${pluginId}`
        })
      }
      if (moduleId) {
        res.push({
          text: moduleId,
          href: `/documentation/${pluginId}/${moduleId}`
        })
      }
      return res
    }
  },
  methods: {
    onChildClick (value) {
      this.activeMenu = value
    }
  }
}
</script>
