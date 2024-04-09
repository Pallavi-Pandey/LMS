<template>
  <navbar />
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <div>
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navbar from "./components/navbar.vue";
export default {
  name: "App",
  components: {
    navbar,
  },
};
</script>