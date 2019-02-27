'use strict';
const path = require('path');
const gulp = require('gulp');
const sass = require('gulp-sass');
const sourcemaps = require('gulp-sourcemaps');
const del = require('del');

const PROJECT_DIR = path.resolve(__dirname);
const SASS_FILES = `${PROJECT_DIR}/core/sass/**/*.scss`;
const CSS_DIR = `${PROJECT_DIR}/core/static/styles`;
const CSS_FILES = `${PROJECT_DIR}/core/static/styles/**/*.css`;
const CSS_MAPS = `${PROJECT_DIR}/core/static/styles/**/*.css.map`;
const FLAGS_SRC = [
  `${PROJECT_DIR}/node_modules/flag-icon-css/**/*.svg`,
  `${PROJECT_DIR}/node_modules/flag-icon-css/**/*.min.css`,
];
const FLAGS_DEST = `${PROJECT_DIR}/core/static/vendor/flag-icons`;

gulp.task('clean', function() {
  return del([CSS_FILES, CSS_MAPS, FLAGS_DEST])
});

gulp.task('flags', function() {
  return gulp.src(FLAGS_SRC)
  .pipe(gulp.dest(FLAGS_DEST));
})

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
  gulp.watch(
    [SASS_FILES],
    ['sass:compile']
  );
});

gulp.task('sass', ['clean', 'sass:compile', 'flags']);

gulp.task('default', ['sass', 'flags']);
