const path = require("path");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const RemovePlugin = require('remove-files-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const ImageMinimizerPlugin = require("image-minimizer-webpack-plugin");

module.exports = {
    devtool: 'source-map',
    entry: {
        cookieBanner: './core/js/src/dit.cookieBanner.js',
        reveal: './core/js/src/dit.reveal.js',
        tagging: './core/js/src/dit.tagging.js',
        videoHeroControl: './core/js/src/dit.videoHeroControl.js',
        main_styles: './core/sass/main.scss',
        atlas_styles: './core/sass/atlas/main.scss',
        atlas_header_footer_styles: './core/sass/atlas/header-footer.scss'
    },
    output: {
        path: path.resolve(__dirname, 'core', 'static', 'core'),
        filename: 'js/dit.[name]-min.js',
    },
    module: {
        rules: [
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: "css-loader",
                        options: {
                            // URLs in source are relative to compiled CSS, /static/core/styles/main.css
                            url: false
                        }
                    },
                    'sass-loader'
                ]
            },
        ],
    },
    optimization: {
        minimize: true,
        minimizer: [
            "...",
            new ImageMinimizerPlugin({
                minimizer: {
                    implementation: ImageMinimizerPlugin.sharpMinify,
                },
            }),
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: ({chunk: {name}}) => `styles/${name.replace('_styles', '')}.css`,
        }),
        new CopyWebpackPlugin({
            patterns: [
                {
                    from: './core/assets/',
                    noErrorOnMissing: true,
                },
            ]
        }),
        new RemovePlugin({
            after: {
                test: [
                    {
                        folder: './core/static/core/js',
                        method: (absoluteItemPath) => new RegExp(/_styles-min\.js(\.map)?$/).test(absoluteItemPath)
                    },
                ],
            },
        }),
    ]
}
