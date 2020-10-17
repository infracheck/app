<template>
  <v-container class="pt-0">
    <v-subheader>
      PLUGIN DATA
    </v-subheader>
    <v-row>
      <v-col lg="6" md="12">
        <v-text-field
          hide-details
          color="accent"
          v-model="plugin.label"
          placeholder="Use the label to describe your test target"
          label="Label"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col
        v-for="(fieldDoc, fieldKey) in docs[plugin.id].props"
        :key="fieldKey"
        cols="12"
        md="6"
        lg="4"
      >
        <InputField
          :input.sync="plugin.props[fieldKey]"
          :field_label="fieldKey"
          :field_documentation="fieldDoc"
        />
        <!--DEBUG ONLY <pre>PARENT: {{plugin.props[fieldKey]}}</pre>-->
      </v-col>
    </v-row>
    <v-subheader>
      MODULE DATA
      <v-divider></v-divider>
    </v-subheader>

    <v-row class="pa-3">
      <v-col cols="6">
        <v-alert outlined color="secondary" v-if="!plugin.modules || plugin.modules.length === 0"> Please add some
          modules to start ...
        </v-alert>
        <v-expansion-panels inset>
          <v-expansion-panel
            v-for="(module, i) in plugin.modules"
            :key="i"
            class="mb-1"
          >
            <v-expansion-panel-header class="pt-5" color="blue-grey darken-4">
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
                  v-for="(fieldDoc, fieldKey) in docs[plugin.id].modules[module.id].props"
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
                         :href="`/documentation/${plugin.id}/${module.id}`">
                    <v-icon>mdi-share-all-outline</v-icon>
                    documentation
                  </v-btn>
                </v-col>
                <v-col cols="6">
                  <v-btn
                    block
                    depressed
                    @click="plugin.modules = plugin.modules.filter(mod => mod !== module)"
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
        <v-list class="pt-0">
          <v-list-item
            v-for="(module, moduleName) in docs[plugin.id].modules"
            :key="moduleName"
            class="mb-1 blue-grey darken-4"
          >
            <v-list-item-content>
              <v-list-item-title>
                {{ moduleName }}
              </v-list-item-title>
            </v-list-item-content>

            <v-list-item-action>
              <v-btn color="accent" small @click="addModule(moduleName)">
                <v-icon>
                  mdi-plus-thick
                </v-icon>
                Add
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import InputField from "@/components/wizard/InputField";

export default {
  name: "TestEditor",
  components: {InputField},
  props: ["pluginInput", "docs"],
  data() {
    return {
      plugin: this.pluginInput
    }
  },
  methods: {
    update() {
      this.$emit('pluginInput:input', this.plugin);
    },
    addModule(moduleName) {
      this.plugin.modules.push(
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
