<template>
  <v-footer
    padless
    class="caption"
  >
    <v-row
      justify="center"
      no-gutters
    >
      <v-btn
        v-for="(link, key) in links"
        link
        :key="link"
        :to="link"
        nuxt
        text
        shaped
        class="my-2 caption"
      >
        {{ key }}
      </v-btn>
      <v-col
        class=" py-4 text-center"
        cols="12"
      >
        {{ new Date().getFullYear() }} — <strong>InfraCheck</strong>
      </v-col>
    </v-row>
  </v-footer>
</template>

<script>
export default {
  name: 'Footer',
  data: () => ({
    links: {
      Home: '/',
      wizard: '/wizard',
      Documentation: '/documentation',
      Results: '/results'
    }
  })
}
</script>

<style scoped>

</style>
