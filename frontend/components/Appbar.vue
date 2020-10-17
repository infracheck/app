<template>
  <div>
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
    >
      <div class="text-center">
        <nuxt-link to="/" class="text-center">
          <img
            src="~/assets/logo_without_text.png"
            alt="infracheck logo"
          ></nuxt-link>
        <h1>InfraCheck</h1>
        <h3 class="caption">Easy infrastructure testing</h3>
      </div>
      <v-divider></v-divider>
      <v-list dense>
        <v-list-item v-for="(item,key) of items" :key="key" link :to="item.to">
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      app
      clipped-left
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
      <v-toolbar-title class="mr-12 align-center">
        InfraCheck
      </v-toolbar-title>
      <v-spacer/>
      <LogoutButton/>
    </v-app-bar>
  </div>
</template>

<script>
import LogoutButton from '~/components/LogoutButton'

export default {
  name: 'Appbar',
  components: {LogoutButton},
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-home-variant-outline',
          title: 'Getting Started',
          to: '/'
        },
        {
          icon: 'mdi-run-fast',
          title: 'Test Wizard',
          to: '/wizard'
        },
        {
          icon: 'mdi-text-box-outline',
          title: 'Documentation',
          to: '/documentation'
        },
        {
          icon: 'mdi-file-table-outline',
          title: 'Results',
          to: '/results'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'InfraCheck'
    }
  }
}
</script>

<style scoped>

</style>
