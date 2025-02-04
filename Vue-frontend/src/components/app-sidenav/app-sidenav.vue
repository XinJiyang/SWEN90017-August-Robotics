<template>
  <div class="app-sidenav">
    <div class="logo-wrapper">
      <img class="logo" src="@/assets/img/ar_logo_02.jpg" />
    </div>
    <div class="menu">
      <el-menu :default-active="defaultActive">
        <template v-for="(route, index) in routes" :key="index">
          <el-menu-item
            v-show="route.meta.icon"
            :index="index + ''"
            @click="handleItemClick(route)"
          >
            <el-icon size="46">
              <component :is="route.meta.icon"></component>
            </el-icon>
          </el-menu-item>
        </template>
      </el-menu>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRouter, useRoute, type RouteRecordNormalized } from 'vue-router';

//get the all user routes
const router = useRouter();
const routes = router.getRoutes();

const curRoute = useRoute();
const defaultActive = computed(() => {
  let index = -1;
  for (let i = 1; i < routes.length; i++) {
    if (routes[i].path === curRoute.path) {
      index = i;
      break;
    }
  }
  return index + '';
});

const handleItemClick = (route: RouteRecordNormalized) => {
  router.push(route.path);
};
</script>

<style lang="less" scoped>
.app-sidenav {
  position: absolute;
  top: 10px;
  bottom: 10px;
  width: 160px;
  margin-left: 5px;
  border-radius: 25px;
  background-color: #639843;

  .logo-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 128px;
    height: 117px;
    margin: 35px auto 0;
    border-radius: 20px;
    background-color: #ffffff;
    user-select: none;

    .logo {
      width: 87px;
      height: 87px;
    }
  }

  .menu {
    margin-top: 50px;
    padding: 0 15px;

    .el-menu {
      border-right: none;
      user-select: none;
      background-color: #639843;

      .el-menu-item {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        width: 128px;
        height: 100px;
        color: #ffffff;
        border-radius: 15px;

        &:hover {
          background-color: rgba(255, 255, 255, 0.3);

          &::before {
            opacity: 1;
            transform: scaleY(1);
          }
        }
        &::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(255, 255, 255, 0.3);
          border-radius: 15px;
          opacity: 0;
          transform: scaleY(0);
          transition: opacity 0.3s, transform 0.3s;
        }
      }
      .el-menu-item.is-active {
        background-color: rgba(255, 255, 255, 0.3);
      }
    }
  }
}
</style>
