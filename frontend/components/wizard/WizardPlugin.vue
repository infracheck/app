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
          <v-btn
            rounded
            color="primary"
            :disabled="!Object.keys(docs).includes(selectedPlugin)"
            @click="addPlugin"
          >
            Add Plugin
          </v-btn>
          <v-chip
            v-for="plugin in data.plugins"
            :key="plugin.id"
            class="ma-2"
            color="pink"
            label
            close
            @click="showDoc = docs[plugin.id]"
            @click:close="data.plugins = data.plugins.filter(dataPlugin=> dataPlugin!== plugin)"
          >
            {{ plugin.id }}
          </v-chip>
          <div v-if="selectedPlugin" class="pa-3">
            <v-divider class="mb-2" />
            <h3>DOCUMENTATION - {{ docs[selectedPlugin].id.toUpperCase() }}</h3>
            <p v-if="docs[selectedPlugin].version">
              Version {{ docs[selectedPlugin].version }}
            </p>
            <p v-if="docs[selectedPlugin].author">
              Author {{ docs[selectedPlugin].author }}
            </p>
            <vue-simple-markdown
              class="white--text mt-0 pt-0"
              :horizontal-line="false"
              :source="docs[selectedPlugin].documentation"
            />
            <prop-table :props="docs[selectedPlugin].props" />
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
  components: { PropTable },
  props: ['data', 'docs'],
  data () {
    return {
      selectedPlugin: '',
      showDoc: null
    }
  },
  methods: {
    addPlugin () {
      this.data.plugins.push({
        id: this.selectedPlugin,
        modules: [],
        props: {}
      })
      this.selectedPlugin = ''
    }

  }
}
</script>

<style scoped>

</style>
