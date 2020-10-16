export default function ({ $axios, redirect }) {
  const PRODUCTION = process.env.NODE_ENV === 'production'

  if (!PRODUCTION) {
    $axios.onRequest((config) => {
      console.log('Making request to ' + config.baseURL + ' ' + config.url)
    })

    $axios.onResponse((response) => {
      console.log('Response with ' + response.status)
    })
  }
}
