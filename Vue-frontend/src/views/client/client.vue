<template>
  <el-container>
    <el-header>
      <el-row align="center" justify="space-between" :gutter="10">
        <el-col :xs="24" :sm="6" :md="6" :lg="6">
          <h1 style="font-size: x-large">Client List</h1>
        </el-col>
        <el-col :xs="24" :sm="8" :md="6" :lg="5" :xl="4">
          <el-input
            v-model="clientStore.$state.search"
            placeholder="Search..."
            clearable
            style="float: right"
            @change="handlePageChange"
            @clear="handlePageChange"
          >
            <template #suffix>
              <el-icon><search /></el-icon>
            </template>
            ></el-input
          >
        </el-col>
        <el-col :xs="24" :sm="10" :md="12" :lg="10" :xl="5">
          <el-button round size="large" color="#639843" style="float: right" :icon="DocumentAdd"
            >Export Data
          </el-button>
          <el-button
            round
            size="large"
            color="#639843"
            @click="AddNewClient"
            style="float: right; margin-right: 10px"
            :icon="Plus"
            >Add New Client
          </el-button>
        </el-col>
      </el-row></el-header
    >
    <el-main>
      <el-table
        :data="clients"
        style="border-radius: 20px"
        size="large"
        table-layout="auto"
        v-loading="loading"
        @sort-change="handleSort"
      >
        <el-table-column prop="id" label="ID" sortable="custom" />
        <el-table-column prop="venue_name" label="Venue Name" sortable="custom" />
        <el-table-column prop="region" label="Region" sortable="custom" />
        <el-table-column prop="email" label="Email" sortable="custom" />
        <el-table-column prop="phone" label="Phone Number" sortable="custom" />
        <el-table-column label="Operate" align="center">
          <template #default="scope">
            <el-popover trigger="hover">
              <template #reference>
                <el-icon><MoreFilled /></el-icon>
              </template>
              <el-menu style="border: none">
                <el-menu-item index="0" @click="ViewClient(scope.row.id)">View</el-menu-item
                ><el-menu-item
                  v-show="loginStore.$state.userInfo.role !== 'viewer'"
                  index="1"
                  @click="EditClient(scope.row.id)"
                  >Edit</el-menu-item
                >
                <el-menu-item
                  v-show="loginStore.$state.userInfo.role !== 'viewer'"
                  index="2"
                  @click="DeleteClient(scope.row.id)"
                  style="color: red"
                  >Delete</el-menu-item
                ></el-menu
              >
            </el-popover>
          </template>
        </el-table-column>
      </el-table></el-main
    >
    <el-footer>
      <el-pagination
        background
        layout="prev, pager, next"
        :total= "clientStore.$state.totalPages*10"
        next-text="Next >>"
        prev-text="<< Previous"
        style="float: right"
        @update:current-page="handlePageChange"
      />
    </el-footer>
  </el-container>
</template>

<script setup lang="ts">
import { onMounted, ref, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import useClientStore from '@/stores/client/client';
import type { IClient } from '@/types';
import type { ElContainer } from 'element-plus';
import { Search, DocumentAdd, Plus } from '@element-plus/icons-vue';
import useLoginStore from '@/stores/login/login';

// store
const router = useRouter();
const clientStore = useClientStore();
const loginStore = useLoginStore();

// loading
const loading = ref(false);

// table data
const clients: Ref<Array<IClient>> = ref([]);

async function handleSort({ column, prop, order }) {
  switch (order) {
    case 'ascending':
      clientStore.$state.sortBy = prop;
      clientStore.$state.sortOrder = true;
      break;
    case 'descending':
      clientStore.$state.sortBy = prop;
      clientStore.$state.sortOrder = false;
      break;
    default:
      clientStore.$state.sortBy = '';
      clientStore.$state.sortOrder = true;
      break;
  }

  await handlePageChange();
}

function AddNewClient() {
  router.push('/client/create');
}

function ViewClient(id: string) {
  router.push('/client/detail/' + id);
}

function EditClient(id: string) {
  router.push('/client/edit/' + id);
}

async function DeleteClient(id: string) {
  await clientStore.deleteClient(id);
  router.push('/client');
}

async function handlePageChange(newPage?: number) {
  if (newPage !== undefined) {
    clientStore.$state.page = newPage;
  }
  loading.value = true;
  clients.value = await clientStore.getClientListWithPagination();
  loading.value = false;

  console.log(clients.value);
  console.log(clientStore.$state.page)
  console.log(clientStore.$state.totalPages)
}


onMounted(async () => {
  await handlePageChange();
});
</script>

<style lang="less" scoped>
* {
  --el-color-primary: #639843;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: large;
  color: #838383;
}

.el-container {
  padding: 20px 10px;
  background-color: #f6f6f6;
  border-radius: 20px;
  height: 100%;
}

.el-button {
  color: white;
}

.el-menu-item {
  display: flex;
  justify-content: center;
  align-items: center;

  &:hover {
    background-color: #d9ebca;
  }
}
</style>
