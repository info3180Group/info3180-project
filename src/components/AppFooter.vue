<template>
      <footer class="mt-5">
          <div class="container">
              <p>Copyright &copy {{ year }} Flask Inc.</p>
          </div>
      </footer>
</template>

<script setup>
import { ref } from "vue";

const year = (new Date).getFullYear();
</script>

<style scoped>
footer {
  background-color: #f8f9fa;
  padding: 20px 0;
  text-align: center;
  font-size: 14px;
  color: #6c757d;
  border-top: 1px solid #dee2e6;
  position: relative;
  bottom: 0;
  width: 100%;
}

footer .container {
  max-width: 960px;
  margin: 0 auto;
}
</style>
