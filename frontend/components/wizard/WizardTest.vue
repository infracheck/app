<template>
  <div>
    <v-row no-gutters>
      <v-col md="3" sm="12">
        <v-subheader>
          MODULES
        </v-subheader>
        <v-row no-gutters class="px-2">
          <v-col lg="7">
            <v-select
              dense
              outlined
              hide-details
              v-model="newPlugin"
              :items="Object.keys(docs)"
              label="Add Plugins ..."
              color="accent"
            />
          </v-col>
          <v-col lg="5">
            <v-btn
              block
              color="accent"
              class="py-5"
              :disabled="!Object.keys(docs).includes(newPlugin)"
              @click="addPlugin"
            >
              <v-icon>mdi-plus-thick</v-icon>
              Add
            </v-btn>
          </v-col>
        </v-row>
        <v-list shaped flat>
          <v-list-item-group
          >
            <v-list-item
              color="red"
              class="secondary darken-2 mb-1"
              v-for="(item, key) in data.plugins"
              :key="key"
              @click="selectedPlugin=data.plugins.find(x => x === item)"
            >
              <v-list-item-content>
                <v-list-item-title>
                  {{ item.id }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ item.label }}
                </v-list-item-subtitle>

              </v-list-item-content>
              <v-list-item-action>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      icon
                      x-small
                      v-bind="attrs"
                      v-on="on"
                      :href="`/documentation/${item.id}`" target="_blank" tag="dasda">
                      <v-icon>mdi-share-all-outline</v-icon>
                    </v-btn>
                  </template>
                  <span>Plugin documentation</span>
                </v-tooltip>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      icon
                      x-small
                      v-bind="attrs"
                      v-on="on"
                      @click="data.plugins = data.plugins.filter(plugin => plugin !== item); selectedPlugin===item ? selectedPlugin = '':undefined"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                  <span>Remove plugin</span>
                </v-tooltip>

              </v-list-item-action>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-col>

      <v-col class="grey darken-4" md="9" sm="12">
        <v-alert class="mt-5 ml-3" width="300" outlined color="accent" v-if="!selectedPlugin">
          Please add and select a plugin on the left side.
        </v-alert>
        <TestEditor
          v-if="plugin === selectedPlugin"
          v-for="(plugin, id) in data.plugins"
          :key="id"
          :pluginInput.sync="plugin"
          :docs="docs"></TestEditor>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import InputField from '@/components/wizard/InputField'
import TestEditor from "@/components/wizard/TestEditor";

export default {
  name: 'WizardTest',
  components: {TestEditor, InputField},
  props: ['data', 'docs'],
  data() {
    return {
      selectedPlugin: '',
      newPlugin: ''
    }
  },
  created() {
    this.selectedPlugin = this.data.plugins[0]
  },
  methods: {
    addPlugin() {
      this.data.plugins.push({
        id: this.newPlugin,
        label: '',
        modules: [],
        props: {}
      })
      this.newPlugin = ''
    }
  }
}
</script>

<style scoped>

</style>
