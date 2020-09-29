<template>
  <v-app>
    <Appbar></Appbar>
    <v-main>
      <v-container fluid class="fill-height pa-0">
        <nuxt/>
      </v-container>
    </v-main>
    <Navigation></Navigation>
    <Footer/>
  </v-app>
</template>

<script>
import Footer from '@/components/Footer'
import Appbar from "~/components/Appbar";
import Navigation from "~/components/Navigation";

export default {
  components: {Navigation, Appbar, Footer},
}
</script>
