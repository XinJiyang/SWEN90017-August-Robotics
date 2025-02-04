import { ElMessageBox } from 'element-plus';
import { BASE_URL, TIME_OUT } from './config';
import Request from './request';
import { localCache } from '@/utils/cache';
import router from '@/router';

const request = new Request({
  baseURL: BASE_URL,
  timeout: TIME_OUT,
  interceptors: {
    requestSuccessFn: (config) => {
      // add token for each request
      const token = localCache.getCache('token');
      if (config.headers && token) {
        config.headers.Authorization = 'Bearer ' + token;
      }
      return config;
    },
    responseSuccessFn: (res) => {
      //return res.data when success
      if (res.status >= 200 && res.status < 300) {
        return res.data;
      }
      return res;
    },
    responseFailureFn: (err) => {
      //handle the token expiration
      if (err.response.status === 401) {
        ElMessageBox.alert('No active account found with the given credentials.', 'Warning', {
          confirmButtonText: 'OK',
          callback: () => {
            localCache.removeCache('token');
            localCache.removeCache('userInfo');
            router.push('/login');
            router.go(0);
          }
        });
        return;
      }
      return Promise.reject(err);
    }
  }
});

export default request;
