<template>
  <div class="markingjobs">
    <v-row>
      <span class="mjheading">Marking Jobs</span>
      <v-col class="text-right">
        <v-btn rounded="lg" color="#639843" size="small" class="fixed-buttons" @click="newJob"
          >New Marking Job</v-btn
        >
      </v-col>
    </v-row>
    <v-dialog v-model="newDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">New Marking Job</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-select
                  v-model="hall"
                  label="Hall Name"
                  :items="hallsData"
                  item-title="hall"
                  item-value="id"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field v-model="show" label="Show"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field v-model="colour" label="Colour"></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field v-model="pre_corners" label="Pre Corners"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field v-model="pre_numbers" label="Pre Numbers"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field v-model="pre_others" label="Pre Others"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field v-model="pre_area" label="Pre Area"></v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="6" md="4">
                <v-text-field v-model="fin_corners" label="Final Corners"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field v-model="fin_numbers" label="Final Numbers"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field v-model="fin_others" label="Final Others"></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field v-model="fin_area" label="Final Area"></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-row>
            <v-col class="text-right">
              <v-btn color="grey-darken-1" variant="text" @click="cancelNewJob" :disabled="hasSaved"> Cancel </v-btn>
              <v-btn ref="SaveNewButton" color="#639843" variant="text" @click="saveNewJob" :loading="singleNewSaveLoading" :disabled="hasSaved">
                Save
              </v-btn>
            </v-col>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <div class="handsontable htColumnHeaders">
      <hot-table ref="hotTableComponent" :settings="settings" :style="style" class="pb-2">
        <hot-column title="Hall" type="dropdown" :source="hallNames" data="mj_hall.hall"></hot-column>
        <hot-column title="Show" data="show"></hot-column>
        <hot-column title="Colour" data="colour"></hot-column>
        <hot-column title="Pre. # Corners" data="pre_corners"></hot-column>
        <hot-column title="Pre. # Numbers" data="pre_numbers"></hot-column>
        <hot-column title="Pre. # Others" data="pre_others"></hot-column>
        <hot-column title="Pre. Net Area" data="pre_area"></hot-column>
        <hot-column title="Fin. # Corners" data="fin_corners"></hot-column>
        <hot-column title="Fin. # Numbers" data="fin_numbers"></hot-column>
        <hot-column title="Fin. # Others" data="fin_others"></hot-column>
        <hot-column title="Fin. Net Area" data="fin_area"></hot-column>
      </hot-table>
    </div>
    <div>
      
    </div>
    <v-row>
      <v-col class="text-center">
        <v-progress-circular v-if="tableLoading"
      indeterminate
      color="#639843"
    ></v-progress-circular>
      </v-col>
      <v-col class="text-right" v-if="!tableLoading">
        <v-btn rounded="lg" color="#639843" size="small" class="fixed-buttons" @click="saveData" :loading="tableSaveLoading"
          >Save</v-btn
        >
      </v-col>
    </v-row>
    <v-divider></v-divider>
    <v-spacer></v-spacer>
    <div>
      <v-row>
        <v-col cols="4">
          <v-text-field
            v-model="rowNum"
            variant="solo"
            label="Rows to be added"
            hint="Must be greater than 2"
          >
            <template v-slot:append>
              <v-btn icon="mdi-plus" variant="elevated" @click="multipleNewJobs"></v-btn>
            </template>
          </v-text-field>
        </v-col>
      </v-row>
      <div v-show="newJobs">
        <hot-table ref="newJobsTable" :settings="newSettings" :style="style" class="pb-2">
          <hot-column type="dropdown" :source="hallNames" data="mj_hall.hall"></hot-column>
          <hot-column title="Show" data="show"></hot-column>
          <hot-column title="Colour" data="colour"></hot-column>
          <hot-column title="Pre. # Corners" data="pre_corners"></hot-column>
          <hot-column title="Pre. # Numbers" data="pre_numbers"></hot-column>
          <hot-column title="Pre. # Others" data="pre_others"></hot-column>
          <hot-column title="Pre. Net Area" data="pre_area"></hot-column>
          <hot-column title="Fin. # Corners" data="fin_corners"></hot-column>
          <hot-column title="Fin. # Numbers" data="fin_numbers"></hot-column>
          <hot-column title="Fin. # Others" data="fin_others"></hot-column>
          <hot-column title="Fin. Net Area" data="fin_area"></hot-column>
        </hot-table>
        <v-row>
          <v-col class="text-right">
            <v-btn rounded="lg" size="small" class="cancel-buttons" @click="cancelNewMultiJob" :disabled="hasSaved"
              >Cancel</v-btn
            >
            <v-btn
              rounded="lg"
              color="#639843"
              size="small"
              class="fixed-buttons"
              :loading="multiNewSaveLoading"
              :disabled="hasSaved"
              @click="saveNewMultiJobs"
              >Save</v-btn
            >
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { onMounted, ref, type Ref } from 'vue';
import { JobStatus, type IJob, type IMarkingJob, type IPerfromance, type IHall } from '@/types';
import useJobDetailStore from '../../stores/job/jobdetails';
import useJobStore from '@/stores/job/job';
import { useRoute } from 'vue-router';
import VGrid from '@revolist/vue3-datagrid';
import '@grapecity/spread-sheets/styles/gc.spread.sheets.excel2016colorful.css';
import { HotTable, HotColumn } from '@handsontable/vue3';
import { registerAllModules } from 'handsontable/registry';
import 'handsontable/dist/handsontable.full.css';
import { mdi } from 'vuetify/iconsets/mdi';

