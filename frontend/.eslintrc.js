// eslint-disable-next-line import/no-extraneous-dependencies
const { createConfig } = require('@openedx/frontend-build');

const config = createConfig('eslint');

config.rules = {
  ...config.rules,
  'import/no-unresolved': ['error', {
    ignore: ['@openedx/openedx-ai-extensions-ui', '@tanstack/react-query'],
  }],
};

module.exports = config;
