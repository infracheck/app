<template>
  <div>
    <v-row no-gutters>
      <v-col md="3" sm="12">
        <v-subheader>
          MODULES
          <v-divider></v-divider>
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
        <v-list shaped>
          <v-list-item-group
          >
            <v-list-item
              color="accent"
              class="grey darken-3"
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
      <v-col v-if="selectedPlugin" class="grey darken-4" md="9" sm="12">
        <v-row>
          <v-col lg="6" md="12">
            <v-text-field
              hide-details
              color="accent"
              v-model="selectedPlugin.label"
              hint="Use the label to tag your plugin sets. Use it as a short description of what you test with this Plugin."
              label="Label"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col
            v-for="(fieldDoc, fieldKey) in docs[selectedPlugin.id].props"
            :key="fieldKey"
            cols="12"
            md="6"
            lg="4"
          >
            <InputField
              :input.sync="selectedPlugin.props[fieldKey]"
              :field_label="fieldKey"
              :field_documentation="fieldDoc"
            />
            <!--DEBUG ONLY <pre>PARENT: {{selectedPlugin.props[fieldKey]}}</pre>-->
          </v-col>
        </v-row>
        <v-subheader>
          MODULES
          <v-divider></v-divider>
        </v-subheader>

        <v-row v-if="selectedPlugin" class="pa-3">
          <v-col cols="6">
            <v-subheader>TESTSET</v-subheader>
            <v-expansion-panels inset>
              <v-expansion-panel
                v-for="(module, i) in selectedPlugin.modules"
                :key="i"
                class="mb-1"
              >
                <v-expansion-panel-header class="pt-5" color="secondary darken-2">
                  <v-row no-gutters>
                    <v-col cols="12">
                      <label>
                        {{ module.label }}
                      </label>
                    </v-col>
                    <v-col cols="12">
                      <small>
                        {{ module.id }}
                      </small>
                    </v-col>
                  </v-row>
                </v-expansion-panel-header>
                <v-expansion-panel-content color="lighten-3">
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        hide-details
                        color="accent"
                        v-model="module.label"
                        hint="Label of this module. Write a short text to describe this test."
                        label="Label"
                      />
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col
                      v-for="(fieldDoc, fieldKey) in docs[selectedPlugin.id].modules[module.id].props"
                      :key="fieldKey"
                      cols="12"
                      lg="6"
                      md="12"
                    >
                      <InputField
                        :input.sync="module.props[fieldKey]"
                        :field_label="fieldKey"
                        :field_documentation="fieldDoc"
                      />
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="6">
                      <v-btn depressed block target="_blank"
                             :href="`/documentation/${selectedPlugin.id}/${module.id}`">
                        <v-icon>mdi-share-all-outline</v-icon>
                        documentation
                      </v-btn>
                    </v-col>
                    <v-col cols="6">
                      <v-btn
                        block
                        depressed
                        @click="selectedPlugin.modules = selectedPlugin.modules.filter(mod => mod !== module)"
                      >
                        <v-icon color="grey lighten-1">
                          mdi-delete
                        </v-icon>
                        Remove
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-col>
          <v-col cols="6">
            <v-subheader>MODULES</v-subheader>
            <v-list class="pt-0">
              <v-list-item
                v-for="(module, moduleName) in docs[selectedPlugin.id].modules"
                :key="moduleName"
                class="mb-1 secondary darken-2"
              >
                <v-list-item-content>
                  <v-list-item-title>
                    {{ moduleName }}
                  </v-list-item-title>
                </v-list-item-content>

                <v-list-item-action>
                  <v-btn color="primary" small @click="addModule(moduleName)">
                    <v-icon color="grey lighten-1">
                      mdi-plus-thick
                    </v-icon>
                    Add
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import InputField from '@/components/wizard/InputField'

export default {
  name: 'WizardTest',
  components: {InputField},
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
      this.selectedPlugin = this.data.plugins[this.data.plugins.length - 1]
    },
    addModule(moduleName) {
      this.selectedPlugin.modules.push(
        {
          id: moduleName,
          props: {}
        }
      )
    }
  }
}
</script>

<style scoped>

</style>
