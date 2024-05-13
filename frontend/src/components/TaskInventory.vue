<template>
  <div class="task-inventory-wrapper">
    <div class="task-inventory-container">
      <div class="task-inventory">
        <h2>Task Inventory</h2>
        <div class="tasks-table-wrapper">
          <table class="tasks-table">
          <thead>
            <tr>
              <th style="width: fit-content;">
                <div class="custom-checkbox custom-checkbox-checked"></div>
              </th>
              <th style="width: fit-content;">Category</th>
              <th style="width: 15%;">Name</th>
              <th style="width: 20%;">Description</th>
              <th style="width: fit-content;">Importance</th>
              <th style="width: fit-content;">Deadline</th>
              <th style="width: 25%;">Options</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="task in tasks.results" :key="task.id" :style="{ backgroundColor: getPriorityColor(task.priority) }">
              <td class="center-cell">
                <div @click="updateTaskStatus(task)">
                  <div class="custom-checkbox" :class="{ 'custom-checkbox-checked': selectedTasks[task.id] }"></div>
                </div>
              </td>
              <td>{{ task.category }}</td>
              <td>{{ task.name }}</td>
              <td>{{ task.description }}</td>
              <td>{{ getImportanceStars(task.importance) }}</td>
              <td>{{ task.deadline }}</td>
              <td class="center-cell">
                <button class="delete-task" @click="deleteTask(task.id)">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2 delete-icon">
                    <path d="M3 6H21"></path>
                    <path d="M8 6V4C8 2.897 8.897 2 10 2H14C15.103 2 16 2.897 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z"></path>
                    <path d="M10 11V17"></path>
                    <path d="M14 11V17"></path>
                  </svg>
                </button>
                <button class="edit-task" @click="editTask(task)">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit edit-icon">
                    <path d="M20 5.7l-1.4-1.4c-.4-.4-1-.4-1.4 0L3 17V21h4l11.7-11.7c.4-.4.4-1 0-1.4l-1.4-1.4z"></path>
                  </svg>
                </button>
                <button class="save-task" @click="saveTask(task)">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-save">
                    <path d="M5 3h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2z"></path>
                    <path d="M17 12l-5 5-5-5M12 17V7"></path>
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        </div>

        <div class="add-task-container">
          <button class="add-task" @click="showAddTaskDialog">Add Task</button>
          <button class="push-tasks" @click="pushSelectedTasks">Push Selected Tasks</button>
        </div>
        <div v-if="showAddTaskDialogFlag" class="add-task-dialog">
          <div class="dialog-content">
            <input type="text" v-model="newTask.category" placeholder="Category">
            <input type="text" v-model="newTask.name" placeholder="Name">
            <input type="text" v-model="newTask.description" placeholder="Description">
            <input type="text" v-model="newTask.priority" placeholder="Priority">
            <input type="text" v-model="newTask.importance" placeholder="importance">
            <input type="text" v-model="newTask.deadline" placeholder="Deadline">
            <button class="add-task" @click="addTask">Add</button>
          </div>
        </div>
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
      selectedTasks: {}
    };
  },
  async mounted() {
    await this.fetchTasks();
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
    async saveTask(task) {
      // Implement save task functionality here
      console.log('Save task:', task);
    },
    showAddTaskDialog() {
      this.showAddTaskDialogFlag = true;
    },
    async pushSelectedTasks() {
        try {
            const selectedTaskNames = [];
            for (const taskId of Object.keys(this.selectedTasks)) {
            if (this.selectedTasks[taskId]) {
                const task = this.tasks.results.find(task => task.id === parseInt(taskId));
                if (task) {
                selectedTaskNames.push(task.name);
                this.selectedTasks[taskId] = false;
                }
            }
            }
            console.log(selectedTaskNames);
            this.$emit('tasks-selected', selectedTaskNames);
        } catch (error) {
            console.error('Error pushing tasks:', error);
        }
      },
    async updateTaskStatus(task) {
      try {
          this.selectedTasks[task.id] = !this.selectedTasks[task.id];
      } catch (error) {
        console.error(`Error updating task ${task.id} status:`, error);
      }
    },
    getPriorityColor(priority) {
      switch (priority) {
        case 1:
          return '#ffd6d6'; // Light Red
        case 2:
          return '#ffe8cc'; // Light Orange
        case 3:
          return '#fffff0'; // Light Yellow
        case 4:
          return '#e5ffe5'; // Light Green
        case 5:
          return '#e5ecff'; // Light Blue
        default:
          return '#fff'; // White (default)
      }
    },
    getImportanceStars(importance) {
      switch (importance) {
        case 1:
          return '★★★★★';
        case 2:
          return '★★★★';
        case 3:
          return '★★★';
        case 4:
          return '★★';
        case 5:
          return '★';
        default:
          return '';
      }
    }
  }
};
</script>

