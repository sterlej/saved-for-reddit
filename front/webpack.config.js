"use strict";
var webpack = require('webpack');
var path = require('path');
var loaders = require('./webpack.loaders');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var DashboardPlugin = require('webpack-dashboard/plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var BundleTracker = require('webpack-bundle-tracker');

const HOST = process.env.HOST || "127.0.0.1";
const PORT = process.env.PORT || "8888";


loaders.push({
	test: /\.scss$/,
	loaders: ['style-loader', 'css-loader?importLoaders=1', 'sass-loader'],
	exclude: ['node_modules']
});

module.exports = {
	entry: [
		'webpack-dev-server/client?http://localhost:3000',
		'webpack/hot/only-dev-server',
		// 'react-hot-loader/patch',
		'./src/index.jsx', // your app's entry point
	],
	devtool: process.env.WEBPACK_DEVTOOL || 'eval-source-map',
	output: {
		publicPath: 'http://localhost:3000/static/',
		path: path.resolve('static/'),
		// path: path.join(__dirname, '../reddit_saved/static'),
		filename: 'bundle.js'
	},
	resolve: {
		extensions: ['.js', '.jsx']
	},
	module: {
		loaders
	},
	devServer: {
		// contentBase: "./public",
		contentBase: "../reddit_saved/static",
		// do not print bundle build stats
		noInfo: true,
		// enable HMR
		hot: true,
		// embed the webpack-dev-server runtime into the bundle
		inline: true,
		// serve index.html in place of 404 responses to allow HTML5 history
		historyApiFallback: true,
		port: PORT,
		host: HOST,
		proxyTable: {
	        '/api': {
	            target: 'http://127.0.0.:8000',
	            changeOrigin: true
	        }
	    }
	},
	plugins: [
		new BundleTracker({filename: './webpack-stats.json'}),
		new webpack.NoEmitOnErrorsPlugin(),
		new webpack.HotModuleReplacementPlugin(),
		new ExtractTextPlugin({
				filename: 'style.css',
				allChunks: true
		}),
		
		new DashboardPlugin(),
		new HtmlWebpackPlugin({
			template: './src/template.html',
			files: {
				css: ['style.css'],
				js: [ "bundle.js"],
			}
		}),
	]
};
