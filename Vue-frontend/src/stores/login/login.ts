import type { IAccount, IUserInfo } from '@/types';
import type { AxiosError } from 'axios';
import { defineStore } from 'pinia';
import { ElMessage } from 'element-plus';
import { userLoginRequest } from '@/service/login/login';
import { localCache } from '@/utils/cache';
import router from '@/router';
import asyncRoutes from '@/router/asyncRoutes';
import { mapRoleToRoutes } from '@/utils/mapRoleToRoutes';
import jwtDecode from 'jwt-decode';

interface ILoginStore {
  token: string;
  userInfo: IUserInfo;
}

const useLoginStore = defineStore('login', {
  state: (): ILoginStore => ({
    token: '',
    userInfo: {
      username: '',
      email: '',
      role: ''
    }
  }),
  actions: {
    async userLoginAction(account: IAccount) {
      try {
        const loginResult = await userLoginRequest(account);

        // Decode the JWT token to get user information
        const decodedToken = jwtDecode(loginResult.access);

        //store userInfo
        this.token = loginResult.access;  // Using the access token here
        this.userInfo.username = decodedToken.username;
        this.userInfo.role = decodedToken.role;
        localCache.setCache('token', this.token);
        localCache.setCache('userInfo', this.userInfo);


        //role based access control
        const routes = mapRoleToRoutes(this.userInfo.role, asyncRoutes);
        routes.forEach((route) => {
          router.addRoute(route);
        });

        //to dashboard page
        router.push('/dashboard');

        window.location.reload();
      } catch (error) {
        if ((error as AxiosError).response?.status === 401) {
          ElMessage.error('No active account found with the given credentials');
        }
      }
    },

    loadLocalCacheAction() {
      const token = localCache.getCache('token');
      const userInfo = localCache.getCache('userInfo');
      if (token && userInfo) {
        this.token = token;
        this.userInfo = userInfo;
      }

      //role based access control
      const routes = mapRoleToRoutes(this.userInfo.role, asyncRoutes);
      routes.forEach((route) => {
        router.addRoute(route);
      });
    }
  }
});

export default useLoginStore;
