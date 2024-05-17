<template>
  <div class="todo-list-wrapper">
    <div class="todo-list" :style="{ width: focusWidth }">
      <h2>ToDo List</h2>
      <div class="add-task-container">
        <input type="text" v-model="newTask" placeholder="Enter task...">
        <button @click="addTask">+</button>
      </div>
      <ul class="tasks-list" :style="{ maxHeight: maxHeight }">
        <li v-for="task in tasks" :key="task.id" class="task-item">
          <div class="task-status">
            <div class="custom-checkbox" :class="{ 'custom-checkbox-checked': task.status }" @click="updateTaskStatus(task)"></div>
          </div>
          <div class="task-name-container">
            <span v-if="!task.editing" @click="startEditing(task)" :class="{ 'disabled': isEditing }">{{ task.name }}</span>
            <input v-else type="text" :id="'task-input-' + task.id" v-model="task.name" @blur="finishEditing(task)" @keyup.enter="finishEditing(task)">
          </div>
          <button class="delete-task" @click="deleteTask(task.id)" :disabled="isEditing"> <!-- Disable delete button while editing -->
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 6H21"></path>
              <path d="M8 6V4C8 2.897 8.897 2 10 2H14C15.103 2 16 2.897 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z"></path>
              <path d="M10 11V17"></path>
              <path d="M14 11V17"></path>
            </svg>
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>
  
<script>
import todoListApi from '../apis/todoListApi';

export default {
  props: {
    selectedTasks: {
      type: Array,
      default: () => []
    },
    maxHeight: {
      type: String,
      default: null
    },
    focusWidth: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      tasks: [],
      newTask: '',
      isEditing: false // Flag to indicate if editing is in progress
    };
  },
  async mounted() {
    await this.fetchTasks();
  },
  watch: {
    selectedTasks: {
      handler: 'addSelectedTasks',
      immediate: true // Call addSelectedTasks immediately on component mount
    }
  },
  methods: {
    async fetchTasks() {
      try {
        const response = await todoListApi.getAllTasks();
        this.tasks = response.results.map(task => ({ ...task, editing: false }));
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    },
    async addTask() {
      try {
        if (this.newTask.trim() !== '') {
          const newTask = await todoListApi.addTask({ name: this.newTask.trim() });
          this.tasks.push({ ...newTask, editing: false });
          this.newTask = '';
          await this.fetchTasks(); // Fetch tasks after adding a new task
        }
      } catch (error) {
        console.error('Error adding task:', error);
      }
    },
    async deleteTask(taskId) {
      try {
        await todoListApi.deleteTask(taskId);
        this.tasks = this.tasks.filter(task => task.id !== taskId);
        await this.fetchTasks(); // Fetch tasks after deleting a task
      } catch (error) {
        console.error(`Error deleting task ${taskId}:`, error);
      }
    },
    async updateTaskStatus(task) {
      try {
        task.status = !task.status; // Toggle task status
        await todoListApi.updateTask(task.id, { status: task.status });
        await this.fetchTasks(); // Fetch tasks after updating task status
      } catch (error) {
        console.error(`Error updating task ${task.id} status:`, error);
      }
    },
    startEditing(task) {
      if (!this.isEditing) { // Check if editing is not already in progress
        this.isEditing = true; // Set editing flag
        this.tasks.forEach(t => {
          t.editing = (t.id === task.id); // Set editing flag for the clicked task
        });
        this.$nextTick(() => {
          const input = document.getElementById(`task-input-${task.id}`);
          if (input) {
            input.focus();
          }
        });
      }
    },
    async finishEditing(task) {
      try {
        await todoListApi.updateTask(task.id, { name: task.name });
        task.editing = false;
        this.isEditing = false; // Reset editing flag when editing is finished
        await this.fetchTasks(); // Fetch tasks after finishing editing
      } catch (error) {
        console.error(`Error updating task ${task.id} name:`, error);
      }
    },
    async addSelectedTasks() {
      try {
        for (const selectedTask of this.selectedTasks) {
          const newTask = await todoListApi.addTask({ name: selectedTask });
          this.tasks.push({ ...newTask, editing: false });
        }
        await this.fetchTasks(); // Fetch tasks after adding selected tasks
      } catch (error) {
        console.error('Error adding selected tasks:', error);
      }
    }
  }
};
</script>

<style scoped>
.todo-list-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.todo-list {
  font-family: Arial, sans-serif;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 98%;
  max-height: 100%;
  /* overflow-y: auto; */
  box-sizing: border-box;
}

.todo-list h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.todo-list .add-task-container {
  margin-bottom: 20px;
  display: flex;
}

.todo-list input[type="text"] {
  flex-grow: 1;
  padding: 10px;
  margin-right: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.todo-list button {
  padding: 10px 20px;
  color: #333;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  transition: color 0.3s, border-color 0.3s;
}

.todo-list button:hover {
  color: #fff;
  background-color: #333;
}

.todo-list ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  max-height: calc(50vh - 205px);
  /* max-height: calc(100vh - 228px); */
  overflow-y: auto;
}

.todo-list .task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.todo-list .task-status {
  margin-right: 10px;
  cursor: pointer;
}

.todo-list .task-name-container {
  flex-grow: 1;
  overflow: hidden;
  text-align: left;
}

.todo-list .task-name-container input[type="text"] {
  width: 100%;
}

.todo-list .delete-task {
  cursor: pointer;
  color: #f44336;
  background-color: transparent;
  border: none;
  transition: color 0.3s;
}

.todo-list .delete-task svg {
  width: 24px;
  height: 24px;
}

.todo-list .delete-task:hover {
  color: #d32f2f;
}

.todo-list .disabled {
  pointer-events: none;
  opacity: 0.5;
}
</style>