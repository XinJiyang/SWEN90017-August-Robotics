<template>
  <div class="heading">
    <v-row>
      <span class="jobnum">Job#{{ JobData.id }} : Venue</span>
      <span class="jobvunue">{{ JobData.venue_name }}</span>
      <v-col class="text-right">
        <v-btn rounded="lg" color="#639843" size="small" class="fixed-buttons">
          Generate Job Summary
        </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-btn variant="text" color="#639843">All jobs</v-btn>
      <v-btn variant="text" color="#639843">General information</v-btn>
      <v-btn variant="text" color="#639843">Performance index</v-btn>
      <v-col class="text-right">
        <v-btn rounded="lg" color="#639843" size="small" class="fixed-buttons" @click="newItem">
          New Marking Job
        </v-btn>
      </v-col>
    </v-row>
  </div>
  <div class="markingjobs">
    <span class="mjheading">Marking Jobs</span>
    <div class="markingjobstable">
      <hot-table :data="hallData" :settings="settings" :style="style">
        <hot-column title="Hall" read-only="true" data="hallID"></hot-column>
        <hot-column title="Show" read-only="true" data="show"></hot-column>
        <hot-column title="Colour" read-only="true" data="color"></hot-column>
        <hot-column title="#Corners" read-only="true" data="numOfCorners"></hot-column>
        <hot-column title="#Numbers" read-only="true" data="numOfNumbers"></hot-column>
        <hot-column title="#Others" read-only="true" data="numOfOthers"></hot-column>
        <hot-column title="Net Area" read-only="true" data="netArea"></hot-column>
        <hot-column title="#Corners" data="finalCorners"></hot-column>
        <hot-column title="#Numbers" data="finalNumbers"></hot-column>
        <hot-column title="#Others" data="finalOthers"></hot-column>
        <hot-column title="Net Area" data="finalNetArea"></hot-column>
      </hot-table>
    </div>
  </div>
  <v-row>
    <v-col class="markingjobs2">
      <span class="mjheading">Versions</span>
      <div class="markingjobstable">
        <hot-table :data="versionData" :settings="settings2" :style="style">
          <hot-column title="Version Number" read-only="true" data="versionNum"></hot-column>
          <hot-column title="Data Changed" read-only="true" data="dataChanged"></hot-column>
          <hot-column title="Operate" read-only="true" data="operate"></hot-column>
        </hot-table>
      </div>
    </v-col>
    <v-col class="markingjobs3">
      <span class="mjheading">Totals</span>
      <div class="markingjobstable">
        <hot-table :data="totalDatas" :settings="settings2" :style="style">
          <hot-column title="Total#Halls" read-only="true" data="totalHalls"></hot-column>
          <hot-column title="Total#Marks" read-only="true" data="totalMarks"></hot-column>
          <hot-column title="Total#Shows" read-only="true" data="totalShows"></hot-column>
        </hot-table>
      </div>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import { VDataTable } from 'vuetify/labs/VDataTable';
import { onMounted, ref, type Ref } from 'vue';
import type { IJob, IMarkingJob } from '@/types';
import useJobDetailStore from '../../stores/job/jobdetails';
import useJobStore from '@/stores/job/job';
import { useRouter, useRoute } from 'vue-router';
import type { Country } from '@/utils/country';
import { HotTable, HotColumn } from '@handsontable/vue3';
import { registerAllModules } from 'handsontable/registry';
import 'handsontable/dist/handsontable.full.css';

console.log('Something');

const route = useRoute();
const jobDetailStore = useJobDetailStore();
const JobDetailData: Ref<Array<IMarkingJob>> = ref([]);
const JobData: Ref<IJob> = ref<IJob>({
  id: '',
  venue_name: '',
  region: undefined,
  show: '',
  start_date: undefined,
  end_date: undefined,
  status: undefined,
  markingJob: []
});

const jobStore = useJobStore();

