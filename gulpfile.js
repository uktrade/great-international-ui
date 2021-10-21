'use strict';
const path = require('path');
const gulp = require('gulp');
const sass = require('gulp-sass')(require('node-sass'));
const sourcemaps = require('gulp-sourcemaps');
const minify = require('gulp-minify');
const del = require('del');
const imagemin = require('gulp-imagemin');

const PROJECT_DIR = path.resolve(__dirname);
const SASS_FILES = `${PROJECT_DIR}/core/sass/**/*.scss`;
const CSS_DIR = `${PROJECT_DIR}/core/static/core/styles`;
const CSS_FILES = `${PROJECT_DIR}/core/static/core/styles/**/*.css`;
const CSS_MAPS = `${PROJECT_DIR}/core/static/core/styles/**/*.css.map`;
const JS_SRC_FILES = `${PROJECT_DIR}/core/js/src/**/*.js`;
const JS_DEST = `${PROJECT_DIR}/core/static/core/js/`;
const ASSETS_SRC = `${PROJECT_DIR}/core/assets/**/*`;
const ASSETS_DEST = `${PROJECT_DIR}/core/static/core`

gulp.task('clean', function () {
    return del([CSS_FILES, CSS_MAPS])
});

gulp.task('sass:compile', function () {
    return gulp.src(SASS_FILES)
        .pipe(sourcemaps.init())
        .pipe(sass({
            includePaths: [
                './conf/',
            ],
            outputStyle: 'compressed'
        }).on('error', sass.logError))
        .pipe(sourcemaps.write('./maps'))
        .pipe(gulp.dest(CSS_DIR));
});

gulp.task('sass:watch', function () {
    return gulp.watch(
        [SASS_FILES],
        gulp.series('sass:compile')
    );
});

gulp.task('js:minify', function () {
    return gulp.src(JS_SRC_FILES)
        .pipe(minify({
            noSource: true
        }))
        .pipe(gulp.dest(JS_DEST))
})

gulp.task('assets:copy', function () {
    return gulp.src(ASSETS_SRC)
        .pipe(imagemin())
        .pipe(gulp.dest(ASSETS_DEST))
})

gulp.task('sass', gulp.series('clean', 'sass:compile'));

gulp.task('default', gulp.parallel('sass', 'js:minify', 'assets:copy'));
