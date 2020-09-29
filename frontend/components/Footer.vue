<template>
  <v-footer
    padless
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
        rounded
        class="my-2"
      >
        {{ key }}
      </v-btn>
      <v-col
        class=" py-4 text-center accent"
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
