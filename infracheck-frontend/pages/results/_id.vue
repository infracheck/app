<template>
  <ResultTable :result="result"></ResultTable>
</template>

<script>
import ResultTable from '@/components/results/ResultTable'

export default {
  name: 'result',
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
