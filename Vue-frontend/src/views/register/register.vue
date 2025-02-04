<template>
    <div>
        <form>
            <input v-model="account.username" type="text" placeholder="username">
            <br>
            <input v-model="account.password" type="password" placeholder="password">
            <br>
            <select v-model="account.privilege">
                <option value="admin">admin</option>
                <option value="operator">operator</option>
                <option value="viewer">viewer</option>
            </select>
            <br>
            <button @click="handleRegister">register</button>
        </form>
    </div>
</template>

<script setup lang="ts">
import router from '@/router';
import { userRegisterRequest } from '@/service/login/login';
import type { AxiosError } from 'axios';
import { ElMessage } from 'element-plus';
import { reactive } from 'vue';

const account = reactive({
    username: '',
    password: '',
    privilege: 'admin'
})

async function handleRegister() {

    try {
        await userRegisterRequest(account);

        ElMessage.info('Register user successfully.');

        //to login page
        router.push('/login');
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          ElMessage.error('Fail to register.');
        }
      }
}
</script>

<style scoped>
form input, form select, form button {
    border: 1px solid black;
}
</style>