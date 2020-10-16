<template>
  <v-btn
    class="mr-4"
    @click="logout"
    color="secondary"
  >
    <v-icon>mdi-export</v-icon>
    Log out
  </v-btn>
</template>
<script>
export default {
  name: 'LogoutButton',
  methods: {
    async logout () {
      try {
        await this.$auth.logout()
        await this.$router.push({
          path: '/login'
        })
      } catch (err) {
        console.log(err)
      }
    }
  }
}
</script>

<style scoped>

</style>
