<template>
  <el-container>
    <el-header>
      <el-row align="center" justify="space-between" :gutter="10">
        <el-col :xs="24" :sm="6" :md="6" :lg="6">
          <h1 style="font-size: x-large">Job List</h1>
        </el-col>
        <el-col :xs="24" :sm="8" :md="6" :lg="5" :xl="4">
          <el-input
            v-model="jobStore.$state.search"
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
            style="float: right; margin-right: 10px"
            :icon="Plus"
            @click="openCreateJobDialog"
            >Add New Job
          </el-button>
        </el-col>
      </el-row></el-header
    >
    <el-main>
      <el-table
        :data="Jobs"
        style="border-radius: 20px"
        size="large"
        table-layout="auto"
        v-loading="loading"
        @sort-change="handleSort"
      >
        <el-table-column prop="id" label="ID" sortable="custom" />
        <el-table-column prop="venue_name" label="Venue" sortable="custom" />
        <el-table-column prop="region" label="Region" sortable="custom" />
        <el-table-column prop="show" label="Show" sortable="custom" />
        <el-table-column prop="start_date" label="Start Date" sortable="custom" />
        <el-table-column prop="end_date" label="End Date" sortable="custom" />
        <el-table-column prop="status" label="Status" sortable="custom">
          <template #default="scope">
            <el-tag
              size="large"
              :type="
                scope.row.status === JobStatus.NEW
                  ? 'danger'
                  : scope.row.status === JobStatus.CANCEL
                  ? 'info'
                  : scope.row.status === JobStatus.FINISH
                  ? 'success'
                  : ''
              "
              >{{ scope.row.status }}</el-tag
            >
          </template>
        </el-table-column>
        <el-table-column label="Operate" align="center">
          <template #default="scope">
            <el-popover trigger="hover">
              <template #reference>
                <el-icon><MoreFilled /></el-icon>
              </template>
              <el-menu style="border: none">
                <el-menu-item index="0"
                  v-show="loginStore.$state.userInfo.role !== 'viewer'"
                 @click="ViewJob(scope.row.id)
                 ">Edit</el-menu-item
                >
                <el-menu-item
                  v-show="loginStore.$state.userInfo.role !== 'viewer'"
                  index="2"
                  @click="DeleteJob(scope.row.id)"
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
        :total="clientStore.$state.totalPages*10"
        next-text="Next >>"
        prev-text="<< Previous"
        style="float: right"
        @update:current-page="handlePageChange"
      />
    </el-footer>
  </el-container>
  <el-dialog
    v-model="dialogFormVisible"
    center
    align-center
    style="border-radius: 20px"
    width="500px"
    @close="resetJobForm(jobFormRef)"
  >
    <el-form
      ref="jobFormRef"
      :model="jobForm"
      :rules="jobFormRules"
      label-position="left"
      label-width="180px"
      size="large"
    >
      <el-form-item label="Venue" prop="venue_name">
        <el-select v-loading="venueNameLoading" v-model="jobForm.venue_name" placeholder="Select">
          <el-option v-for="item in venueNameOptions" :key="item" :label="item" :value="item" />
        </el-select>
      </el-form-item>
      <el-form-item label="Start Date" prop="start_date">
        <el-date-picker
          v-model="jobForm.start_date"
          type="date"
          placeholder="Pick a Date"
          format="YYYY/MM/DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="End Date" prop="end_date">
        <el-date-picker
          v-model="jobForm.end_date"
          type="date"
          placeholder="Pick a Date"
          format="YYYY/MM/DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="Status" prop="status">
        <el-select v-model="jobForm.status" placeholder="Select">
          <el-option v-for="item in jstatus" :key="item" :label="item" :value="item" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button round type="danger" size="large" @click="resetJobForm(jobFormRef)"
        >Cancel</el-button
      >
      <el-button round type="success" size="large" @click="submitJobForm(jobFormRef)"
        >Save</el-button
      >
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, type Ref } from 'vue';
import { useRouter } from 'vue-router';
import { JobStatus, type IJob } from '@/types';
import useJobStore from '@/stores/job/job';
import { jstatus } from '@/types/job';
import useClientStore from '@/stores/client/client';
import { Search, DocumentAdd, Plus } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus';
import type { AxiosError } from 'axios';
import { jobAddRequest } from '@/service/job/job';
import useLoginStore from '@/stores/login/login';

