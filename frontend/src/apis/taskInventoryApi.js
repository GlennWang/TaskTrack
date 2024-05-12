// /src/apis/taskInventoryApi.js

import baseApi from './baseApi';

const taskInventoryApi = {
  getAllTasks: async () => {
    return baseApi('get', 'tasks/');
  },

  getTask: async (taskId) => {
    return baseApi('get', `tasks/${taskId}`);
  },

  addTask: async (taskData) => {
    return baseApi('post', 'tasks/', taskData);
  },

  updateTask: async (taskId, taskData) => {
    return baseApi('put', `tasks/${taskId}`, taskData);
  },

  deleteTask: async (taskId) => {
    return baseApi('delete', `tasks/${taskId}`);
  }
};

export default taskInventoryApi;

