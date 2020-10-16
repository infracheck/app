<template>
  <v-layout
    column
    justify-center
    align-center
  >
    <v-flex
      xs12
      sm8
      md6
    >
      <div class="text-center"/>
      <v-card outlined>
        <v-card-title class="headline">
          <img src="~assets/logo_white.png" alt="infracheck icon">
        </v-card-title>
        <v-card-subtitle>
          Infrastructure Testing - Plug in system - REST API
        </v-card-subtitle>
        <v-card-text>
          <h1>Welcome</h1>
          <p>
            This tool gives you a universal codeless test server. <br>
            Send simple json files to InfraCheck and start complex test flows. <br>
            Custom plugins and modules extend the functionality of this tool. <br>
            If you need to perform complicated test operations, write them once, as a plugin or module and share them
            with everybody. <br>
            This tool grows, as you do.
          </p>

          <h3>Why InfraCheck?</h3>
          <p class="h4 ml-1">
            Are your tired of programming your test code? <br>
            Would you like to test your infrastructure more often?<br>
            Is testing so far more of a chore?
          </p>
          Did you answer any of these questions with yes? Then <b>InfraCheck</b> could help you.
          <h3>Features</h3>
          <ul>
            <li>Codeless testing - No need to write complicated code</li>
            <li>🌷 Plugin system - Share your modules and benefit from the work of others</li>
            <li>⏰ Fast and superior - Define complex test sets within minutes using existing plugins</li>
            <li>🍕 Sharing of results - Share your results the way you like</li>
            <li>🌴 Automate everything - Using the <b>InfraCheck</b> API you can easily automate your tests</li>
          </ul>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            color="primary"
            nuxt
            to="/wizard"
          >
            Launch you first test ...
          </v-btn>
          <v-btn
            nuxt
            to="/results"
          >
            Results ...
          </v-btn>
          <v-btn
            nuxt
            to="/documentation"
          >
            Documentation ...
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>

export default {
  components: {},
  methods: {
    async refresh() {
      // Not used for now, but should be implemented on every page later
      try {
        await this.$auth.refreshTokens()

      } catch (err) {
        console.log(err);
      }
    }
  }
}
</script>
