<template>
  <v-col md="12" class="pa-0">
    <v-list-item>
      <v-list-item-content>{{ label }}</v-list-item-content>
      <v-list-item-content class="align-end">
        {{ value }}
      </v-list-item-content>
    </v-list-item>
  </v-col>
</template>

<script>
export default {
  name: 'ListItem',
  props: ['label', 'value']
}
</script>

<style scoped>

</style>
