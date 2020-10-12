<template>
  <v-row>
    <v-col cols="12">
      <v-card outlined>
        <v-card-text>
          <p>
            Choose plugins from the list. Click on them to show their documentation.
            Then, click 'Add plugin' to add it to your testset.
          </p>
          <v-select
            v-model="selectedPlugin"
            :items="Object.keys(docs)"
            label="Standard"
          />
          <v-text-field
            v-if="selectedPlugin"
            v-model="label"
            hint="Use the label to tag your plugin sets. Use it as a short description of what you test with this Plugin."
            label="Label"
          />
          <v-btn
            rounded
            color="primary"
            :disabled="!Object.keys(docs).includes(selectedPlugin)"
            @click="addPlugin"
          >
            Add Plugin
          </v-btn>
          <v-chip
            v-for="(plugin, i) in data.plugins"
            :key="i"
            class="ma-2"
            color="pink"
            label
            close
            @click="showDoc = docs[plugin.id]"
            @click:close="data.plugins = data.plugins.filter(dataPlugin => dataPlugin!== plugin)"
          >
            {{ plugin.id }}
          </v-chip>
          <div v-if="selectedPlugin" class="pa-3">
            <v-divider class="mb-2"/>
            <h3>DOCUMENTATION - {{ docs[selectedPlugin].id.toUpperCase() }}</h3>
            <p v-if="docs[selectedPlugin].version">
              Version {{ docs[selectedPlugin].version }}
            </p>
            <p v-if="docs[selectedPlugin].author">
              Author {{ docs[selectedPlugin].author }}
            </p>
            <a class="title" target="_blank" :href="`/documentation/${selectedPlugin}`">
              Show documentation
            </a>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import PropTable from '@/components/documentation/PropTable'

export default {
  name: 'WizardPlugin',
  components: {PropTable},
  props: ['data', 'docs'],
  data() {
    return {
      selectedPlugin: '',
      showDoc: null,
      label: '',
    }
  },
  methods: {
    addPlugin() {
      this.data.plugins.push({
        id: this.selectedPlugin,
        label: this.label,
        modules: [],
        props: {}
      })
      this.selectedPlugin = ''
      this.label = ''
    }

  }
}
</script>

<style scoped>

</style>
