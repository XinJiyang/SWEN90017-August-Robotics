<template>
  <div class="heading">
    <v-row>
      <span class="jobnum">Job#{{ JobData.id }}&nbsp;: &nbsp;Venue</span>
      <span class="jobvunue">&nbsp;{{ JobData.venue_name }} &nbsp;</span>
      <v-btn rounded="lg" icon="mdi-pencil" size="medium" class="edit-button" variant="plain" @click="openEditJobDialog"></v-btn>
      <v-col class="text-right">
        <v-btn rounded="lg" color="#639843" size="small" class="fixed-buttons" @click = "ViewJobSummary(JobData.id)"
          >Generate Job Summary</v-btn>
      </v-col>
    </v-row>
    <v-tabs v-model="tab" color="#639843">
      <v-tab :value="1">All jobs</v-tab>
      <v-tab :value="2">General information</v-tab>
      <v-tab :value="3">Performance index</v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <v-window-item :value="1">
        <!-- Add job detail here -->
        <v-container fluid><jobdetails :jobId="extractIdFromParams()" /></v-container>
      </v-window-item>
      <v-window-item :value="2">
        <!-- Add general info here -->
        <v-container fluid><generalInfo :jobId="extractIdFromParams()" /></v-container>
      </v-window-item>
      <v-window-item :value="3">
        <v-container fluid
          ><performance
            :start_date="JobData.start_date"
            :end_date="JobData.end_date"
            :data="JobPerformance"
        /></v-container>
      </v-window-item>
    </v-window>
  </div>
  <div>
    <!-- Dialog pop up -->
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
      :model="JobData"
      :rules="jobFormRules"
      label-position="left"
      label-width="180px"
      size="large"
    >
      <el-form-item label="Start Date" prop="start_date">
        <el-date-picker
          v-model="JobData.start_date"
          type="date"
          placeholder="Pick a Date"
          format="YYYY/MM/DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="End Date" prop="end_date">
        <el-date-picker
          v-model="JobData.end_date"
          type="date"
          placeholder="Pick a Date"
          format="YYYY/MM/DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="Status" prop="status">
        <el-select v-model="JobData.status" placeholder="Select">
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
  </div>
</template>

<script setup lang="ts">
import useJobStore from '@/stores/job/job';
import { JobStatus, type IJob, type IMarkingJob, type IPerfromance } from '@/types';
import { onMounted,reactive } from 'vue';
import { ref, type Ref } from 'vue';
import { loadRouteLocation, useRoute, useRouter } from 'vue-router';
import performance from './performance.vue';
import jobdetails from './jobdetails.vue';
import generalInfo from './generalInfo.vue';
import { getJobPerformanceIndex } from '@/service/job/jobPerformanceIndex';
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus';
import { jstatus } from '@/types/job';


const tab = ref(null);

const route = useRoute();

const router = useRouter();

const jobStore = useJobStore();

const JobDetailData: Ref<Array<IMarkingJob>> = ref([]);

const JobData: Ref<IJob> = ref({
  id: '',
  venue_name: '',
  region: undefined,
  show: '',
  start_date: new Date(),
  end_date: new Date(),
  status: JobStatus.NEW,
  markingJob: [],
  performance: undefined,
  employees: []
});

const JobPerformance: Ref<IPerfromance> = ref({
  total_halls: 0,
  total_shows: 0,
  total_marks: 0,
  marks_day: 0,
  marks_fte_day: 0,
  marks_person_day: 0.0,
  marks_window: 0,
  marks_hall: 0,
  halls_day: 0.0,
  fte: 0,
  intern_helper: 0,
  fte_engineer_days: 0,
  intern_helper_days: 0,
  fte_ratio: 0.0
});

const dialogFormVisible = ref(false);

const jobFormRef = ref<FormInstance>();

const jobFormRules = reactive<FormRules>({
  start_date: [{ required: true, message: 'Please input start date', trigger: 'blur' }],
  end_date: [{ required: true, message: 'Please input end date', trigger: 'blur' }]
});

function extractIdFromParams(): string | undefined {
  let id: string | undefined;

  if (route.params.id !== undefined && route.params.id !== '') {
    if (Array.isArray(route.params.id)) {
      id = route.params.id[0];
    } else {
      id = route.params.id;
    }
  }

  return id;
}

onMounted(async () => {
  // extract id from params
  let id = extractIdFromParams();
  if (id) {
    // fetch basic job data
    let res = await jobStore.getJob(id);
    if (res) {
      JobData.value = res;
    } else {
      // fail to fetch job data
    }

    // fetch general info

    // fetch performance index
    let performanceRes = await getJobPerformanceIndex(id);
    if (performanceRes) {
      JobPerformance.value = performanceRes;
    } else {
      // fail to fetch job data
    }
  }
});

function ViewJobSummary(id: string | undefined) {
  router.push('/job/summary/' + id);
}

async function openEditJobDialog() {
  dialogFormVisible.value = true;
}

async function submitJobForm(form: FormInstance | undefined) {
  if (!form) return;
  await form.validate((valid, fields) => {
    if (valid) {
      // confirmation
      ElMessageBox.confirm('Are you sure you want to change this job?', 'Confirmation', {
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
              if (JobData.value.id===undefined) {
                throw console.error();
              }else{
                console.log("Save Form");
                console.log(JobData.value);
                await jobStore.editJob(JobData.value.id, JobData.value);
                location.reload();
              }
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

</script>

<style lang="less" scoped>
.heading {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: x-large;
  color: #838383;
  font-weight: 600;
  padding: 30px;
  background-color: #f6f6f6;
  border-radius: 20px;
}
.jobnum {
  font-weight: 700;
  margin-left: 0.5em;
}
.jobvunue {
  margin-left: 0.5em;
  font-weight: 350;
}
.fixed-buttons {
  margin-right: 10px;
  margin-bottom: 1em;
  color: white;
}

.edit-button{
  margin-right: 40px;
  margin-bottom: 1em;
}

.edit-button:hover {
  color: #639843; /* Change the color on hover */
}
.markingjobs {
  margin-left: 2em;
  padding-top: 1em;
}
.markingjobs2 {
  margin-left: 2em;
  padding-top: 6em;
}
.markingjobs3 {
  margin-left: 1em;
  padding-top: 6em;
}
.mjheading {
  font-weight: 700;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: x-large;
  color: #838383;
}
.markingjobstable {
  margin-top: 1em;
  text-align: center;
  height: 200px;
  overflow: auto;
}
</style>
