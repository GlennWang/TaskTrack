<template>
  <div class="container">
    <nav class="navbar">
      <button @click="switchToComprehensiveMode">Comprehensive Mode</button>
      <button @click="switchToCoreMode">Core Mode</button>
      <button @click="switchToDailyMode">Daily Mode</button>
      <button @click="switchToFocusMode">Focus Mode</button>
    </nav>

    <div v-if="mode !== 'daily' && mode !== 'focus'" class="content">
      <div class="TaskInventory-container">
        <TaskInventory @tasks-selected="handlePushSelectedTasks"/>
      </div>
      <div class="main-content">
        <div v-if="mode !== 'core'" class="DailyTask-container">
          <DailyTask @tasks-selected="handlePushSelectedTasks" />
        </div>
        <div class="ToDoList-container">
          <ToDoList :selected-tasks="selectedTasksFromDailyTask" :maxHeight="ToDoListulmaxHeight" :focusWidth="ToDoListFocusWidth"/>
        </div>
      </div>
    </div>

    <!-- 新的布局 -->
    <div v-if="mode === 'daily' || mode === 'focus'" class="new-layout">
      <div v-if="mode === 'daily'" class="DailyTask-full">
        <DailyTask @tasks-selected="handlePushSelectedTasks" :maxHeight="DailyTaskulmaxHeight"/>
      </div>
      <div class="ToDoList-full">
        <ToDoList :selected-tasks="selectedTasksFromDailyTask" :maxHeight="ToDoListulmaxHeight" :focusWidth="ToDoListFocusWidth"/>
      </div>
    </div>
  </div>
</template>


<script>
import TaskInventory from './components/TaskInventory.vue';
import DailyTask from './components/DailyTask.vue';
import ToDoList from './components/ToDoList.vue';

export default {
  components: {
    TaskInventory,
    DailyTask,
    ToDoList
  },
  data() {
    return {
      selectedTasksFromDailyTask: [],
      mode: 'comprehensive',
      ToDoListulmaxHeight: null,
      ToDoListFocusWidth: '98%',
      DailyTaskulmaxHeight: null
    };
  },
  methods: {
    switchToComprehensiveMode() {
      this.mode = 'comprehensive';
      this.ToDoListulmaxHeight = null;
      this.ToDoListFocusWidth = '98%';
      this.DailyTaskulmaxHeight = null;
      this.clearSelectedTasks();
    },
    switchToCoreMode() {
      this.mode = 'core';
      this.ToDoListulmaxHeight = 'calc(100vh - 228px)';
      this.ToDoListFocusWidth = '98%';
      this.DailyTaskulmaxHeight = null;
      this.clearSelectedTasks();
    },
    switchToDailyMode() {
      this.mode = 'daily';
      // this.ToDoListulmaxHeight = 'calc(74vh - 70px)';
      // this.DailyTaskulmaxHeight = 'calc(70vh - 77px)';
      this.ToDoListulmaxHeight = 'calc(100vh - 228px)';
      this.ToDoListFocusWidth = '98%';
      this.DailyTaskulmaxHeight = 'calc(100vh - 269px)';
      // this.ToDoListulmaxHeight = null;
      // this.DailyTaskulmaxHeight = null;
      this.clearSelectedTasks();
    },
    switchToFocusMode() {
      this.mode = 'focus';
      this.ToDoListulmaxHeight = 'calc(100vh - 228px)';
      this.ToDoListFocusWidth = '60vw';
      this.DailyTaskulmaxHeight = null;
      this.clearSelectedTasks();
    },
    handlePushSelectedTasks(selectedTasks) {
      this.selectedTasksFromDailyTask = selectedTasks;
    },
    clearSelectedTasks() {
      this.selectedTasksFromDailyTask = [];
    }
  }
};
</script>


<style scoped>
.container {
  display: flex;
  flex-direction: column;
  /* height: 100%; */
  height: 100vh;
  width: 100vw;
  background-color: #e0e0e0;
}

.navbar {
  background-color:aliceblue;
  padding: 5px;
}

.navbar button {
  background-color: #f0f0f0;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  transition: color 0.3s, border-color 0.3s;
  margin-right: 10px;
}

.navbar button:hover {
  color: #fff;
  background-color: #333;
}

.content {
  display: flex;
  flex: 1;
}

.main-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  /* width: 50vw; */
}

.TaskInventory-container {
  order: 0;
  background-color: #e0e0e0;
  box-sizing: border-box;
}

.DailyTask-container {
  order: 2;
  background-color: #e0e0e0;
  box-sizing: border-box;
}

.ToDoList-container {
  order: 3;
  background-color: #e0e0e0;
  box-sizing: border-box;
}

.new-layout {
  display: flex;
  /* height: 100%; */
}

.DailyTask-full {
  flex: 1;
  background-color: #e0e0e0;
  box-sizing: border-box;
}

.ToDoList-full {
  flex: 1;
  background-color: #e0e0e0;
  box-sizing: border-box;
}
</style>