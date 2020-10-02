<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-alert v-if="alert" transition="scale-transition" class="mt-2" :type="alert.type">
          {{ alert.text }}
        </v-alert>
        <v-btn
          color="accent"
          @click="dialog=true;exportData=true;importData=false;"
        >
          Export JSON...
        </v-btn>
        <v-dialog
          v-model="dialog"
          max-width="290"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="accent"
              v-bind="attrs"
              @click="exportData=false;importData=true"
              v-on="on"
            >
              Import JSON...
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="headline">
              Import from JSON...
            </v-card-title>
            <v-textarea
              v-if="importData"
              v-model="insertJSON"
              filled
              label="JSON"
            />
            <v-textarea
              v-if="exportData"
              label="JSON"
              :value="JSON.stringify(data)"
            />
            <v-card-actions>
              <v-spacer/>
              <v-btn
                color="green darken-1"
                text
                @click="dialog = false"
              >
                Cancel
              </v-btn>
              <v-btn
                v-if="importData"
                color="green darken-1"
                text
                @click="loadJson"
              >
                Import
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-col>
      <v-col offset-md="0" offset-xl="1" xl="10" md="12">
        <v-stepper
          v-model="step"
          vertical
        >
          <!--  STEP 1  -->
          <v-stepper-step
            step="1"
            :complete="Boolean(data.description) && Boolean(data.description)"
          >
            Define Meta data
          </v-stepper-step>
          <v-stepper-content step="1">
            <WizardMeta :data="data"/>
            <v-btn
              color="primary"
              :disabled="!data.description && data.description"
              @click="step = 2"
            >
              Continue
            </v-btn>
          </v-stepper-content>

          <!--  STEP 2  -->
          <v-stepper-step
            step="2"
            :complete="data.plugins.length>0"
          >
            Select Plugins
          </v-stepper-step>

          <v-stepper-content step="2">
            <wizard-plugin :data="data" :docs="docs"/>
            <v-btn
              color="primary"
              :disabled="!data.plugins.length>0"
              @click="step = 3"
            >
              Continue
            </v-btn>
            <v-btn text @click="step=1">
              Back
            </v-btn>
          </v-stepper-content>

          <!--  STEP 3  -->
          <v-stepper-step
            step="3"
            :complete="data.plugins.length>0"
          >
            Insert data
          </v-stepper-step>

          <v-stepper-content step="3">
            <wizard-test :data="data" :docs="docs"/>
            <v-btn
              color="primary"
              @click="step=4"
            >
              Ready for launch
            </v-btn>
            <v-btn text @click="step=2">
              Back
            </v-btn>
          </v-stepper-content>
          <!--  STEP 4  -->
          <v-stepper-step step="4">
            Run test
          </v-stepper-step>

          <v-stepper-content step="4">
            <v-btn
              color="primary"
              @click="launchTest"
            >
              Launch test
            </v-btn>
            <v-btn text @click="step=3">
              Back
            </v-btn>
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="primary"
            />
            <ResultTable v-if="result" :result="result"/>
          </v-stepper-content>
        </v-stepper>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ResultTable from '@/components/results/ResultTable'
import WizardMeta from '@/components/wizard/WizardMeta'
import WizardPlugin from '@/components/wizard/WizardPlugin'
import WizardTest from '@/components/wizard/WizardTest'

export default {
  name: 'Wizard',
  components: {
    WizardTest,
    WizardPlugin,
    WizardMeta,
    ResultTable
  },
  async asyncData ({ $axios }) {
    const docs = await $axios.$get('/plugins')
    return { docs }
  },
  data () {
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
        name: '',
        description: '',
        plugins: [
        ]
      }
    }
  },
  methods: {
    async launchTest () {
      this.loading = true
      const result = await this.$axios.post('/test', this.data)
      this.result = result.data
      this.loading = false
    },
    loadJson () {
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
