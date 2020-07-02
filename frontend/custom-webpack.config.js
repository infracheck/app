const webpack = require('webpack');

// Defines custom plugin that is used to import system environment variables into the app when it is build
module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      $ENV: {
        SERVER: JSON.stringify(process.env.BACKEND)
      }
    })
  ]
};