registerAllModules();

const route = useRoute();
let jobDetailStore = useJobDetailStore();
const hotTableComponent = ref(HotTable);
const newJobsTable = ref(HotTable);

// pass job Id from jobLayout
const props = defineProps<{ jobId: string | undefined }>();

const JobDetailData: Ref<Array<IMarkingJob>> = ref([]);
const NewJobDetailData: Ref<Array<IMarkingJob>> = ref([]);
const hallsData: Ref<Array<IHall>> = ref([]);
const hallNames: Ref<Array<string>> = ref([]);
const JobData: Ref<IJob> = ref<IJob>({
  id: '',
  venue_name: '',
  region: undefined,
  show: '',
  start_date: new Date(),
  end_date: new Date(),
  status: JobStatus.NEW,
  markingJob: [],
  employees: []
});

const settings = {
  height: 'auto',
  rowHeights: 40,
  startRows: 0,
  colWidths: 95,
  overflow: 'visible',
  colHeaderHeight: 115,
  className: 'htMiddle',
  licenseKey: 'non-commercial-and-evaluation',
};

const newSettings = {
  height: 'auto',
  startRows: 0,
  rowHeights: 40,
  colWidths: 95,
  overflow: 'visible',
  colHeaderHeight: 115,
  className: 'htMiddle',
  licenseKey: 'non-commercial-and-evaluation',
};

const newJobs = ref(false);
const rowNum = ref(0);

// TODO: use 0 instead of null value for numeric values as defaults
const hall = ref(undefined);
const show = ref('');
const colour = ref('');
const pre_corners = ref(0);
const pre_numbers = ref(0);
const pre_others = ref(0);
const pre_area = ref(0);
const fin_corners = ref(0);
const fin_numbers = ref(0);
const fin_others = ref(0);
const fin_area = ref(0);

const newDialog = ref(false);

const jobStore = useJobStore();

const tableLoading = ref(true);
const tableSaveLoading = ref(false);
const singleNewSaveLoading = ref(false);
const multiNewSaveLoading =  ref(false);
const hasSaved =  ref(false);

onMounted(async () => {
  const jobId = route.params.id;
  let jobIdString = jobId.toString();
  // extract id from params
  if (jobId) {
    // get basic info of a job
    let jobInfo = await jobStore.getJob(jobIdString);
    if (jobInfo === undefined) {
      // cannot find client
    } else {
      // set retrieved value as default value
      JobData.value = jobInfo;
    }

    // get marking jobs of a job
    let jobdetails = await jobDetailStore.getJobDetailList(jobIdString);
    console.log("mount");
    console.log(jobdetails);
    JobDetailData.value = jobdetails;

    // load data to table
    //loadData();
    hotTableComponent.value.hotInstance.loadData(JobDetailData.value);
    newJobsTable.value.hotInstance.loadData(NewJobDetailData.value);

    // gets all halls that client can have
    let halls = await jobDetailStore.getJobHalls(jobIdString);

    //console.log('getting halls data: ' + halls);
    hallsData.value = halls;
    halls.forEach((hall: { hall: string; }) => {
      hallNames.value.push(hall.hall);
    });
    //console.log(hallsData.value);
    //console.log(hallNames.value);
    tableLoading.value = false;
  }
});

// Function to transform halls objects into ids for the API call
function transformHalls(data:any, table:(typeof HotTable)){
  let currHalls = table.value.hotInstance.getDataAtCol(0);
  let i=0;
  currHalls.forEach((hallName:string) => {
    data[i].mj_hall = findHallId(hallName);
    i++;
  });
  return data
}

// Function to find the appropriate hall name
function findHallId(name:string) {
  let index = hallNames.value.findIndex((hall_name: string) => hall_name == name);
  return hallsData.value[index].id;
}

