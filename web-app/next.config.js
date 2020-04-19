const withTM = require('next-transpile-modules')(['react-responsive-music-player']);

const BUILD_ENV_KEYS_TO_SET_IN_APP = [
  'SKIP_PREFLIGHT_CHECK',
  'REACT_APP_FIREBASE_API_KEY',
  'REACT_APP_FIREBASE_AUTH_DOMAIN',
  'REACT_APP_FIREBASE_DATABASE_URL',
  'REACT_APP_GOOGLE_PROJECT_ID',
  'REACT_APP_FIREBASE_STORAGE_BUCKET',
  'REACT_APP_FIREBASE_MESSAGING_SENDER_ID',
  'REACT_APP_FIREBASE_APP_ID',
  'REACT_APP_PHONE_NUMBER'
];

module.exports = withTM({
  env: BUILD_ENV_KEYS_TO_SET_IN_APP.reduce((envObject, key) => {
    return {
      ...envObject,
      [key]: process.env[key],
    }
  }, {}),
  exportTrailingSlash: true,
  exportPathMap: function () {
    return {
      '/': {page: '/'}
    };
  },
});
