import colors from 'vuetify/es5/util/colors'
import refresh from "@nuxtjs/auth-next/dist/schemes/refresh";

const PRODUCTION = process.env.NODE_ENV === 'production'
const AUTHENTICATION = process.env.SECURE ? process.env.SECURE : PRODUCTION

export default {
  /*
  ** Nuxt rendering mode
  ** See https://nuxtjs.org/api/configuration-mode
  */
  ssr: true,
  /*
  ** Nuxt target
  ** See https://nuxtjs.org/api/configuration-target
  */
  target: 'server',
  debug: !PRODUCTION,
  /*
  ** Headers of the page
  ** See https://nuxtjs.org/api/configuration-head
  */
  head: {
    titleTemplate: '%s - ' + process.env.npm_package_name,
    title: 'InfraCheck',
    meta: [
      {charset: 'utf-8'},
      {
        name: 'viewport',
        content: 'width=device-width, initial-scale=1'
      },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [
      {
        rel: 'icon',
        type: 'image/x-icon',
        href: '/favicon.ico'
      }
    ]
  },
  /*
  ** Global CSS
  */
  css: [
    '~/assets/style.scss',
  ],
  /*
  ** Plugins to load before mounting the App
  ** https://nuxtjs.org/guide/plugins
  */
  plugins: [
    '@/plugins/Markdown.js',
    '~/plugins/axios'
  ],
  /*
  ** Auto import components
  ** See https://nuxtjs.org/api/configuration-components
  */
  components: true,
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    '@nuxt/typescript-build',
    '@nuxtjs/vuetify'
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/auth-next'
  ],
  /*
  ** Authentication
  ** https://auth.nuxtjs.org/guide/middleware.html
  ** https://dev.auth.nuxtjs.org/schemes/refresh
  */
  router: AUTHENTICATION ? {
    middleware: ['auth']
  } : {},
  auth: AUTHENTICATION ? {
    cookie: {
      options: {
        sameSite: 'lax'
      }
    },
    strategies: {
      local: {
        scheme: 'refresh',
        token: {
          property: 'access_token',
          maxAge: 1800
          // type: 'Bearer'
        },
        refreshToken: {
          property: 'refresh_token',
          data: 'refresh_token',
          maxAge: 60 * 60 * 24 * 30,
          required: true,
          tokenRequired: true
        },
        endpoints: {
          login: {
            url: '/login',
            method: 'post'
          },
          refresh: {
            url: '/refresh', // TODO: Send refresh token in authorization header
            method: 'post'
          },
          logout: {
            url: '/logout',
            method: 'post'
          },
          user: false,
          autoLogout: true
        }
      }
    }
  } : {},
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  * baseURL => URL for server
  * browserBaseURL => URL for clients
  */
  axios: {
    proxy: true,
    retry: {retries: 3},
    baseURL: PRODUCTION ? 'http://backend:8080' : 'http://127.0.0.1:5000',
    browserBaseURL: PRODUCTION ? '/api/' : 'http://127.0.0.1:5000'
  },
  /*
  ** vuetify module configuration
  ** https://github.com/nuxt-community/vuetify-module
  */
  vuetify: {
    theme: {
      dark: true,
      themes: {
        light: {
          primary: colors.indigo.base,
          secondary: colors.blueGrey.base,
          accent: colors.teal.base,
          error: colors.red.base,
          warning: colors.orange.base,
          info: colors.lightBlue.base,
          success: colors.lightGreen.darken2
        },
        dark: {
          primary: colors.indigo.base,
          secondary: colors.blueGrey.base,
          accent: colors.teal.base,
          error: colors.red.base,
          warning: colors.orange.base,
          info: colors.lightBlue.base,
          success: colors.lightGreen.darken2
        }
      }
    }
  },
  /*
  ** Build configuration
  ** See https://nuxtjs.org/api/configuration-build/
  */
  build: {
    transpile: ['@nuxtjs/auth']
  }
}
