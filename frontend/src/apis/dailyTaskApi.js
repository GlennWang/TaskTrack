// /src/apis/dailyTaskApi.js

import baseApi from './baseApi';

const dailyTaskApi = {
  getAllTasks: async () => {
    return baseApi('get', 'daily_tasks/');
  },

  getTask: async (taskId) => {
    return baseApi('get', `daily_tasks/${taskId}`);
  },

  addTask: async (taskData) => {
    return baseApi('post', 'daily_tasks/', taskData);
  },

  updateTask: async (taskId, taskData) => {
    return baseApi('put', `daily_tasks/${taskId}`, taskData);
  },

  deleteTask: async (taskId) => {
    return baseApi('delete', `daily_tasks/${taskId}`);
  }
};

export default dailyTaskApi;
