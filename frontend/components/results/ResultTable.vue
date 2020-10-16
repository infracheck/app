<template>
  <v-row>
    <v-col cols="12">
      <v-card outlined elevation="10">
        <v-card-title>
          <h1>{{ result.label }}</h1>
        </v-card-title>
        <v-card-subtitle>
          <h3>General data</h3>
        </v-card-subtitle>
        <v-card-text>
          <v-list dense>
            <ListItem label="Date" :value="result.date"/>
            <ListItem label="Description" :value="result.description"/>
          </v-list>
          <v-alert
            dense
            prominent
            :type="result.failure_count > 0 ? 'error':'success'"
          >
            {{ result.message }}
          </v-alert>
        </v-card-text>
      </v-card>
    </v-col>
    <v-col
      v-for="plugin in result.plugin_result"
      :key="plugin.id"
      cols="12"
    >
      <v-card outlined elevation="10">
        <v-card-title class="ml-1 mt-1">
          <v-badge
            left
            color="secondary"
            :content="plugin.module_result.length"
          >
            <h2>{{ plugin.label }}</h2>
          </v-badge>
        </v-card-title>
        <v-card-subtitle>
          <h3>{{ plugin.plugin_name }} {{plugin.plugin_version}}</h3>
        </v-card-subtitle>
        <v-card-text>
          <v-list dense>
            <ListItem label="Total tests" :value="plugin.total_count"/>
            <ListItem label="Successful tests" :value="plugin.success_count"/>
            <ListItem label="Failed tests" :value="plugin.failure_count"/>
          </v-list>
          <v-expansion-panels flat focusable>
            <v-expansion-panel class="ma-0 pa-0">
              <v-expansion-panel-header class="pl-4">
                Input Properties
              </v-expansion-panel-header>
              <v-expansion-panel-content class="p-0">
                <PropTable :props="plugin.props"/>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-expansion-panels>
          <v-alert
            class="mt-2"
            dense
            :type="plugin.failure_count > 0 ? 'error':'success'"
          >
            {{ plugin.message }}
          </v-alert>


          <v-row>
            <v-col
              v-for="module in plugin.module_result"
              :key="module.id"

              lg="6"
              md="12"
            >
              <v-card outlined flat elevation="0">
                <v-card-title>
                  <h3>{{ module.label }}</h3>

                </v-card-title>
                <v-card-subtitle>
                  <h4>{{ module.module_name }} {{ module.module_version }}</h4>
                </v-card-subtitle>
                <v-card-text>
                  <v-expansion-panels flat focusable>
                    <v-expansion-panel v-if="module.result_data !== {}">
                      <v-expansion-panel-header class="pl-4">
                        Custom results
                      </v-expansion-panel-header>
                      <v-expansion-panel-content class="pa-0">
                        <pre class="pa-2 rounded">{{ module.result_data }}</pre>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                    <v-expansion-panel v-if="module.props !== {}">
                      <v-expansion-panel-header class="pl-4">
                        Input Properties
                      </v-expansion-panel-header>
                      <v-expansion-panel-content class="pa-0">
                        <PropTable :props="module.props"/>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                  <v-alert
                    dense
                    class="mt-2"
                    :type="module.result_successful ? 'success' : 'error'"
                  >
                    {{ module.result_message ? module.result_message : 'Test successful' }}
                  </v-alert>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import ListItem from '@/components/results/ListItem'
import PropTable from '@/components/documentation/PropTable'

export default {
  name: 'ResultTable',
  components: {
    PropTable,
    ListItem
  },
  props: {
    result: {
      type: Object
    }
  }
}
</script>

<style scoped>

</style>
