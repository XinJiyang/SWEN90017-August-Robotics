import request from '..';
import type { IAccount } from '@/types';

export function userLoginRequest(account: IAccount) {
  return request.post({
    url: '/user/login',
    data: account
  });
}

export function userRegisterRequest(account: any) {
  return request.post({
    url: '/user/register',
    data: {
      username: account.username,
      password: account.password,
      privilege: account.privilege
    }
  });
}
