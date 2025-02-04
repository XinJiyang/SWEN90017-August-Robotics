import type { RouteRecordRaw } from 'vue-router';

export function mapRoleToRoutes(
  role: 'admin' | 'operator' | 'viewer' | '',
  routes: RouteRecordRaw[]
) {
  const allowedRoutes = [];

  routes.forEach((item) => {
    if (item.children) {
      const temp = item;
      temp.children = item.children.filter((c) => {
        const roles = c.meta?.roles;
        return Array.isArray(roles) && roles.includes(role);
      });
      console.log(temp);
      console.log(item);
      allowedRoutes.push(temp);
    } else {
      const roles = item.meta?.roles;
      if (Array.isArray(roles) && roles.includes(role)) {
        allowedRoutes.push(item);
      }
    }
  });
  return allowedRoutes;
}
