# Front end

In general, front end code is in the [frontend](../frontend/) directory.

This guide is about the nuts-and-bolts of developing front end code; for
details on how to use or style individual components, see the
[style guide][].

## The static asset generator

If you haven't already, make sure you've followed the
[setup guide](setup.md); it explains how to run `docker-compose up`,
which (among other things) will watch for changes to front end
code and re-build bundles as needed.

All the static assets (SASS for CSS and ES6 JavaScript) are
located in the [frontend/source/](../frontend/source/) directory. Outputs
from the static asset generator are placed in
`frontend/static/frontend/built/`.

Examine [gulpfile.js](../gulpfile.js) for details about the generator's
pipeline.

If you just want to build the assets once without watching for changes, run:

```sh
docker-compose run app yarn gulp build
```

## Developing the front end

### JavaScript
Globally, we use [yarn][] to manage our node dependencies and run node tasks.
`yarn`, in addition to being faster than using `npm install`, has the
benefit of locking dependency versions via a `yarn.lock` file.
Read the [yarn workflow docs][] if you are not familiar with how to use it.

Parts of the site use React and Redux. More information available below.

### CSS
We use [Sass](https://sass-lang.com/) for our stylesheets. Their [basics guide](https://sass-lang.com/guide)
is a good place to start if you've not used it before. Sass allows us to abstract frequently used parts of
the CSS into reusable components like variables and mixins. Some variables come directly from the
[U.S. Web Design System](https://github.com/uswds/uswds/blob/develop/src/stylesheets/core/_variables.scss)
and we define new values for them in
[frontend/source/sass/base/_uswds_variables.scss](../frontend/source/sass/base/_uswds_variables.scss).
Other variables are specific to CALC, and those are defined in
[frontend/source/sass/base/_variables.scss](../frontend/source/sass/base/_variables.scss).

This project generally follows a modified [BEM](https://frontend.18f.gov/css/naming/#bem) (Block, Element, Modifier)
naming scheme. This prevents namespace collisions and alleviates the need for too much nested Sass.

The Sass files follow a few conventions:
- Core styles are divided into four categories: [admin](../frontend/source/sass/admin/) (controls styling for the Django site admin),
[base](../frontend/source/sass/base/) (styles like resets, grid, and variables), [components](../frontend/source/sass/components/)
(individual site components like the header and footer), and [libs](../frontend/source/sass/libs/) (vendored CSS).
- All of the site's core styles are imported in [frontend/source/sass/main.scss](../frontend/source/sass/main.scss).
- Partials (also called includes or imports) are files that will get compiled into the main CSS file. These are prefixed
with an underscore (such as `components/_footer.scss`).

A more detailed explanation of how to use specific components can be found in the CALC [style guide][].

### Templates
The site makes use of Django's templating system to ensure common elements like the header, navigation, and footer are applied
consistently. The main base template lives at [data_explorer/templates/base.html](../data_explorer/templates/base.html).

## Site section-specific implementation details

Different parts of CALC are constructed in different ways, so
developing the front end depends on which part you want to change.

There are three distinct sections of the site that rely on different technologies:
The data explorer (the publicly available tool that lives at `calc.gsa.gov`),
the data capture tool (which encapsulates both the workflow that starts at
`calc.gsa.gov/data-capture/step/1` and the bulk upload available to site admins
at `calc.gsa.gov/data-capture/bulk/region-10/step/1`), and the site admin
(the place site admins can approve submitted price lists, manage users, and more,
available at `calc.gsa.gov/admin/`).

### Data explorer

The data explorer is a [React][]-based app that uses [Redux][] for data flow and state management. It's located in [frontend/source/js/data-explorer](../frontend/source/js/data-explorer/).

#### Testing

The data explorer's test suite uses [Jest][], and the tests are located in [frontend/source/js/data-explorer/tests](../frontend/source/js/data-explorer/tests/).

To run all the tests, run:

```sh
docker-compose run app yarn test
```

You can also run the tests in a continuous "watch" mode, which re-runs tests as you change your code:

```sh
docker-compose run app yarn test:watch
```

You can run `jest` directly, too: `docker-compose run app jest`, followed by any [Jest CLI options](https://facebook.github.io/jest/docs/cli.html).

#### Analyzing bundles

To see a visual representation of the bundles generated by Webpack, you can use `webpack-bundle-analyzer`.

```sh
docker-compose run app yarn gulp build
docker-compose run -p 8888:8888 app yarn analyze-webpack
```

Then visit http://localhost:8888 to explore the modules that comprise each bundle.

### Data capture

Data capture largely consists of Django templates combined with
HTML5 Custom Elements to provide a progressively-enhanced experience.

The source code is located in
[frontend/source/js/data-capture](../frontend/source/js/data-capture/).

Tests are [QUnit][]-based and are located in
[frontend/source/js/tests](../frontend/source/js/tests/).
They are run as part of our Python test suite via [frontend/tests/test_qunit.py](../frontend/tests/test_qunit.py).

You can also visit [`/tests/`](http://localhost:8000/tests/) on your local development instance to run the [QUnit][] tests directly in your browser.

### Site admin

We skin the Django administrative UI to look like part of the CALC
site; its templates are located in
[calc/templates/admin](../calc/templates/admin).

### Other components

Other parts of CALC are usually stored in either Django templates
or somewhere under the [frontend/source/](../frontend/source/)
hierarchy.

When in doubt, see the [style guide][]!

[QUnit]: https://qunitjs.com/
[React]: https://facebook.github.io/react/
[Redux]: http://redux.js.org/
[Jest]: https://facebook.github.io/jest/
[style guide]: https://calc-dev.app.cloud.gov/styleguide/
[yarn]: https://yarnpkg.com/
[yarn workflow docs]: https://yarnpkg.com/en/docs/yarn-workflow
