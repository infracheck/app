<template>
  <div>

    <v-row no-gutters>
      <v-col cols="12">
        <v-card flat class="mb-3 transparent">
          <v-card-text class="white--text">
            <v-row>
              <v-col xl="8" lg="6" md="12">
                <div class="overline mb-2">
                  {{ documentation.type }}
                </div>
                <div class="headline mb-1">
                  {{ documentation.id }}
                </div>
                <div v-if="documentation.author" class="subtitle-2">
                  Author: {{ documentation.author }}
                </div>

                <vue-simple-markdown
                  highlight
                  class="white--text"
                  :horizontal-line="false"
                  :source="documentation.documentation"
                />
              </v-col>
              <v-col xl="4" lg="6" md="12">
                <v-row>
                  <v-col>
                    <v-card class="mb-2" outlined>
                      <v-card-text>
                        <div class="overline mb-4">
                          Input Properties
                        </div>
                        <PropTable :props="documentation.props"/>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
                <v-subheader v-if="documentation.modules">Modules
                  <v-divider></v-divider>
                </v-subheader>
                <v-row v-if="documentation.modules">
                  <v-col cols="12">
                    <v-text-field
                      color="secondary darken-2"
                      outlined
                      dense
                      filled
                      v-model="moduleSearch"
                      label="Search modules ..."
                      prepend-inner-icon="mdi-magnify"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    v-if="module.id.includes( moduleSearch)"
                    v-for="(module, moduleId) in documentation.modules"
                    :key="moduleId"
                    md="6"
                    sm="12">
                    <v-card
                      color="secondary darken-2"
                      outlined
                      class="mb-3"
                      nuxt
                      hover
                      :to="`/documentation/${documentation.id}/${moduleId}`">
                      <v-card-title>
                        {{ moduleId }} {{ documentation.version }}
                      </v-card-title>
                      <v-card-subtitle> {{ documentation.author }}</v-card-subtitle>
                    </v-card>
                  </v-col>
                </v-row>

              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>

</template>

<script lang="ts">

import PropTable from "~/components/documentation/PropTable.vue";

export default {
  name: 'DocContent',
  components: {PropTable},
  props: {
    documentation: {
      default: {}
    },
    name: {
      type: String,
      default: ''
    }
  },
  data: () => ({
    moduleSearch: ''
  })
}
</script>

<style>
.v-application code {
  color: #2884a5;
  background: #1e1e1e;
}


</style>
