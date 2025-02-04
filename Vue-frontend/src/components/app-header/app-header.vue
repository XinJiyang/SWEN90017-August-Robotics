<template>
  <el-popover trigger="hover">
    <template #reference>
      <el-avatar
        :src="avatarUrl"
        :size="56"
        style="float: right; margin-top: 10px; margin-right: 20px"
      />
    </template>
    <el-row justify="center" style="text-align: center">
      <el-col style="margin-bottom: 10px;"
        ><h2>{{ loginStore.$state.userInfo.username }}</h2></el-col
      >
      <el-col style="margin-bottom: 10px; color: grey;"
        ><h3>{{ loginStore.$state.userInfo.role }}</h3></el-col
      >
      <el-col><el-button @click="handleExitClick" text size="large">Log Out</el-button></el-col>
    </el-row>
  </el-popover>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { localCache } from '@/utils/cache';
import avatarUrl from '@/assets/img/user_avatar.png';
import useLoginStore from '@/stores/login/login';

const router = useRouter();

const loginStore = useLoginStore();

const handleExitClick = () => {
  localCache.removeCache('token');
  localCache.removeCache('userInfo');
  router.push('/login');
  router.go(0);
};
</script>

<style lang="less" scoped>
.el-avatar {
  background-color: #ffffff;
  outline: none;
  cursor: pointer;
}
</style>
