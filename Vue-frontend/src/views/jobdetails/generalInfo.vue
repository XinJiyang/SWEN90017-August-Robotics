<template>
  <el-container style="background-color: white; border-radius: 10px">
    <el-header class="pt-4">
      <el-row :gutter="20" align="middle" justify="space-around">
        <el-col :span="5">{{
          generalInfo.start_date &&
          'Start Date:&nbsp;&nbsp;' + generalInfo.start_date.toLocaleDateString()
        }}</el-col>
        <el-col :span="5">{{
          generalInfo.end_date &&
          'End Date:&nbsp;&nbsp;' + generalInfo.end_date.toLocaleDateString()
        }}</el-col>
        <el-col :span="10">
          <el-space>
            Total Marking Days:
            <el-input-number
              v-model.number="total_mark_day"
              :min="1"
              :max="generalInfo.max_mark_day"
              controls-position="right"
              :disabled="!markingDayMode"
            />
            <el-button
              circle
              v-show="!markingDayMode"
              color="#639843"
              :icon="Edit"
              size="small"
              @click="markingDayMode = !markingDayMode"
            />
            <el-button
              circle
              v-show="markingDayMode"
              color="#639843"
              :icon="Check"
              size="small"
              :loading="saveMKButtonLoading"
              @click="handleMKSubmit"
            />
            <el-button
              circle
              v-show="markingDayMode"
              type="danger"
              :icon="Close"
              size="small"
              @click="handleMKReset"
            />
          </el-space>
        </el-col>
        <el-col :span="4"
          ><el-button round color="#639843" @click="handleMode" :loading="saveButtonLoading">{{
            mode ? 'Save' : 'Edit'
          }}</el-button
          ><el-button v-show="mode" round type="danger" @click="handleReset"
            >cancel</el-button
          ></el-col
        >
      </el-row>
    </el-header>
    <el-main class="pa-2" style="border-top: 2px solid lightgrey">
      <el-form ref="formRef" :model="form">
        <el-table :data="form" style="width: 100%" table-layout="auto" max-height="340">
          <el-table-column prop="name" label="Name">
            <template #default="scope">
              <el-form-item
                :prop="[scope.$index, 'name']"
                :rules="[{ required: true, message: 'name is required' }]"
              >
                <el-input v-model="scope.row.name" placeholder="name" :disabled="!mode" />
              </el-form-item>
            </template>
          </el-table-column>
          <el-table-column prop="type" label="Type">
            <template #default="scope">
              <el-form-item
                :prop="[scope.$index, 'type']"
                :rules="[{ required: true, message: 'type is required' }]"
              >
                <el-select v-model="scope.row.type" placeholder="Select Type" :disabled="!mode">
                  <el-option label="Full-time-employee" value="Full-time-employee"></el-option>
                  <el-option label="Helper" value="Helper"></el-option>
                </el-select>
              </el-form-item>
            </template>
          </el-table-column>

          <el-table-column prop="days" label="Work Day">
            <template #default="scope">
              <el-form-item
                :prop="[scope.$index, 'days']"
                :rules="[
                  { required: true, message: 'day is required' },
                  { type: 'number', message: 'day must be a number' }
                ]"
              >
                <el-input-number
                  v-model.number="scope.row.days"
                  :min="1"
                  controls-position="right"
                  :disabled="!mode"
                />
              </el-form-item>
            </template>
          </el-table-column>
          <el-table-column prop="hall" label="Hall">
            <template #default="scope">
              <el-form-item
                :prop="[scope.$index, 'hall']"
                :rules="[{ required: true, message: 'hall is required' }]"
              >
                <el-select v-model="scope.row.hall" placeholder="Select" :disabled="!mode">
                  <el-option
                    v-for="item in halls"
                    :key="item.id"
                    :label="item.hall"
                    :value="item.hall"
                  />
                </el-select>
              </el-form-item>
            </template>
          </el-table-column>
          <el-table-column v-if="mode" label="Operations">
            <template #default="scope">
              <el-button type="danger" size="small" @click.prevent="deleteRow(scope.$index)">
                Remove
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-button class="mt-4" color="#639843" style="width: 100%" v-show="mode" @click="addRow"
          >Add Row</el-button
        >
      </el-form>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import {
  editJobGeneralInfo,
  editTotalMarkingDay,
  getJobGeneralInfo
} from '@/service/job/jobGeneralInfo';
import { getJobHalls } from '@/service/job/jobdetails';
import type { IEmployee, IHall } from '@/types/job';
import type { AxiosError } from 'axios';
import { ElMessage, type FormInstance } from 'element-plus';
import { Check, Edit, Close } from '@element-plus/icons-vue';
import type { Ref } from 'vue';
import { reactive } from 'vue';
import { onMounted } from 'vue';
import { ref } from 'vue';