<style scoped>
.task-inventory-wrapper {
  width: 100%;
  height: 100%;
  overflow: auto;
}

.task-inventory-container {
  width: 50vw;
  height: 100vh;
  overflow-y: auto;
}

.task-inventory {
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
  margin: 0 auto;
  padding: 20px;
  height: calc(100% - 40px);
}

.task-inventory h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.tasks-table-wrapper {
  position: relative; /* 讓父容器成為相對定位 */
  max-height: calc(100% - 120px);
  overflow-y: auto;
}

.tasks-table thead {
  position: sticky;
  top: 0;
}


.tasks-table {
  width: 100%;
  border-collapse: collapse;
}

.tasks-table th,
.tasks-table td {
  padding: 6px;
  border: 1px solid #ccc;
}

.tasks-table th {
  background-color: #f2f2f2;
}

.tasks-table td {
  text-align: left;
}

.tasks-table .center-cell {
  text-align: center;
}

.add-task-container {
  margin-top: 5px;
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

.task-inventory .delete-task,
.task-inventory .edit-task,
.task-inventory .save-task {
  background-color: #00000000;
  padding: 10px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: color 0.3s, border-color 0.3s;
}

.task-inventory .delete-task svg,
.task-inventory .edit-task svg,
.task-inventory .save-task svg {
  width: 24px;
  height: 24px;
}

.task-inventory .delete-task path,
.task-inventory .edit-task path,
.task-inventory .save-task path {
  fill: none;
  stroke-width: 2;
}

.task-inventory .delete-task:hover,
.task-inventory .edit-task:hover,
.task-inventory .save-task:hover {
  background-color: #333;
}

.task-inventory .delete-task {
  color: #f44336;
}

.task-inventory .edit-task {
  color: #007bff;
}

.task-inventory .save-task {
  color: #4caf50;
}

.task-inventory .add-task,
.task-inventory .push-tasks {
  margin-bottom: 15px;
  padding: 10px 20px;
  color: #333;
  border: 1px solid #ccc; /* Keep border */
  border-radius: 4px;
  cursor: pointer;
  transition: color 0.3s, border-color 0.3s;
}

.task-inventory .add-task:hover,
.task-inventory .push-tasks:hover {
  color: #fff;
  background-color: #333;
}

::-webkit-scrollbar {
  width: 12px;
}

::-webkit-scrollbar-track {
  background-color: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 6px;
  border: 3px solid #f1f1f1;
}

::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}

/* Custom checkbox styles */
.custom-checkbox {
  display: inline-block;
  width: 22px;
  height: 22px;
  border: 2px solid rgb(223, 223, 223);
  background-color: rgb(223, 223, 223);
  border-radius: 50%;
}

.custom-checkbox:hover {
  opacity: 0.6;
}

.custom-checkbox::after {
  content: "";
  display: block;
  margin-left: 7px;
  margin-top: 3px;
  width: 5px;
  height: 11px;
  border-style: solid;
  border-color: rgb(255, 255, 255);
  border-image: initial;
  border-width: 0px 3px 3px 0px;
  transform: rotate(45deg);
}

.custom-checkbox-checked {
  border: 2px solid #2ecc71; 
  background-color: #2ecc71;
}
</style>