// stores
const router = useRouter();
const clientStore = useClientStore();
const jobStore = useJobStore();
const loginStore = useLoginStore();

// loading
const loading = ref(false);

// create job dialog
const venueNameOptions: Ref<string[]> = ref([]);
const venueNameLoading = ref(false);
const dialogFormVisible = ref(false);
const jobFormRef = ref<FormInstance>();
const jobForm = reactive<IJob>({
  id: undefined,
  region: undefined,
  show: '',
  venue_name: '',
  start_date: undefined,
  end_date: undefined,
  status: JobStatus.NEW,
  markingJob: [],
  performance: undefined,
  employees: []
});
const jobFormRules = reactive<FormRules>({
  venue_name: [{ required: true, message: 'Please input hall name', trigger: 'blur' }],
  start_date: [{ required: true, message: 'Please input start date', trigger: 'blur' }],
  end_date: [{ required: true, message: 'Please input end date', trigger: 'blur' }]
});

async function openCreateJobDialog() {
  dialogFormVisible.value = true;

  venueNameLoading.value = true;
  venueNameOptions.value = await clientStore.getClientNameList();
  venueNameLoading.value = false;
}

async function submitJobForm(form: FormInstance | undefined) {
  if (!form) return;
  await form.validate((valid, fields) => {
    if (valid) {
      // confirmation
      ElMessageBox.confirm('Are you sure you want to create a new job?', 'Confirmation', {
        confirmButtonText: 'Yes',
        cancelButtonText: 'Cancel',
        type: 'warning',
        center: true,
        roundButton: true,
        beforeClose: async (action, instance, done) => {
          if (action === 'confirm') {
            // activate loading animation
            instance.confirmButtonLoading = true;
            instance.confirmButtonText = 'Loading...';

            try {
              // send request
              await jobAddRequest(jobForm);

              // request success
              instance.confirmButtonLoading = false;
              done();
              dialogFormVisible.value = false;
              ElMessage.success('Add new job successfully.');
              await handlePageChange();
            } catch (error) {
              // request fail
              if ((error as AxiosError).response?.status === 400) {
                ElMessage.error('Fail to add new job.');
              }
            }
          } else {
            done();
          }
        }
      });
    }
  });
}

function resetJobForm(form: FormInstance | undefined) {
  if (!form) return;
  form.resetFields();
  dialogFormVisible.value = false;
}

// job table
const Jobs: Ref<Array<IJob>> = ref([]);
async function handleSort({ column, prop, order }) {
  switch (order) {
    case 'ascending':
      jobStore.$state.sortBy = prop;
      jobStore.$state.sortOrder = true;
      break;
    case 'descending':
      jobStore.$state.sortBy = prop;
      jobStore.$state.sortOrder = false;
      break;
    default:
      jobStore.$state.sortBy = '';
      jobStore.$state.sortOrder = true;
      break;
  }

  await handlePageChange();
}

function EditJob(id: string) {
  router.push('/job/edit/' + id);
}

function ViewJob(id: string) {
  router.push('/job/view/' + id);
}

function DeleteJob(id: string) {
  jobStore.deleteJob(id);
}

async function handlePageChange(newPage?: number) {
  if (newPage !== undefined) {
    jobStore.$state.page = newPage;
  }

  loading.value = true;
  Jobs.value = await jobStore.getJobListWithPagination();
  loading.value = false;
}

// component lifecycle
onMounted(async () => {
  await handlePageChange();
});
</script>

<style lang="less" scoped>
*:not(.el-tag) {
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
    background-color: rgba(0, 0, 0, 0.1);
  }
}

.el-tag {
  font-size: large;
}

</style>