const props = defineProps<{ jobId: string | undefined }>();

interface IGeneralInfo {
  start_date?: Date;
  end_date?: Date;
  max_mark_day?: number;
  total_mark_day?: number;
}

const default_table: Ref<Array<IEmployee>> = ref([]);

// total marking day
const markingDayMode = ref(false);
const total_mark_day = ref(0);
const saveMKButtonLoading = ref(false);
async function handleMKSubmit() {
  saveMKButtonLoading.value = true;
  if (props.jobId) {
    try {
      await editTotalMarkingDay(props.jobId, total_mark_day.value);
      saveMKButtonLoading.value = false;
      markingDayMode.value = !markingDayMode.value;
      ElMessage.success('Update total marking day successfully.');
    } catch (error) {
      // request fail
      if ((error as AxiosError).response?.status === 400) {
        saveMKButtonLoading.value = false;
        ElMessage.error('Fail to update total marking day.');
      }
    }
  }
}

function handleMKReset() {
  if (generalInfo.total_mark_day) {
    total_mark_day.value = generalInfo.total_mark_day;
  }
  markingDayMode.value = !markingDayMode.value;
}

// table
const mode = ref(false); // true for edit, false for view-only
const formRef = ref<FormInstance>();
const form = ref<Array<IEmployee>>([]);
const saveButtonLoading = ref(false);
const halls = ref<Array<IHall>>([]);
const generalInfo: IGeneralInfo = reactive({});

async function handleMode() {
  if (!formRef.value) return;
  await formRef.value.validate(async (valid, fields) => {
    if (mode.value) {
      if (props.jobId && valid) {
        try {
          // send request
          saveButtonLoading.value = true;
          await editJobGeneralInfo(props.jobId, form.value);
          // request success
          saveButtonLoading.value = false;
          mode.value = !mode.value;
          ElMessage.success('Update general information successfully.');
        } catch (error) {
          // request fail
          if ((error as AxiosError).response?.status === 400) {
            saveButtonLoading.value = false;
            ElMessage.error('Fail to update general informatiom.');
          }
        }
      }
    } else {
      mode.value = !mode.value;
    }
  });
}

function handleReset() {
  if (!formRef.value) return;
  form.value = default_table.value;
  mode.value = !mode.value;
}

const deleteRow = (index: number) => {
  form.value.splice(index, 1);
};

const addRow = () => {
  form.value.push({
    name: '',
    type: '',
    days: 0,
    hall: ''
  });
};

onMounted(async () => {
  if (props.jobId) {
    // fetch generalInfo
    try {
      const res = await getJobGeneralInfo(props.jobId);
      generalInfo.start_date = new Date(res.start_date);
      generalInfo.end_date = new Date(res.end_date);
      generalInfo.total_mark_day = res.total_mark_day;

      // calculate maximum marking day
      if (generalInfo.start_date && generalInfo.end_date) {
        generalInfo.max_mark_day =
          (generalInfo.end_date.getTime() - generalInfo.start_date.getTime()) / (1000 * 3600 * 24);
      }

      if (generalInfo.total_mark_day) {
        total_mark_day.value = generalInfo.total_mark_day;
      }

      res.employees.forEach((element: IEmployee) => {
        default_table.value.push(element);
      });
      form.value = default_table.value.slice();

      // get hall list
      halls.value = await getJobHalls(props.jobId);
    } catch (error) {
      // request fail
      if ((error as AxiosError).response?.status === 400) {
        ElMessage.error('Fail to load data.');
      }
    }
  }
});
</script>
<style lang="less" scoped>
.el-header {
  font-size: medium;
}
.el-button {
  color: white;
}
</style>
