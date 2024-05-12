<template>
  <div>
    
    <!-- <DailyTask @tasks-selected="handlePushSelectedTasks" /> -->

    <!-- <ToDoList :selected-tasks="selectedTasksFromDailyTask" /> -->

    <TaskInventory />
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

</style>
