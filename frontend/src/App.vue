<template>
  <div>
    <!-- 左侧固定的 TaskInventory 组件容器 -->
    <div class="task-inventory-container">
      <!-- TaskInventory 组件 -->
      <TaskInventory @tasks-selected="handlePushSelectedTasks"/>
    </div>
    

    <div class="DailyTask-and-ToDoList-container">
      <DailyTask @tasks-selected="handlePushSelectedTasks" />
      <ToDoList :selected-tasks="selectedTasksFromDailyTask" />
    </div>
  </div>
</template>

<script>
import TaskInventory from './components/TaskInventory.vue'
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
      selectedTasksFromDailyTask: []
    };
  },
  methods: {
    handlePushSelectedTasks(selectedTasks) {
      this.selectedTasksFromDailyTask = selectedTasks;
    }
  }
};
</script>

<style scoped>
.task-inventory-container {
  position: fixed;
  top: 0;
  left: 0;
}

.DailyTask-and-ToDoList-container {
  position: fixed;
  top: 0;
  right: 400px;
}
</style>
