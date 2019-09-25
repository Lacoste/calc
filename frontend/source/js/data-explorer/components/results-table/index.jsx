import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { setSort } from '../../actions';
import createSortableColumn from './sortable-column';
import * as ExcludedColumn from './excluded-column';
import * as LaborCategoryColumn from './labor-category-column';
import * as EducationColumn from './education-column';
import * as KeywordsColumn from './keywords-column';
import * as CertificationsColumn from './certifications-columns';
import * as ExperienceColumn from './experience-column';
import * as PriceColumn from './price-column';
import * as VendorColumn from './vendor';

const COLUMNS = [
  ExcludedColumn,
  LaborCategoryColumn,
  PriceColumn,
  EducationColumn,
  ExperienceColumn,
  VendorColumn,
  KeywordsColumn,
  CertificationsColumn,
  createSortableColumn({
    key: 'schedule',
    title: 'Contract vehicle',
  }),
];

const { priceForContractYear } = PriceColumn;

export class ResultsTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      search_keywords: ""
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ search_keywords: nextProps.search_keywords }, () => {
      const searchLength = (this.state.search_keywords).length;
      if (searchLength > 2) {
        this.setState({ search_filter_need: true });
      } else {
        this.setState({ search_filter_need: false },
          () => {
            this.sendBackData(0);
          });
      }
    });
  }

  sendBackData(data) {
    this.props.countBackToParent(data);
  }

  analyzeOverallData(overall, searchArr) {
    let a = 0;
    let b = 0;
    const countArr = [];
    let currentKey = "";
    let currentCer = "";

    for (a = 0; a < overall.length; a++) {
      currentKey = overall[a].keywords;
      currentCer = overall[a].certifications;
      for (b = 0; b < searchArr.length; b++) {
        if (searchArr[b] !== "" && (currentKey || currentCer)) {
          if (
            (currentKey 
                && (currentKey.toLowerCase()).indexOf(searchArr[b].toLowerCase()) !== -1) 
                  || (currentCer 
                && (currentCer.toLowerCase()).indexOf(searchArr[b].toLowerCase()) !== -1)
          ) {
            if (countArr.indexOf(a) === -1) {
              countArr.push(a);
            }
          }
        }
      }
      this.sendBackData(countArr.length);
    }
  }


  checkKeyOrCertiExist(dataKeyword, dataCertificate, index, overall) {
    const searchStr = this.state.search_keywords;
    const searchArr = searchStr.split(',');
    let noMatchFound = true;
    let i = 0;
    for (i = 0; i < searchArr.length; i++) {
      if (searchArr[i] !== "" 
          && ( 
            (dataKeyword  
                && (dataKeyword.toLowerCase()).indexOf(searchArr[i].toLowerCase()) !== -1) 
                  || (dataCertificate 
                && (dataCertificate.toLowerCase()).indexOf(searchArr[i].toLowerCase()) !== -1) 
          )) {
        noMatchFound = false;
      }
    }

    if (overall.length === index + 1) { // last loop
      this.analyzeOverallData(overall, searchArr);
    }
    return noMatchFound;
  }

  renderBodyRows() {
    return this.props.results
      .filter(r => !!priceForContractYear(this.props.contractYear, r))
      .map((result, index) => (
        <tr 
          key={result.id} 
          className={
            (
              (  
                (!(result.keywords) && !(result.certifications))
                || this.checkKeyOrCertiExist(result.keywords, result.certifications, 
                  index, this.props.results)
              )
              && this.state.search_filter_need ? 'hidden' : ''
            )
        }
        >
          {COLUMNS.map((col) => {
            const cellKey = `${result.id}-${col.DataCell.cellKey}`;
            return (
              <col.DataCell key={cellKey} sort={this.props.sort} result={result} />
            );
          })
      }
        </tr>
      ));
  }

  render() {
    const id = `${this.props.idPrefix}results-table`;
    const idHref = `#${id}`;

    return (
      <table id={id} className="results has-data sortable hoverable">
        <thead>
          <tr>
            {COLUMNS.map(col => (
              <col.HeaderCell
                key={`header-${col.DataCell.cellKey}`}
                setSort={this.props.setSort}
                sort={this.props.sort}
              />
            ))}
          </tr>
        </thead>
        <tbody id="results_table_body">
          {this.renderBodyRows()}
        </tbody>
        {/* data-totalrow = {this.updateVisibleRowCount(this.state.search_keywords)} */}
        <tfoot>
          <tr>
            <td colSpan={COLUMNS.length} className="results-table_return-link">
              <a href={idHref}>
Return to the top
              </a>
            </td>
          </tr>
        </tfoot>
      </table> 
    );
  }
}

ResultsTable.propTypes = {
  sort: PropTypes.object.isRequired,
  setSort: PropTypes.func.isRequired,
  results: PropTypes.array.isRequired,
  contractYear: PropTypes.string.isRequired,
  idPrefix: PropTypes.string,
  search_keywords: PropTypes.string.isRequired,
  countBackToParent: PropTypes.any
};

ResultsTable.defaultProps = {
  idPrefix: '',
  countBackToParent: ''
};

function mapStateToProps(state) {
  return {
    sort: state.sort,
    results: state.rates.data.results,
    contractYear: state['contract-year'],
  };
}

const mapDispatchToProps = { setSort };

export default connect(mapStateToProps, mapDispatchToProps)(ResultsTable);
