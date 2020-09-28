<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">
            Name
          </th>
          <th class="text-left">
            Type
          </th>
          <th class="text-left">
            Default / Value
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(value, key) in props" :key="key">
          <td>{{ key }}</td>
          <td>{{ value.type }}</td>
          <td v-if="value.default">
            {{ value.default }}
          </td>
          <td v-else-if="value.value">
            {{ value.value }}
          </td>
          <td v-else />
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script>
export default {
  name: 'PropTable',
  props: {
    props: Object
  }
}
</script>

<style scoped>

</style>
