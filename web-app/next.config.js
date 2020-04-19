const Dotenv = require('dotenv-webpack');
const withTM = require('next-transpile-modules')(['react-responsive-music-player']);

module.exports = withTM({
  exportTrailingSlash: true,
  exportPathMap: function () {
    return {
      '/': {page: '/'}
    };
  },
  webpack: (config) => {
    config.plugins.push(new Dotenv({silent: true}));

    return config;
  }
});