// Save changes to marking jobs
async function saveData() {
  tableSaveLoading.value = true;
  let data = JSON.parse(JSON.stringify(JobDetailData.value));
  console.log('save:');
  console.log('currHalls:');
  transformHalls(data, hotTableComponent);
  console.log(data);
  await jobDetailStore.editMarkingJobs(route.params.id.toString(), data);
  tableSaveLoading.value = false;
  //location.reload();
}

function multipleNewJobs() {
  let rows = rowNum.value;
  if (rows < 2) {
    // Stop
  } else {
    newSettings.startRows = rows;
    let emptyTable: IMarkingJob[] = [];
    for (let index = 0; index < rows; index++) {
      emptyTable.push({
        id: '',
        mj_hall: JSON.parse(JSON.stringify(hallsData.value[0])),
        show: JobDetailData.value[0].show,
        colour: '',
        pre_corners: 0,
        pre_numbers: 0,
        pre_others: 0,
        pre_area: 0,
        fin_corners: 0,
        fin_numbers: 0,
        fin_others: 0,
        fin_area: 0
      });
    }
    NewJobDetailData.value = emptyTable;
    console.log('generating empty table:');
    //console.log(NewJobDetailData.value);
    newJobs.value = true;
    newJobsTable.value.hotInstance.loadData(NewJobDetailData.value);
    console.log(NewJobDetailData.value);
  }
}

async function cancelNewMultiJob() {
  hasSaved.value = false;
  newJobs.value = false;
  newSettings.startRows = 0;
  NewJobDetailData.value = [];
}

async function saveNewMultiJobs() {
  console.log("saving new marking jobs");
  multiNewSaveLoading.value = true;
  hasSaved.value = true;
  if (route.params.id && route.params.id !== '') {
    let id: string;

    if (Array.isArray(route.params.id)) {
      id = route.params.id[0];
    } else {
      id = route.params.id;
    }
    
    console.log(NewJobDetailData.value);

    try {
      let data = JSON.parse(JSON.stringify(NewJobDetailData.value));
      transformHalls(data, newJobsTable);
      const processAsyncData = async (item: IMarkingJob) => {
        await jobDetailStore.addNewJobDetail(id,item);
      };

      for (const item of data) {
        await processAsyncData(item);
      }

      multiNewSaveLoading.value = false;
      location.reload()
    } catch (error) {
      console.error("Error while saving new marking jobs:", error);
      return;
    }
  } else {
    console.warn("ID is not provided or empty");
  }
  
}

async function newJob() {
  newDialog.value = true;
  console.log('New Marking Job');
  console.log(route.params.id);
}

async function saveNewJob() {
  singleNewSaveLoading.value = true;
  hasSaved.value = true;
  if (route.params.id !== '') {
    let id: string;
    if (Array.isArray(route.params.id)) {
      id = route.params.id[0];
    } else {
      id = route.params.id;
    }
    let newMarkingJob = {
      id: '',
      mj_hall: hall.value,
      show: show.value,
      colour: colour.value,
      pre_corners: pre_corners.value,
      pre_numbers: pre_numbers.value,
      pre_others: pre_others.value,
      pre_area: pre_area.value,
      fin_corners: fin_corners.value,
      fin_numbers: fin_numbers.value,
      fin_others: fin_others.value,
      fin_area: fin_area.value,
    };
    console.log('getMarkingJob');
    console.log(newMarkingJob);
    await jobDetailStore.addNewJobDetail(id, newMarkingJob);
    newDialog.value = false;
    singleNewSaveLoading.value = false;
    location.reload();
  }
}

function cancelNewJob() {
  hasSaved.value = false;
  newDialog.value = false;
}



const style = {
  style: 'font-size: 300px'
};
</script>
<script lang="ts">
export default {
  components: {
    HotTable,
    HotColumn
  }
};
const showPerformanceIndex = ref(false);
const togglePerformanceIndex = () => {
  console.log('Toggle Performance Index');
  showPerformanceIndex.value = !showPerformanceIndex.value;
};
</script>

<style lang="less" scoped>
.heading {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: x-large;
  color: #838383;
  font-weight: 600;
  margin-left: 2em;
  padding-top: 1em;
}
.handsontable .htDropdownMenu {
    position: fixed !important;
    overflow: visible !important;
    max-height: auto; /* Or set it to a specific value if needed */
    z-index: 1000; /* Ensures it's on top of other elements */
}

.handsontable {
    overflow: visible !important;
}

.textfield {
  background-color: white;
}
.jobnum {
  font-weight: 700;
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
.cancel-buttons {
  margin-right: 10px;
  margin-bottom: 1em;
  padding-right: 4px;
  color: black;
}
.markingjobs {
  margin-left: 0;
  padding-top: 0;
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
