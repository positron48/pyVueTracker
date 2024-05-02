const path = require('path')

module.exports = {

  // Root files
  root: path.resolve(__dirname, '..'),

  // Source files
  src: path.resolve(__dirname, '../src'),

  // Static files
  static: path.resolve(__dirname, '../static'),

  // Production build files
  build: path.resolve(__dirname, '../dist'),
}
