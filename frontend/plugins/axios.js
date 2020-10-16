export default function ({ $axios, redirect }) {
  const PRODUCTION = process.env.NODE_ENV === 'production'

  // $axios.onError(error => {
  //   const code = parseInt(error.response && error.response.status)
  //   if (code === 401 || code === 500) {
  //     redirect('/login')
  //   }
  // })

  if (!PRODUCTION) {
    $axios.onRequest((config) => {
      console.log('Making request to ' + config.baseURL + ' ' + config.url)
    })

    $axios.onResponse((response) => {
      console.log('Response with ' + response.status)
    })
  }
}
