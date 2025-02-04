import { createApp } from 'vue';

import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import 'element-plus/theme-chalk/el-message.css';
import 'element-plus/theme-chalk/el-message-box.css';

import 'normalize.css';
import './assets/css/index.less';

import App from './App.vue';
import router from './router';
import pinia from './stores';
import useLoginStore from './stores/login/login';

// Vuetify
import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import VueExcelEditor from 'vue3-excel-editor'


const app = createApp(App);

//element-plus icon
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

export const vuetify = createVuetify({
  components,
  directives
});

app.use(vuetify);

app.use(pinia);
useLoginStore().loadLocalCacheAction();

app.use(router);
app.use(VueExcelEditor)

app.mount('#app');
