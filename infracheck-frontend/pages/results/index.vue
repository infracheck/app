<template>
  <v-row class="fill-height" no-gutters dense>
    <v-col class="fill-height">
      <v-card class="fill-height">
        <v-card-title>Results</v-card-title>
        <v-card-text>
          <v-data-table
            :headers="headers"
            :items="results"
            :items-per-page="13"
            item-key="id"
            class="elevation-1"
          >
            <template v-slot:item.link="{ item }">
              <v-btn
                tile
                nuxt
                :to="'results/'+item.id"
              >
                Open...
              </v-btn>
            </template>
            <template v-slot:item.result="{ item }">
              <v-chip
                v-if="item.failure_count > 0"
                color="red"
                dark
              >
                FAILED
              </v-chip>
              <v-chip
                v-else
                color="green"
                dark
              >
                SUCCESS
              </v-chip>
            </template>
          </v-data-table>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'Results',
  async asyncData ({ $axios }) {
    const results = await $axios.$get(process.env.baseUrl + '/results')
    return { results }
  },
  data () {
    return {
      headers: [
        {
          text: 'Name',
          align: 'start',
          value: 'name'
        },
        {
          text: 'Date',
          value: 'date'
        },
        {
          text: 'result',
          value: 'result'
        },
        {
          text: 'test count',
          value: 'total_count'
        }, {
          text: 'failed tests',
          value: 'failure_count'
        }, {
          text: 'successul tests',
          value: 'success_count'
        },
        {
          text: 'message',
          value: 'message'
        },
        {
          text: '',
          value: 'link'
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
