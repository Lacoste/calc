// @ts-check


import xhr from 'xhr';
import * as qs from 'querystring';

export const API_BASE = '/api';
export const API_RATES_SCHEDULES = '/schedules';
export const API_PATH_RATES_CSV = '/rates/csv';
export const API_PATH_RATES = '/rates';
export const API_PATH_SEARCH = '/search';

/** 
 * @typedef {Object} ScheduleMetadata
 * @property {string} schedule - The schedule identifier
 * @property {string} sin - The SIN number (can be an empty string)
 * @property {string} full_name - The user-facing name for the schedule
 */

export default class API {
  constructor(basePath = API_BASE) {
    this.basePath = basePath;
  }
  
  /* eslint-disable */
  get({ uri, data }, callback) {
    let path;
    // @ts-ignore
    if(window.API_HOST) {
      // @ts-ignore
      path = window.API_HOST + uri;
    } {
      path = this.basePath + uri;
    }
    if (data) {
      path += `?${qs.stringify(data)}`;
    }
    return xhr(path, {
      json: true,
    }, (err, res) => {
      if (err) {
        callback(`Error: Internal XMLHttpRequest Error: ${err.toString()}`);
      } else if (res.statusCode >= 400) {
        callback(res.rawRequest.statusText);
      } else {
        callback(null, res.body);
      }
    });
  }

  /**
   * Get schedule metadata from the API.
   * 
   * @param {function(string|null, ScheduleMetadata[]?)} callback
   */
  getSchedules(callback) {
    this.get({ uri: API_RATES_SCHEDULES, data: null }, callback);
  }
}
