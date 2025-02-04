import axios from 'axios';
import type { AxiosInstance } from 'axios';
import type { RequestConfig } from './type';

//Encapsulate axios
class Request {
  instance: AxiosInstance;

  // request instance => axios instance
  constructor(config: RequestConfig) {
    this.instance = axios.create(config);

    // add interceptors for each Request instance
    this.instance.interceptors.request.use(
      (config) => {
        return config;
      },
      (err) => {
        return Promise.reject(err);
      }
    );
    this.instance.interceptors.response.use(
      (res) => {
        return res;
      },
      (err) => {
        return Promise.reject(err);
      }
    );

    // add interceptors for a specific Request instance
    this.instance.interceptors.request.use(
      config.interceptors?.requestSuccessFn,
      config.interceptors?.requestFailureFn
    );
    this.instance.interceptors.response.use(
      config.interceptors?.responseSuccessFn,
      config.interceptors?.responseFailureFn
    );
  }

  // Encapsulated network request method
  // T => IHomeData
  request<T = any>(config: RequestConfig<T>) {
    // Successful intercept handling of a single request
    if (config.interceptors?.requestSuccessFn) {
      config = config.interceptors.requestSuccessFn(config);
    }

    // return Promise
    return new Promise<T>((resolve, reject) => {
      this.instance
        .request<any, T>(config)
        .then((res) => {
          // Successful intercept handling of a single response
          if (config.interceptors?.responseSuccessFn) {
            res = config.interceptors.responseSuccessFn(res);
          }
          resolve(res);
        })
        .catch((err) => {
          reject(err);
        });
    });
  }

  get<T = any>(config: RequestConfig<T>) {
    return this.request({ ...config, method: 'GET' });
  }
  post<T = any>(config: RequestConfig<T>) {
    return this.request({ ...config, method: 'POST' });
  }
  delete<T = any>(config: RequestConfig<T>) {
    return this.request({ ...config, method: 'DELETE' });
  }
  patch<T = any>(config: RequestConfig<T>) {
    return this.request({ ...config, method: 'PATCH' });
  }
  put<T = any>(config: RequestConfig<T>) {
    return this.request({ ...config, method: 'PUT' });
  }
}

export default Request;
