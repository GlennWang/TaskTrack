<template>
  <div class="daily-tasks-wrapper">
    <div class="daily-tasks">
      <h2>Daily Tasks</h2>
      <div class="add-task-container">
        <input type="text" v-model="newTask" placeholder="Enter task...">
        <button @click="addTask">+</button>
      </div>
      <ul class="tasks-list">
        <li v-for="task in tasks.results" :key="task.id" :class="{ 'editing': editingId === task.id }" class="task-item">
          <div class="task-status" @click="updateTaskStatus(task)">
            <div class="custom-checkbox" :class="{ 'custom-checkbox-checked': selectedTasks[task.id] }"></div>
          </div>
          <div class="task-name-container">
            <span v-if="!editingId || editingId !== task.id" @click="startEditing(task)" :class="{ 'disabled': isEditing }">{{ task.name }}</span>
            <input v-else type="text" :id="'task-input-' + task.id" v-model="task.name" @blur="finishEditing(task)" @keyup.enter="finishEditing(task)">
          </div>
          <button class="delete-task" @click="deleteTask(task.id)" :disabled="isEditing">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-trash-2">
              <path d="M3 6H21"></path>
              <path d="M8 6V4C8 2.897 8.897 2 10 2H14C15.103 2 16 2.897 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z"></path>
              <path d="M10 11V17"></path>
              <path d="M14 11V17"></path>
            </svg>
          </button>
        </li>
      </ul>
      <button @click="pushTasks" :disabled="isEditing">Push Selected Tasks</button>
    </div>
  </div>
</template>
  
<script>
  import dailyTaskApi from '../apis/dailyTaskApi';
  
  export default {
    data() {
      return {
        tasks: { results: [] },
        newTask: '',
        selectedTasks: {},
        editingId: null,
        isEditing: false
      };
    },
    async mounted() {
      await this.fetchTasks();
    },
    methods: {
      async fetchTasks() {
        try {
          this.tasks = await dailyTaskApi.getAllTasks();
        } catch (error) {
          console.error('Error fetching tasks:', error);
        }
      },
      async addTask() {
        try {
          if (this.newTask.trim() !== '') {
            const newTask = await dailyTaskApi.addTask({ name: this.newTask.trim() });
            this.tasks.results.push(newTask);
            this.newTask = '';
            await this.fetchTasks();
          }
        } catch (error) {
          console.error('Error adding task:', error);
        }
      },
      async deleteTask(taskId) {
        try {
          await dailyTaskApi.deleteTask(taskId);
          const index = this.tasks.results.findIndex(task => task.id === taskId);
          if (index !== -1) {
            this.tasks.results.splice(index, 1);
          }
        } catch (error) {
          console.error(`Error deleting task ${taskId}:`, error);
        }
      },
      startEditing(task) {
        this.editingId = task.id;
        this.isEditing = true;
        this.$nextTick(() => {
          const input = document.getElementById(`task-input-${task.id}`);
          if (input) {
            input.focus();
          }
        });
      },
      async finishEditing(task) {
        try {
          await dailyTaskApi.updateTask(task.id, { name: task.name });
          this.editingId = null;
          this.isEditing = false;
          await this.fetchTasks();
        } catch (error) {
          console.error(`Error updating task ${task.id}:`, error);
        }
      },
      async pushTasks() {
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
            // console.log(selectedTaskNames);
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
    }
  };
</script>
  
<style scoped>
.daily-tasks-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.daily-tasks {
  font-family: Arial, sans-serif;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 98%;
  max-height: 98%;
  overflow-y: auto;
  box-sizing: border-box;
}

.daily-tasks h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.daily-tasks .add-task-container {
  margin-bottom: 20px;
  display: flex;
}

.daily-tasks input[type="text"] {
  flex-grow: 1;
  padding: 10px;
  margin-right: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.daily-tasks button {
  padding: 10px 20px;
  color: #333;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  transition: color 0.3s, border-color 0.3s;
}

.daily-tasks button:hover {
  color: #fff;
  background-color: #333;
}

.daily-tasks ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  max-height: calc(50vh - 245px); 
  overflow-y: auto;
}

.daily-tasks .task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.daily-tasks .task-status {
  margin-right: 10px;
  cursor: pointer;
}

.daily-tasks .task-name-container {
  flex-grow: 1;
  overflow: hidden;
  text-align: left;
}

.daily-tasks .task-name-container input[type="text"] {
  width: 100%;
}

.daily-tasks .delete-task {
  cursor: pointer;
  color: #f44336;
  background-color: transparent;
  border: none;
  transition: color 0.3s;
}

.daily-tasks .delete-task svg {
  width: 24px;
  height: 24px;
}

.daily-tasks .delete-task:hover {
  color: #d32f2f;
}

.daily-tasks .disabled {
  pointer-events: none;
  opacity: 0.5;
}
</style>