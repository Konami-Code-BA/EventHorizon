'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')
require('dotenv').config();

module.exports = merge(prodEnv, {
    NODE_ENV: '"development"',
    PYTHON_ENV: process.env.PYTHON_ENV
})