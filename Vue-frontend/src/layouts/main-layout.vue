<template>
  <div class="main-layout">
    <el-container>
      <el-aside width="165px">
        <app-sidenav />
      </el-aside>
      <el-container>
        <el-header height="70px">
          <app-header />
        </el-header>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="less" scoped>
.main-layout {
  height: 100%;
  .el-container {
    height: 100%;

    .el-aside {
      position: relative;
    }

    .el-main {
      padding-top: 10px;
    }
  }

  .main-wrapper {
    background-color: #f6f6f7;
    border-radius: 20px;
  }
}
</style>
