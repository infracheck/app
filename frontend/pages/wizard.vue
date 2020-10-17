<template>
  <v-row class="fill-height" no-gutters dense>
    <v-dialog
      v-model="dialog"
      max-width="500"
    >
      <v-card>
        <v-card-title class="headline">
          Import from JSON...
        </v-card-title>
        <v-textarea
          v-if="importData"
          v-model="insertJSON"
          filled
          color="accent"
          label="JSON"
        />
        <v-textarea
          color="accent"
          v-if="exportData"
          label="JSON"
          :value="JSON.stringify(data)"
        />
        <v-card-actions>
          <v-spacer/>
          <v-btn
            color="accent"
            text
            @click="dialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            v-if="importData"
            color="accent"
            text
            @click="loadJson"
          >
            Import
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-col cols="12" class="fill-height">
      <v-card class="fill-height">
        <v-card-title> Test Wizard</v-card-title>
        <v-card-text class="pa-0">
          <div class="ml-2">
            <v-alert dismissible v-if="alert" transition="scale-transition" class="mt-2" :type="alert.type">
              {{ alert.text }}
            </v-alert>
            <v-btn
              color="secondary"
              @click="dialog=true;exportData=false;importData=true"
            >
              Import JSON...
            </v-btn>
            <v-btn
              color="secondary"
              @click="dialog=true;exportData=true;importData=false;"
            >
              Export JSON...
            </v-btn>
          </div>
          <v-stepper
            non-linear
            class="rounded-0 elevation-0 transparent mt-2"
            v-model="step"
          >
            <v-stepper-header class="blue-grey darken-4">
              <v-stepper-step
                color="accent"
                editable
                step="1"
                :complete="Boolean(data.description) && Boolean(data.description)"
              >
                Meta
                <small>Define your testsets meta data</small>
              </v-stepper-step>
              <v-divider></v-divider>
              <v-stepper-step
                color="accent"
                editable
                step="2"
                :complete="data.plugins.length>0"
              >
                Test set
                <small>Add Plugins and Modules</small>
              </v-stepper-step>
              <v-divider></v-divider>
              <v-stepper-step editable color="accent" step="3">
                Result
              </v-stepper-step>
            </v-stepper-header>
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="accent"
            />
            <v-stepper-items>
              <v-stepper-content step="1">
                <WizardMeta :data="data"/>
                <v-btn
                  color="accent"
                  @click="step = 2"
                >
                  Continue
                </v-btn>
              </v-stepper-content>
              <v-stepper-content class="pa-0" step="2">
                <wizard-test :data="data" :docs="docs"/>
                <v-btn
                  color="accent"
                  @click="step=3"
                  :disabled="data.plugins.length === 0"
                >
                  Ready for launch
                </v-btn>
                <v-btn text @click="step=1">
                  Back
                </v-btn>
              </v-stepper-content>
              <v-stepper-content step="3">
                <v-btn
                  color="accent"
                  @click="launchTest"
                >
                  Launch test
                </v-btn>
                <v-btn text @click="step=2">
                  Back
                </v-btn>
                <ResultTable v-if="result" :result="result"/>
              </v-stepper-content>
            </v-stepper-items>

          </v-stepper>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import ResultTable from '@/components/results/ResultTable'
import WizardMeta from '@/components/wizard/WizardMeta'
import WizardTest from '@/components/wizard/WizardTest'

export default {
  name: 'Wizard',
  components: {
    WizardTest,
    WizardMeta,
    ResultTable
  },
  async asyncData({$axios}) {
    const docs = await $axios.$get('/plugins')
    return {docs}
  },
  data() {
    return {
      step: 1,
      result: null,
      loading: false,
      dialog: false,
      insertJSON: '',
      alert: null,
      exportData: true,
      importData: true,
      data: {
        label: '',
        description: '',
        plugins: []
      }
    }
  },
  methods: {
    async launchTest() {
      this.loading = true
      const result = await this.$axios.post('/test', this.data)
      this.result = result.data
      this.loading = false
    },
    loadJson() {
      try {
        this.data = JSON.parse(this.insertJSON)
        this.alert = {
          text: 'JSON import was successful.',
          type: 'success'
        }
      } catch (e) {
        this.alert = {
          text: 'Your JSON is malformed.',
          type: 'error'
        }
      } finally {
        this.insertJSON = ''
        this.dialog = false
      }
    }
  }
}
</script>

<style scoped>

</style>
