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

        <div class="task-action-buttons">
          <button @click="showAddTaskDialog">Add Task</button>
          <button @click="pushSelectedTasks">Push Selected Tasks</button>
        </div>
        <div v-if="showAddTaskDialogFlag" class="dialog">
          <div class="dialog-content">
            <input type="text" v-model="newTask.category" placeholder="Category">
            <input type="text" v-model="newTask.name" placeholder="Name">
            <input type="text" v-model="newTask.description" placeholder="Description">
            <select v-model="newTask.priority" class="select-priority">
              <option disabled selected value="">Priority</option>
              <option value="1">Critical</option>
              <option value="2">High</option>
              <option value="3">Medium</option>
              <option value="4">Low</option>
              <option value="5">Negligible</option>
            </select>
            <select v-model="newTask.importance" class="select-importance">
              <option disabled selected value="">Importance</option>
              <option value="1">Critical</option>
              <option value="2">High</option>
              <option value="3">Medium</option>
              <option value="4">Low</option>
              <option value="5">Negligible</option>
            </select>
            <input type="text" v-model="newTask.deadline" placeholder="Deadline">
            <button @click="addTask">Add</button>
            <button @click="cancelAddTask">Cancel</button>
          </div>
        </div>
        <div v-if="showEditTaskDialogFlag" class="dialog">
          <div class="dialog-content">
            <input type="text" v-model="editTaskData.category" placeholder="Category">
            <input type="text" v-model="editTaskData.name" placeholder="Name">
            <input type="text" v-model="editTaskData.description" placeholder="Description">
            <select v-model="editTaskData.priority" class="select-priority">
              <option disabled selected value="">Priority</option>
              <option value="1">Critical</option>
              <option value="2">High</option>
              <option value="3">Medium</option>
              <option value="4">Low</option>
              <option value="5">Negligible</option>
            </select>
            <select v-model="editTaskData.importance" class="select-importance">
              <option disabled selected value="">Importance</option>
              <option value="1">Critical</option>
              <option value="2">High</option>
              <option value="3">Medium</option>
              <option value="4">Low</option>
              <option value="5">Negligible</option>
            </select>
            <input type="text" v-model="editTaskData.deadline" placeholder="Deadline">
            <button @click="updateEditedTask">Update</button>
            <button @click="cancelEditTask">Cancel</button>
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
      selectedTasks: {},
      showEditTaskDialogFlag: false,
      editTaskData: {}
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
      this.editTaskData = { ...task };
      this.showEditTaskDialogFlag = true;
    },
    async updateEditedTask() {
      try {
        await taskInventoryApi.updateTask(this.editTaskData.id, this.editTaskData);
        await this.fetchTasks();
        this.showEditTaskDialogFlag = false;
        this.clearEditTaskData();
      } catch (error) {
        console.error('Error updating edited task:', error);
      }
    },
    cancelEditTask() {
      this.showEditTaskDialogFlag = false;
      this.clearEditTaskData();
    },
    clearEditTaskData() {
      this.editTaskData = {};
    },
    async saveTask(task) {
      // Implement save task functionality here
      console.log('Save task:', task);
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
    },
    showAddTaskDialog() {
      this.showAddTaskDialogFlag = true;
    },
    cancelAddTask() {
      this.showAddTaskDialogFlag = false;
      this.clearNewTaskData();
    },
    clearNewTaskData() {
      this.newTask = {
        category: '',
        name: '',
        description: '',
        priority: '',
        importance: '',
        deadline: ''
      };
    }
  }
};
</script>

<style scoped>
.task-inventory-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.task-inventory-container {
  width: 50vw;
  /* height: 100vh; */
  height: calc(100vh - 52px);
  overflow-y: auto;
}

.task-inventory {
  font-family: Arial, sans-serif;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 98%;
  height: 100%;
  box-sizing: border-box;
}

.task-inventory h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.task-inventory button {
  background-color: #00000000;
  padding: 10px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: color 0.3s, border-color 0.3s;
}

.task-inventory button:hover {
  color: #fff;
  background-color: #333;
}

.task-inventory button svg {
  width: 24px;
  height: 24px;
}

.task-inventory button path {
  fill: none;
  stroke-width: 2;
}

.task-inventory .delete-task,
.task-inventory .delete-task:hover {
  color: #f44336;
}

.task-inventory .edit-task,
.task-inventory .edit-task:hover {
  color: #007bff;
}

.task-inventory .save-task,
.task-inventory .save-task:hover {
  color: #4caf50;
}

.tasks-table-wrapper {
  position: relative;
  max-height: calc(100% - 120px);
  overflow-y: auto;
}

.tasks-table thead {
  position: sticky;
  top: 0;
  z-index: 999;
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

.task-action-buttons {
  margin-top: 5px;
  display: flex;
  justify-content: space-between;
}

.dialog {
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

.dialog input,
.dialog select {
  display: block;
  margin-bottom: 10px;
  width: calc(100% - 20px);
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.dialog select {
  width: 100%;
}

.task-action-buttons button,
.dialog-content button {
  margin: 0 10px;
  margin-bottom: 15px;
  padding: 10px 20px;
  border: 1px solid #ccc; /* Keep border */
}
</style>
