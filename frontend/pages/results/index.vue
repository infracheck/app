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
            sort-by="date"
            :sort-desc="true"
            item-key="id"
            class="elevation-1"
            :search="search"
          >
            <template v-slot:top>
              <v-row>
                <v-col lg="4" md="12">
                  <v-text-field
                    v-model="search"
                    color="primary"
                    outlined
                    append-icon="mdi-magnify"
                    label="Search"
                  />
                </v-col>
              </v-row>
            </template>
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
                color="error"
              >
                FAILED
              </v-chip>
              <v-chip
                v-else
                color="primary"
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
    const results = await $axios.$get('/results')
    return { results }
  },
  data () {
    return {
      search: '',
      headers: [
        {
          text: 'Name',
          align: 'start',
          value: 'label'
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
          text: 'successful tests',
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
