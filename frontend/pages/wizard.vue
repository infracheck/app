<template>
  <v-container fluid>
    <v-row>
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
            <WizardMeta :data="data" />
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
            <wizard-plugin :data="data" :docs="docs" />
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
            <wizard-test :data="data" :docs="docs" />
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
            <ResultTable v-if="result" :result="result" />
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
      data: {
        name: '',
        description: '',
        plugins: []
      }
    }
  },
  methods: {
    async launchTest () {
      this.loading = true
      const result = await this.$axios.post('/test', this.data)
      this.result = result.data
      this.loading = false
    }
  }
}
</script>

<style scoped>

</style>
