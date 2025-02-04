<template>
  <div class="login">
    <el-container>
      <el-aside width="530px">
        <div class="login-panel-wrapper">
          <login-panel />
        </div>
        <img class="computer-img" src="@/assets/img/login-computer.svg" />
      </el-aside>
      <el-main>
        <img class="background-img" src="@/assets/img/login-background.svg" />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import LoginPanel from './components/login-panel.vue';
</script>

<style lang="less" scoped>
.login {
  height: 100%;
  .el-container {
    height: 100%;

    .el-aside {
      position: relative;
      height: 100%;

      .login-panel-wrapper {
        position: absolute;
        top: 140px;
        left: 50%;
        transform: translateX(-50%);
      }
      .computer-img {
        position: absolute;
        bottom: 0;
        width: 80%;

        @media (max-height: 859px) {
          display: none;
        }
      }
    }

    .el-main {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100%;
      padding: 0;
      border-left: #dcdfe6 4px solid;
      background-color: #639843;

      .background-img {
        height: 80%;
      }
    }
  }
}
</style>
