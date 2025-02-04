export interface IAccount {
  username: string;
  password: string;
}

export interface IUserInfo {
  username: string;
  email: string;
  role: 'admin' | 'operator' | 'viewer' | '';
}
