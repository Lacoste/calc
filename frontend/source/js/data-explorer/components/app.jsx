/* eslint-disable react/button-has-type, jsx-a11y/anchor-is-valid */

import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import classNames from 'classnames';

import {
  resetState,
  invalidateRates,
} from '../actions';

import histogramToImg from '../histogram-to-img';

import { trackEvent } from '../../common/ga';
import Description from './description';
import Highlights from './highlights';
import Histogram from './histogram';
import ExportData from './export-data';
import ResultsTable from './results-table';
import ProposedPrice from './proposed-price';
import QueryType from './query-type';
import LoadableOptionalFilters from './optional-filters/loadable-optional-filters';
import LaborCategory from './labor-category';
import KeywordFilter from './keyword-filter';
import LoadingIndicator from './loading-indicator';
import SearchCategory from './search-category';
import TitleTagSynchronizer from './title-tag-synchronizer';

import { autobind } from '../util';

class App extends React.Component {
  constructor(props) {
    super(props);
    autobind(this, [
      'handleSubmit',
      'handleResetClick',
      'handleDownloadClick',
    ]);
    this.state = {
      keywordDisabled: true,
      searchkeyword: "",
      resetFilter: false
    };
  }

  getContainerClassNames() {
    let loaded = false;
    let loading = false;
    let error = false;

    if (this.props.ratesInProgress) {
      loading = true;
    } else if (this.props.ratesError) {
      if (this.props.ratesError !== 'abort') {
        error = true;
        loaded = true;
      }
    } else {
      loaded = true;
    }

    return {
      search: true,
      content: true,
      container: true,
      loaded,
      loading,
      error,
    };
  }




  setKeywordDisabled(childData) {
    this.setState({ keywordDisabled: childData, resetFilter:false });
  }
  setEnteredKeyword(childData) {
    this.setState({ searchkeyword: childData, resetFilter:false });
  }

  handleSubmit(e) {
    e.preventDefault();
    this.props.invalidateRates();
  }

  handleResetClick(e) {
    e.preventDefault();
    this.props.resetState();
    this.setState({ resetFilter: true, searchkeyword: "" });
  }

  handleDownloadClick(e) {
    e.preventDefault();
    histogramToImg(
      this.histogram.getWrappedInstance().svgEl,
      this.canvasEl,
    );
    trackEvent('download-graph', 'click');
  }

  render() {
    const prefixId = name => `${this.props.idPrefix}${name}`;

    return (
      <form
        id={prefixId('search')}
        className={classNames(this.getContainerClassNames())}
        onSubmit={this.handleSubmit}
      >
        <div className="row card dominant">
          <div className="search-header columns twelve content">
            <h2>
              Search CALC
            </h2>
            <TitleTagSynchronizer />
            <section className="search">
              <div className="container clearfix">
                <div className="row">
                  <div className="twelve columns">
                    <div className="row">
                      <div className="twelve columns">
                        <SearchCategory />
                      </div>
                    </div>
                    <br />
                    <br />
                    <div className="row">
                      <div className="five columns reduce_right_margin">
                        <LaborCategory parentCallback = {this.setKeywordDisabled.bind(this)}api={this.props.api}>

                        </LaborCategory>
                      </div>
                      <div className="five columns reduce_right_margin keyword_filter">
                          <KeywordFilter parentCallback = {this.setEnteredKeyword.bind(this)} keywordDisabled = {this.state.keywordDisabled} resetFilter = {this.state.resetFilter}>
                          
                          </KeywordFilter>
                      </div>
                      <div className="two columns button_holder">
                      
                          <button
                            style={ {margin: '5px 2px'} }
                            className="submit usa-button-primary icon-search submit_button"
                            aria-label="Search CALC"
                           ></button>{' '}
                          <input onClick={this.handleResetClick}
                            className="reset usa-button usa-button-secondary reset_button"
                            type="reset"
                            value="Reset"
                          />
                      </div>
                    </div>
                  </div>
                  <div className="four columns">
                    <QueryType />
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
        <div className="row card secondary">
          <div className="columns nine">

            <div className="graph-block">
              {/* for converting the histogram into an img --> */}
              <canvas
                ref={(el) => { this.canvasEl = el; }}
                id={prefixId('graph') /* Selenium needs it. */}
                className="hidden"
                width="710"
                height="280"
              />

              <Description />

              <LoadingIndicator />

              <div className="graph">
                <div id={prefixId('price-histogram')}>
                  <Histogram ref={(el) => { this.histogram = el; }} />
                </div>
              </div>

              <div className="highlights-container">
                <Highlights />
                <ProposedPrice />
              </div>

              <div>
                <p className="info-text">
                  <b>Note: </b>
                  68% of the prices fall between the +1 and -1 Standard Deviation.
                </p>
              </div>  

              <div className="">
                <a
                  className="usa-button usa-button-primary"
                  id={prefixId('download-histogram') /* Selenium needs it. */}
                  href=""
                  onClick={this.handleDownloadClick}
                >
                  ⬇ Download graph
                </a>
                <ExportData />
                <p className="help-text">
                  The rates shown here are fully burdened, applicable
                  {' '}
                  worldwide, and representative of the current fiscal
                  {' '}
                  year. This data represents rates awarded at the master
                  {' '}
                  contract level.
                </p>
              </div>
            </div>
          </div>

          <div className="filter-container columns three">
            <div className="filter-block">
              <h5 className="filter-title">
Optional filters
              </h5>
              <LoadableOptionalFilters />
            </div>
          </div>
        </div>
        <section className="results">
          <div className="container">
            <div className="row">
              <div className="table-container">
                <ResultsTable search_keywords={this.state.searchkeyword} />
              </div>
            </div>
          </div>
        </section>
      </form>
    );
  }
}

App.propTypes = {
  api: PropTypes.object.isRequired,
  ratesInProgress: PropTypes.bool.isRequired,
  ratesError: PropTypes.string,
  resetState: PropTypes.func.isRequired,
  invalidateRates: PropTypes.func.isRequired,
  idPrefix: PropTypes.string,
};

App.defaultProps = {
  idPrefix: '',
  ratesError: null,
};

export default connect(
  state => ({
    ratesInProgress: state.rates.inProgress,
    ratesError: state.rates.error,
  }),
  { resetState, invalidateRates },
)(App);
