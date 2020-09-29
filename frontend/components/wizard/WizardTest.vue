<template>
  <v-row>
    <v-col cols="3">
      <v-card
        flat
        tile
        outlined
      >
        <v-list shaped>
          <v-subheader>PLUGINS</v-subheader>
          <v-list-item-group
            color="primary"
          >
            <v-list-item
              v-for="(item, key) in data.plugins"
              :key="key"
              @click="selectedPlugin=data.plugins.find(x => x === item)"
            >
              <v-list-item-icon>
                <v-icon v-text="'mdi-toy-brick'"/>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="item.id"/>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-card>
    </v-col>
    <v-col v-if="selectedPlugin" cols="9">
      <v-card
        outlined
        tile
        flat
      >
        <v-subheader>PROPERTIES</v-subheader>
        <v-card-text>
          <v-row>
            <v-col
              v-for="(fieldDoc, fieldKey) in docs[selectedPlugin.id].props"
              :key="fieldKey"
              cols="12"
              md="6"
              lg="4"
              xl="3"
            >
              <InputField
                :props="selectedPlugin.props"
                :field_label="fieldKey"
                :field_documentation="fieldDoc"
              />
            </v-col>
          </v-row>
          <v-btn
            depressed
            @click="data.plugins = data.plugins.filter(plugin => plugin !== selectedPlugin); selectedPlugin = null"
          >
            Remove plugin
          </v-btn>
          <v-divider class="mt-2"/>

          <v-row v-if="selectedPlugin" class="pa-3">
            <v-col>
              <v-subheader>TESTSET</v-subheader>
              <v-expansion-panels inset>
                <v-expansion-panel
                  v-for="(module, i) in selectedPlugin.modules"
                  :key="i"
                  class="mb-1"
                >
                  <v-expansion-panel-header color="accent">
                    {{ module.id }}
                  </v-expansion-panel-header>
                  <v-expansion-panel-content color="lighten-3">
                    <v-row>
                      <v-col cols="12">
                        <vue-simple-markdown
                          class="white--text"
                          :horizontal-line="false"
                          :source="docs[selectedPlugin.id].modules[module.id].documentation"
                        />
                      </v-col>

                      <v-col
                        v-for="(fieldDoc, fieldKey) in docs[selectedPlugin.id].modules[module.id].props"
                        :key="fieldKey"
                        cols="12"
                        md="6"
                        lg="4"
                        xl="3"
                      >
                        <InputField
                          :props="module.props"
                          :field_label="fieldKey"
                          :field_documentation="fieldDoc"
                        />
                      </v-col>
                    </v-row>
                    <v-btn
                      depressed
                      @click="selectedPlugin.modules = selectedPlugin.modules.filter(mod => mod !== module)"
                    >
                      Remove
                    </v-btn>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-col>
            <v-divider vertical/>
            <v-col cols="4">
              <v-subheader>MODULES</v-subheader>

              <v-list>
                <v-list-item
                  class="mb-1 accent"
                  v-for="(module, moduleName) in docs[selectedPlugin.id].modules"
                  :key="moduleName"
                >
                  <v-list-item-content>
                    <v-list-item-title v-text="moduleName"/>
                  </v-list-item-content>

                  <v-list-item-action>
                    <v-btn color="primary" small @click="addModule(moduleName)">
                      <v-icon color="grey lighten-1">
                        mdi-plus-thick
                      </v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import InputField from '@/components/wizard/InputField'

export default {
  name: 'WizardTest',
  components: { InputField },
  props: ['data', 'docs'],
  data () {
    return {
      selectedPlugin: ''
    }
  },
  methods: {
    addModule (moduleName) {
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
