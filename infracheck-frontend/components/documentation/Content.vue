<template>
  <v-container
  >
    <v-row>
      <v-col cols="12">
        <v-card outlined class="mb-3">
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
                  class="white--text"
                  :horizontal-line="false"
                  :source="documentation.documentation"
                />
              </v-col>
              <v-col xl="4" lg="6" md="12">
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
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <div v-if="documentation.modules">
      <v-subheader>Modules</v-subheader>
      <v-divider class="mb-2"></v-divider>
      <v-row dense>
        <v-col
          v-for="(module, moduleId) in documentation.modules"
          :key="moduleId"
          lg="4"
          md="6"
          sm="12"
        >
          <v-card outlined class="mb-3">
            <v-card-text>
              <div class="overline mb-1">
                {{ module.type }}
              </div>
              <div class="headline mb-0">
                {{ moduleId }}
              </div>
              <div v-if="documentation.author" class="subtitle-2">
                Author: {{ documentation.author }}
              </div>
              <div v-if="documentation.author" class="subtitle-2">
                Author: {{ documentation.author }}
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>

  </v-container>
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
  }
}
</script>

<style>
.markdown-body a {
  color: #35b1b4;
}

</style>
