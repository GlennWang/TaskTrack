// vue/src/apis/baseApi.js

import axios from 'axios';
import { host } from '../config/config';

const baseApi = async (method, endpoint, data = null) => {
  try {
    let response;
    if (method === 'get' || method === 'delete') {
      response = await axios[method](`${host}/${endpoint}`);
    } else {
      response = await axios[method](`${host}/${endpoint}`, data);
    }
    return response.data;
  } catch (error) {
    console.error(`Error ${method}ing data from ${endpoint}:`, error);
    throw error;
  }
};

export default baseApi;
