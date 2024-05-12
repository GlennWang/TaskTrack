// /src/apis/todoListApi.js

import baseApi from './baseApi';

const todoListApi = {
  getAllTasks: async () => {
    return baseApi('get', 'todo_lists/');
  },

  getTask: async (taskId) => {
    return baseApi('get', `todo_lists/${taskId}`);
  },

  addTask: async (taskData) => {
    return baseApi('post', 'todo_lists/', taskData);
  },

  updateTask: async (taskId, taskData) => {
    return baseApi('put', `todo_lists/${taskId}`, taskData);
  },

  deleteTask: async (taskId) => {
    return baseApi('delete', `todo_lists/${taskId}`);
  }
};

export default todoListApi;
