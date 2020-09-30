<template>
  <v-container fluid>
    <v-row dense>
      <v-col
        v-for="(pluginData,pluginId) in plugins"
        :key="pluginId"
      >
        <v-card hover outlined nuxt :to="`/documentation/${pluginId}`" color="accent">
          <v-card-title v-text="pluginId"></v-card-title>
          <v-card-text>
            <v-row>
              <v-col>{{ pluginData.modules.length > 1 ? 'Modules' : 'Module' }}</v-col>
              <v-col>{{ pluginData.modules.length }}</v-col>
            </v-row>
            <v-row>
              <v-col>Author</v-col>
              <v-col>{{ pluginData.author }}</v-col>
            </v-row>
            <v-row>
              <v-col>Version</v-col>
              <v-col>{{ pluginData.version }}</v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'PluginCards',
  props: ['plugins']
}
</script>

<style scoped>

</style>
