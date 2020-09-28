<template>
  <v-row
    no-gutters
    class="fill-height"
  >
    <v-col
      cols="12"
    >
      <ResultTable :result="result" />
    </v-col>
  </v-row>
</template>

<script>
import ResultTable from '@/components/results/ResultTable'

export default {
  name: 'Result',
  components: { ResultTable },
  async asyncData ({ $axios, params }) {
    const result = await $axios.$get(process.env.baseUrl + '/results/' + params.id)
    return { result }
  },
  async validate ({ params, $axios }) {
    const result = await $axios.$get(process.env.baseUrl + '/results/' + params.id)
    return result
  }
}
</script>

<style scoped>

</style>
