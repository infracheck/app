<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-12">
          <v-card-title class="headline">
            <img src="~assets/logo_white.png" alt="infracheck icon">
          </v-card-title>
          <v-card-text>
            <v-form
              ref="form"
              lazy-validation
            >
              <v-text-field
                v-model="login.username"
                label="Username"
                type="text"
              />
              <v-text-field
                v-model="login.password"
                label="Password"
                type="password"
              />
            </v-form>
            <v-alert v-if="failed" type="error">
              {{ failText }}
            </v-alert>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              class="mr-4 pl-8 pr-8"
              right
              large
              @click="userLogin"
              color="primary"
            >
              Log in
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  layout: 'empty',
  auth: false,
  data: () => ({
    failed: false,
    failText: '',
    login: {
      username: '',
      password: ''
    }
  }),
  methods: {
    async userLogin () {
      this.failed = false
      try {
        await this.$auth.loginWith('local', { data: this.login })
        await this.$router.push({
          path: '/'
        })
      } catch (err) {
        this.failed = true
        this.login.password = ''
        switch (err.response.status) {
          case 401:
            this.failText = 'Credentials not correct.'
            break
          case 400:
            this.failText = 'Connection failed. Did you enter both, a username and a password?'
            break
          default:
            this.failText = 'Unknown issue. Check your server and ask your admin for help.'

        }
      }
    }
  }
}
</script>