onMounted(async () => {
  console.log(route.params.id);
  if (route.params.id !== '') {
    let id: string;
    if (Array.isArray(route.params.id)) {
      id = route.params.id[0];
    } else {
      id = route.params.id;
    }
    console.log(route.params.id);
    let jobInfo = await jobStore.getJob(id);
    console.log('jobInfo:' + jobInfo);
    if (jobInfo === undefined) {
      // cannot find client
      // TODO: add warning to notify user
    } else {
      // set retrieved value as default value
      JobData.value = jobInfo;
    }
  }
});

onMounted(async () => {
  if (route.params.id !== undefined) {
    let id: string;
    if (Array.isArray(route.params.id)) {
      id = route.params.id[0];
    } else {
      id = route.params.id;
    }
    let jobdetails = await jobDetailStore.getJobDetailList(id);
    JobDetailData.value = jobdetails;
  }
});

// register Handsontable's modules
registerAllModules();

const hallData = [
  {
    hallID: 'HALL-A1',
    show: 'NT23',
    color: 'BLUE',
    numOfCorners: 300,
    numOfNumbers: 300,
    numOfOthers: 300,
    netArea: '2000 m^2',
    finalCorners: 'Enter Data',
    finalNumbers: 'Enter Data',
    finalOthers: 'Enter Data',
    finalNetArea: 'Enter Data'
  },
  {
    hallID: 'HALL-A1',
    show: 'OM23',
    color: 'GREEN',
    numOfCorners: 300,
    numOfNumbers: 300,
    numOfOthers: 300,
    netArea: '2000m^ 2',
    finalCorners: 'Enter Data',
    finalNumbers: 'Enter Data',
    finalOthers: 'Enter Data',
    finalNetArea: 'Enter Data'
  },
  {
    hallID: 'HALL-A2',
    show: 'NT23',
    color: 'BLUE',
    numOfCorners: 300,
    numOfNumbers: 300,
    numOfOthers: 300,
    netArea: '2000 m^2',
    finalCorners: 'Enter Data',
    finalNumbers: 'Enter Data',
    finalOthers: 'Enter Data',
    finalNetArea: 'Enter Data'
  },
  {
    hallID: 'HALL-A3',
    show: 'NT23',
    color: 'BLUE',
    numOfCorners: 300,
    numOfNumbers: 300,
    numOfOthers: 300,
    netArea: '2000 m^2',
    finalCorners: 'Enter Data',
    finalNumbers: 'Enter Data',
    finalOthers: 'Enter Data',
    finalNetArea: 'Enter Data'
  },
  {
    hallID: 'HALL-A4',
    show: 'NT23',
    color: 'BLUE',
    numOfCorners: 300,
    numOfNumbers: 300,
    numOfOthers: 300,
    netArea: '2000 m^2',
    finalCorners: 'Enter Data',
    finalNumbers: 'Enter Data',
    finalOthers: 'Enter Data',
    finalNetArea: 'Enter Data'
  }
];
const versionData = [
  {
    versionNum: '#1.0',
    dataChanged: '28/02/2023',
    operate: ''
  }
];

function countUniqueHallKinds(data) {
  const uniqueHallKinds = new Set();

  for (const item of data) {
    uniqueHallKinds.add(item.hallID);
  }
  return uniqueHallKinds.size;
}

const numberOfUniqueHalls = countUniqueHallKinds(hallData);

const totalDatas = [
  {
    totalHalls: numberOfUniqueHalls,
    totalMarks: '28/02/2023',
    totalShows: ''
  }
];
const settings = {
  height: 'auto',
  overflow: 'hidden',
  rowHeights: 40,
  colWidths: 115,
  colHeaderHeight: 115,
  className: 'htMiddle',
  licenseKey: 'non-commercial-and-evaluation'
};
const settings2 = {
  height: 'auto',
  overflow: 'hidden',
  rowHeights: 40,
  colWidths: 170,
  colHeaderHeight: 115,
  className: 'htMiddle',
  licenseKey: 'non-commercial-and-evaluation'
};
const style = {
  style: 'font-size: 300px;'
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
