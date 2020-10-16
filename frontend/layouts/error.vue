<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12" flat outlined>
          <v-card-title class="headline">
            <img src="~assets/logo_white.png" alt="infracheck icon">
          </v-card-title>
          <v-card-subtitle>
            <h1>Error occured</h1>
          </v-card-subtitle>
          <v-card-text>
            <v-alert color="error">
              Error {{ error.statusCode }}: {{ error.message }}
            </v-alert>
            <v-btn
              block
              color="primary"
              nuxt
              :to="[401,500].includes(error.statusCode) ? '/login':'/'"
            >
              <v-icon
                left
              >
                mdi-arrow-left-circle
              </v-icon>
              Go back
            </v-btn>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  layout: 'empty',
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      pageNotFound: '404 Not Found',
      otherError: 'An error occurred'
    }
  },
  head() {
    const title =
      this.error.statusCode === 404 ? this.pageNotFound : this.otherError
    return {
      title
    }
  }
}
</script>

<style scoped>
h1 {
  font-size: 20px;
}
</style>
