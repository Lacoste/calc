# Change log

All notable changes to this project will be documented in this file,
which uses the format described in
[keepachangelog.com](http://keepachangelog.com/). This project adheres
to [Semantic Versioning](http://semver.org/).

## [Unreleased][unreleased]

## [2.8.5][] - 2018-03-29

### Changed

- Improved performance of Region 10 bulk data upload processing (#1675).
- Switched to native PostgreSQL full-text search instead of using djorm-exp-pgfulltext (#1652).
- Upgraded to Django 1.11 (#1640).
- Upgraded to Redis 3.2 (#1647).
- Upgraded to React 15.5 (#1680).
- Upgraded dj-email-url in support of switching to Amazon SES for email sending (#1678).
- Fixed automated deployments to redeploy the main app and worker apps (#1651).
- Added coverage reporting for the Data Explorer React app (#1653).
- Setup nightly tests to be run against the production instance of CALC (#1654).
- Minimized vendor JavaScript bundle (#1655).

## [2.8.4][] - 2018-03-20

### Changed

- Use the latest version of Python 3.6.x in deployed applications (#1631).
- Fixed a bug that impacted the sending of emails from worker applications (#1599).
- Updated Code Climate config to match that services new format (#1629).
- Updated README with information about waiting for automated deploys to finish (#1598).

## [2.8.3][] - 2017-10-05

### Changed

- Fixed a bug whereby some region 10 spreadsheets would cause CALC bulk
  upload to fail (#1594).

## [2.8.2][] - 2017-10-03

### Changed

- The session cookie now expires when the user's browser is closed (#1584).
- All admin routes have the 'Cache-Control: no-cache' header to prevent browser caching (#1590).

## [2.8.1][] - 2017-10-02

### Changed

- The cross-origin security policy of the API has been hardened to
  only allow CORS requests under `/api/`, and only allow the
  `GET` and `OPTIONS` HTTP methods (#1585).

- Improved logging for price list status changes (#1579).

## [2.8.0][] - 2017-09-19

### Added

- Added additional required logging (#1569).

## [2.7.2][] - 2017-09-19

### Changed

- Switch to 3-tiered branch-based deployments (`develop`, `staging`, `master`).

## [2.7.1][] - 2017-09-19

### Changed

- Migrate from TravisCI to CircleCI.
- Upgrade to Python 3.6.2.
- Fix an issue that allowed CSVs exported from the Data Explorer to contain
  auto-running Excel formulas in the query field.

## [2.7.0][] - 2017-04-14

### Changed

- Upgraded Django to 1.9.3 (#1526).
- Upgraded jQuery to 3.2.1 (#1539).
- CALC is now prepared for migration to Django 1.10 (#1544). However,
  as the development team currently has a limited amount of time to
  work on CALC, we've decided not to actually migrate to the new
  version of Django, as we may not have time to address any problems
  occurring from the upgrade in the near future.

### Added

- Added support for recording and replaying attempted price list
  submissions (#1491), and added a new **Technical Support Specialist**
  role. This will allow the development team to better serve
  users who are having problems submitting their price lists.
- Added integration with Slack, so that the development team will be
  notified of events happening on CALC and be able to respond quickly
  to anything that needs attention (#1505).
- Added documentation on monitoring CALC (#1518).

## [2.6.0][] - 2017-03-24

### Changed

- Modified how autocomplete search results are returned from the server
  to improve the speed of retrieving, processing, showing results.
- Changed `/healthcheck/` to include an `is_everything_ok` property and
  always return `200` in order to effectively monitor that endpoint (#1516).
- Optimized client JavaScript by removing global D3, using Webpack to make
  all bundles, and switching to a React-based component for the Experience
  slider.

## [2.5.1][] - 2017-03-20

### Changed

- Fixed a bug that caused errors in the API due to a bad interaction between
  the New Relic monitor and djorm-ext-pgfulltext (#1498).

## [2.5.0][] - 2017-03-16

### Changed

- Fixed a bug in the data explorer search input that prevented searches for
  numeric strings (#1475).
- Fixed a bug in the the data explorer search input that would cause a
  JavaScript error when empty results were returned from the autocompletion
  API (#1484).
- Fixed a bug preventing Unit of Issue cells with extra spaces from passing
  validation (#1494).
- Modified the Schedule 70 price list parser to look for some variations on
  column names in order to accept more price list uploads.
- Fixed some minor styling bugs in the admin interface (#1326 and #1262).
- Upgraded CALC to use Django 1.9.

## [2.4.0][] - 2017-03-10

### Added

- When logged-in, the username in the upper right corner of the page has been
  turned into a small dropdown menu (#1413).

### Changed

- CALC now understands certain acronyms and abbreviations, such as
  "jr" (junior), "sr" (senior), and "sme" (subject matter expert). Searches
  for any of these will yield more inclusive results than before (#1378).
- System-generated emails have vastly improved styling (#1208).
- The logic to parse the minimum experience values from
  uploaded Schedule 70 price lists has been made more flexible by using the
  first numeric value encountered.
- The data explorer page now changes the page title based on the current search
  term(s) (#1315).
- Price list details pages have improved status indication styling (#980).
- Styling of the error page of the price list upload process has been improved
  (#1266).
- The Rates API now handles quotation-delimited search terms, like
  "engineer, senior" (#1459).

## [2.3.0][] - 2017-02-22

### Added

- CALC's developer documentation has been modularized and is now available at
  at `/docs/` (#1301).

### Changed

- A bug in the labor category search box that could cause the user's browser
  to lock up on special-character-only search queries has been fixed (#1355).

- The labor category search box and associated URL parameter now enforce a
  a maximum length of 255 characters (#1354).

- The navigation tabs no longer "jump" while the front page is loaded (#1341).

- Table header styling throughout CALC has been improved and made more
  consistent (#1202).

- Some minor styling bugs (#1229) and inconsistencies (#1371) in the filter box
  on the front have been corrected.

- CALC now runs on Python 3.6.0.

## [2.2.0][] - 2017-02-07

### Added

- A test suite for testing the production instance of CALC has been created
  (#1199).

### Changed

- The Schedule 70 price list parsing logic has been amended to address a bug
  where it attempted to parse rows outside of the price list table (#1318).

- Ethnio (used for recruiting users for research sessions) has been removed.

- The cloud.gov UAA authentication code has been extracted to a separate
  package called [`cg-django-uaa`](https://github.com/18F/cg-django-uaa).

- Most Python dependencies have been updated.

## [2.1.0][] - 2017-01-31

### Added

- A link to "Read about recent updates to CALC" now appears in the
  footer of every page.

### Changed

- Search queries ending with trailing commas and using the "contains phrase"
  criteria now work properly.

- CALC now validates minimum wages based on the value of $10.20 per
  hour, as set forth by
  [Executive Order 13658](https://www.dol.gov/whd/flsa/eo13658/index.htm).

- Various improvements to the copy of emails sent out by CALC have been
  made, thanks to the efforts of the 18F Writing Lab.

- Emails are also sent in HTML format (in addition to plain text) and
  include relevant links back to CALC where applicable.

- Sent emails also now have a `reply-to` header set to a valid email
  address that will be checked and responded-to by a CALC team member.

- Errors in uploaded price lists are now displayed via tooltips (#1245).

- Explicit HTTP `Cache-Control` headers are now set on responses so that
  Amazon CloudFront will behave properly when new versions of CALC are
  deployed.

- A new `manage.py send_example_emails` command has been added to make
  it easier to iterate on the emails sent by CALC.

## [2.0.0][] - 2017-01-18

### Added

- The new data capture functionality has been added, allowing COs
  to log in (via cloud.gov) and submit their approved Schedule 70
  price lists. Data administrators can then review these price lists and
  add their data into CALC.

- Additionally, data administrators can directly upload Region 10
  bulk data. The uploaded data will then replace all existing Region 10
  data in CALC.

### Changed

- In October 2015, the schedules represented in CALC were consolidated
  into the [Professional Services Schedule][pss] to give federal agency
  acquisition professionals the ability to obtain total contract solutions
  for their professional services requirements using one contract vehicle.

  Consequently, the "Schedule" filter in the data explorer has
  been renamed to the "SIN / Schedule" filter, and allows rates to be
  filtered by SIN number.

- Searching for multiple words in the data explorer's search field
  now produces expected autocompletion results.

- The data explorer is now much more keyboard-accessible and
  screenreader-friendly.

- The "proposed price" field in the data explorer automatically
  updates the histogram on a per-keypress basis; there is no longer
  any need to click the "Go" button.

- Sharing CALC links with the "Education" field filled out now works
  properly.

- The CALC banner has been redesigned to be less confusing and easier
  to read.

- Google Analytics for CALC now properly track new searches in the
  data explorer as page views. We also track clicks on links in the
  "Contract #" column of the data explorer results table.

[pss]: https://www.gsa.gov/portal/content/246403

## [1.2.0][] - 2015-07-21

- filtering empty list items out of query building

## [1.1.2][] - 2015-07-14

- Merge pull request #224 from 18F/ethnio
- Add ethnio screener

## [1.1.1][] - 2015-07-08

- hide proposed price field so that we may deploy to production
  everything but this feature

## [1.1.0][] - 2015-07-07

- Merge pull request #211 from 18F/add-histogram-design
- Updates to histogram

## [1.0.1][] - 2015-06-29

- Merge pull request #205 from 18F/search-bug
- Strip non-alpha numeric or whitespace chars out of search query

## 1.0.0 - 2015-06-24

- adds hidden proposed price starting functionality
- adds standard deviation callouts
- adds icons in header
- workflow documentation
- bug fix for stacked histogram labels
- removing python 2.7 support
- script to run django migrations on cloud foundry
- slider and drop downs to replace single drop down for years experience
- refining header wording
- replace drop down for education with multi select

[unreleased]: https://github.com/18F/calc/compare/v2.8.5...HEAD
[2.8.5]: https://github.com/18F/calc/compare/v2.8.4...v2.8.5
[2.8.4]: https://github.com/18F/calc/compare/v2.8.3...v2.8.4
[2.8.3]: https://github.com/18F/calc/compare/v2.8.2...v2.8.3
[2.8.2]: https://github.com/18F/calc/compare/v2.8.1...v2.8.2
[2.8.1]: https://github.com/18F/calc/compare/v2.8.0...v2.8.1
[2.8.0]: https://github.com/18F/calc/compare/v2.7.2...v2.8.0
[2.7.2]: https://github.com/18F/calc/compare/v2.7.1...v2.7.2
[2.7.1]: https://github.com/18F/calc/compare/v2.7.0...v2.7.1
[2.7.0]: https://github.com/18F/calc/compare/v2.6.0...v2.7.0
[2.6.0]: https://github.com/18F/calc/compare/v2.5.1...v2.6.0
[2.5.1]: https://github.com/18F/calc/compare/v2.5.0...v2.5.1
[2.5.0]: https://github.com/18F/calc/compare/v2.4.0...v2.5.0
[2.4.0]: https://github.com/18F/calc/compare/v2.3.0...v2.4.0
[2.3.0]: https://github.com/18F/calc/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/18F/calc/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/18F/calc/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/18F/calc/compare/v1.2.0...v2.0.0
[1.2.0]: https://github.com/18F/calc/compare/v1.1.2...v1.2.0
[1.1.2]: https://github.com/18F/calc/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/18F/calc/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/18F/calc/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/18F/calc/compare/v1.0.0...v1.0.1