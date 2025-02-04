<template>
  <div class="login-panel">
    <div class="logo-wrapper">
      <img src="@/assets/img/ar_logo.svg" />
    </div>
    <h2 class="title">Welcome back!</h2>
    <el-form label-width="80px" :model="account" :rules="accountRules" ref="formRef">
      <el-form-item label-width="0" prop="username">
        <h5 class="label">USERNAME</h5>
        <el-input v-model="account.username" />
      </el-form-item>
      <el-form-item label-width="0" prop="password">
        <h5 class="label">PASSWORD</h5>
        <el-input type="password" v-model="account.password" show-password />
      </el-form-item>
    </el-form>
    <div class="rem-wrapper">
      <el-switch style="--el-switch-on-color: #639843" v-model="isRemPasswd" />
      <h4>Remember me</h4>
    </div>
    <el-button class="login-btn" size="large" color="#639843" @click="handleLoginClick"
      >LOGIN</el-button
    >
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch } from 'vue';
import type { FormRules, FormInstance } from 'element-plus';
import { ElMessage } from 'element-plus';
import useLoginStore from '@/stores/login/login';
import { localCache } from '@/utils/cache';

const account = reactive({
  username: localCache.getCache('username') ?? '',
  password: localCache.getCache('password') ?? ''
});

const formRef = ref<FormInstance>();
const accountRules: FormRules = {
  username: [
    { required: true, message: 'Username cannot be empty', trigger: 'blur' },
    {
      pattern: /^[a-z0-9]{3,20}$/,
      message: 'Must consist of 3 to 20 alphanumeric characters~',
      trigger: ['blur', 'change']
    }
  ],
  password: [
    { required: true, message: 'Password cannot be empty', trigger: 'blur' },
    {
      min: 3,
      max: 20,
      message: 'Length should be 3 to 20',
      trigger: ['blur', 'change']
    }
  ]
};

const isRemPasswd = ref(localCache.getCache('isRemPasswd') === 'true');
watch(isRemPasswd, (newValue) => {
  if (newValue === false) {
    localCache.removeCache('username');
    localCache.removeCache('password');
  }
  localCache.setCache('isRemPasswd', newValue + '');
});

const loginStore = useLoginStore();
const handleLoginClick = () => {
  formRef.value?.validate((valid) => {
    if (valid) {
      if (isRemPasswd.value) {
        localCache.setCache('username', account.username);
        localCache.setCache('password', account.password);
      }
      loginStore.userLoginAction(account);
    } else {
      ElMessage.error('Oops, Please pay attention to the format of username and password');
    }
  });
};
</script>

<style lang="less" scoped>
.login-panel {
  width: 300px;

  .title {
    margin-bottom: 30px;
  }

  .label {
    margin: 0 0 5px 0;
    letter-spacing: 0.1em;
    color: #97a0c3;
  }
  .logo-wrapper {
    width: 150px;
    margin-bottom: 25px;
    img {
      width: 100%;
    }
  }

  .rem-wrapper {
    display: flex;
    align-items: center;
    margin-bottom: 20px;

    h4 {
      margin-left: 5px;
      font-weight: 500;
    }
  }

  .login-btn {
    width: 100%;
    border-radius: 7px;
  }
  :deep(.el-input__wrapper.is-focus) {
    box-shadow: 0 0 0 1px #639843 inset;
  }
}
</style>
