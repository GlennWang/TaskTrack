<template>
    <div class="task-inventory">
      <h2>Task Inventory</h2>
      <ul class="tasks-list">
        <li v-for="task in tasks.results" :key="task.id" class="task-item">
          <div class="task-details">
            <div class="task-category">{{ task.category }}</div>
            <div class="task-name">{{ task.name }}</div>
            <div class="task-description">{{ task.description }}</div>
            <div class="task-priority">{{ task.priority }}</div>
            <div class="task-importance">{{ task.importance }}</div>
            <div class="task-deadline">{{ task.deadline }}</div>
          </div>
          <div class="kebab-menu">
            <button @click="toggleTaskOptions(task.id)">...</button>
            <div v-if="task.id === selectedTaskId" :class="{ 'task-options': true, 'active': showOptions }">
                <button @click="deleteTask(task.id)">Delete</button>
                <button @click="editTask(task)">Edit</button>
            </div>
          </div>
        </li>
      </ul>
      <div class="add-task-container">
        <button @click="showAddTaskDialog">Add Task</button>
        <button @click="pushSelectedTasks">Push Selected Tasks</button>
      </div>
      <div v-if="showAddTaskDialogFlag" class="add-task-dialog">
        <div class="dialog-content">
          <input type="text" v-model="newTask.category" placeholder="Category">
          <input type="text" v-model="newTask.name" placeholder="Name">
          <input type="text" v-model="newTask.description" placeholder="Description">
          <input type="text" v-model="newTask.priority" placeholder="Priority">
          <input type="text" v-model="newTask.importance" placeholder="Importance">
          <input type="text" v-model="newTask.deadline" placeholder="Deadline">
          <button @click="addTask">Add</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
import taskInventoryApi from '../apis/taskInventoryApi';

export default {
  data() {
    return {
      tasks: { results: [] },
      newTask: {
        category: '',
        name: '',
        description: '',
        priority: '',
        importance: '',
        deadline: ''
      },
      showAddTaskDialogFlag: false,
      selectedTaskId: null,
      showOptions: false
    };
  },
  async mounted() {
    await this.fetchTasks();
    document.addEventListener('click', this.closeOptionsOnOutsideClick);
  },
  beforeDestroy() {
    document.removeEventListener('click', this.closeOptionsOnOutsideClick);
  },
  methods: {
    async fetchTasks() {
      try {
        this.tasks = await taskInventoryApi.getAllTasks();
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    },
    async addTask() {
      try {
        await taskInventoryApi.addTask(this.newTask);
        this.newTask = {
          category: '',
          name: '',
          description: '',
          priority: '',
          importance: '',
          deadline: ''
        };
        this.showAddTaskDialogFlag = false;
        await this.fetchTasks();
      } catch (error) {
        console.error('Error adding task:', error);
      }
    },
    async deleteTask(taskId) {
      try {
        await taskInventoryApi.deleteTask(taskId);
        await this.fetchTasks();
      } catch (error) {
        console.error(`Error deleting task ${taskId}:`, error);
      }
    },
    async editTask(task) {
      // Implement edit task functionality here
      console.log('Edit task:', task);
    },
    showAddTaskDialog() {
      this.showAddTaskDialogFlag = true;
    },
    toggleTaskOptions(taskId) {
  if (this.selectedTaskId === taskId) {
    this.showOptions = !this.showOptions; // 切换显示状态
  } else {
    this.selectedTaskId = taskId;
    this.showOptions = true;
  }
},
    closeOptionsOnOutsideClick(event) {
      if (!event.target.closest('.kebab-menu')) {
        this.showOptions = false;
      }
    },
    pushSelectedTasks() {
      const selectedTasks = this.tasks.results.filter(task => task.selected);
      const selectedTaskNames = selectedTasks.map(task => task.name);
      this.$emit('tasks-selected', selectedTaskNames);
    }
  }
};
</script>
  
  <style scoped>
  .task-inventory {
    font-family: Arial, sans-serif;
    width: 100%;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .task-inventory h2 {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
  }
  
  .task-inventory .tasks-list {
    list-style-type: none;
    padding: 0;
    margin-bottom: 20px;
  }
  
  .task-inventory .task-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
  }
  
  .task-inventory .task-details {
    display: flex;
    flex-wrap: wrap;
    flex-grow: 1;
  }
  
  .task-inventory .task-category,
  .task-inventory .task-name,
  .task-inventory .task-description,
  .task-inventory .task-priority,
  .task-inventory .task-importance,
  .task-inventory .task-deadline {
    margin-right: 10px;
  }
  
  .task-inventory .kebab-menu {
    position: relative;
  }
  
  .task-inventory .kebab-menu button {
    cursor: pointer;
    background-color: transparent;
    border: none;
  }
  
  .task-inventory .kebab-menu button:hover {
    color: #333;
  }
  
  .task-inventory .kebab-menu .task-options {
  position: absolute;
  top: calc(100% + 5px); 
  right: 0;
  display: none;
  background-color: #f9f9f9;
  border: 1px solid #ccc;
  border-radius: 4px;
  z-index: 999; 
}

.task-inventory .kebab-menu .task-options.active {
  display: flex; /* 将菜单显示出来 */
  flex-direction: column;
}

.task-inventory .kebab-menu .task-options button {
  padding: 10px;
  cursor: pointer;
  width: 100%; 
  text-align: left; 
}

.task-inventory .kebab-menu .task-options button:hover {
  background-color: #e0e0e0;
}
  
  .add-task-container {
    display: flex;
    justify-content: space-between;
  }
  
  .add-task-dialog {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 20px;
    z-index: 999;
    width: 400px;
  }
  
  .add-task-dialog input {
    display: block;
    margin-bottom: 10px;
    width: calc(100% - 20px);
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .add-task-dialog button {
    padding: 10px 20px;
    color: #333;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s, border-color 0.3s;
  }
  
  .add-task-dialog button:hover {
    color: #fff;
    background-color: #333;
  }
  </style>
  