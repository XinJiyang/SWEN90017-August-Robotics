<template>
    <div class = "heading">
        <div style="padding-bottom: 15px;">
            <el-row align="center" justify="space-between" :gutter="10">
                <el-col :xs="24" :sm="10" :md="12" :lg="6"><h1 style="font-size: x-large">Job Summary</h1></el-col>
                <el-col :xs="24" :sm="10" :md="12" :lg="10" :xl="5"><el-button round size="large" color="#639843" style="float: right; color:white; " 
                    @click="onDownloadClick" :icon="Download">Download
          </el-button></el-col>
            </el-row>
        </div>

        <el-descriptions title="" :column="3" border  style="padding-bottom: 15px;">
            <el-descriptions-item
                label="Venue Name"
                label-align="right" 
                align ="center"
                label-class-name="my-label"
                class-name="my-content"
                width="150px"
                ><el-tag size="small">{{ JobSummary.client?.venue_name }}</el-tag></el-descriptions-item
            >
            <el-descriptions-item label="Region" label-align="right" align="center"
                >{{ JobSummary.client?.region }}</el-descriptions-item
            >
            <el-descriptions-item label="Phone Number" label-align="right" align="center"
                >{{ JobSummary.client?.phone }}</el-descriptions-item
            >
            <el-descriptions-item label="Email" label-align="right" align="center">
                {{ JobSummary.client?.email }}
            </el-descriptions-item>
            <el-descriptions-item label="Start Date" label-align="right" align="center"
                > {{ JobSummary.job?.start_date }}</el-descriptions-item
            >
            <el-descriptions-item label="End Date" label-align="right" align="center"
                > {{ JobSummary.job?.end_date }}</el-descriptions-item
            >
        </el-descriptions>


   <main class="container max-w-5xl mx-auto text-zinc-600 px-6">
    <div id="downloadable-element">
      <div class="invoice-box">
        <table cellpadding="0" cellspacing="0">
          <tr class="top">
            <td colspan="2">
              <table>
                <tr>
                  <td class="title">
                    <img class="logo" src="@/assets/img/ar_logo_02.jpg" />
                  </td>

                  <td>
                    Job Summary # {{ JobSummary.job?.id  }}<br />
                    Created at {{ formattedDate }}<br /><br />
                    Start Date {{ JobSummary.job?.start_date }}<br />
                    End Date {{ JobSummary.job?.end_date }}<br />
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr class="information">
            <td colspan="2">
              <table>
                <tr>
                  <td>
                    <br />
                    August Robotics<br />
                    <a href="https://augustrobotics.com/about/" target="_blank" style="color:darkgreen;">Official Website</a><br />
                    info@augustrobotics.com
                  </td>

                  <td>
                    {{ JobSummary.client?.venue_name }}<br />
                    {{ JobSummary.client?.region }}<br />
                    {{ JobSummary.client?.phone }}<br />
                    {{ JobSummary.client?.email }}
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        
        <v-table>
          <tbody>
          <tr style="background-color: #f6f6f6;  color: #838383;">
            <td class="text-left">Job Done</td>
            <td class="text-right">Results</td>
          </tr>
          <tr>
            <td class="text-left" >Total Halls</td>
            <td class="text-right">{{ JobSummary.performance?.total_halls}}</td>
          </tr>
          <tr>
            <td class="text-left" >Total Marks</td>
            <td class="text-right">{{ JobSummary.performance?.total_marks }}</td>
          </tr>
          <tr>
            <td class="text-left" >Total shows</td>
            <td class="text-right">{{ JobSummary.performance?.total_shows }}</td>
          </tr>
          <tr>
            <td class="text-left" >Marks/Day</td>
            <td class="text-right">{{ JobSummary.performance?.marks_day }}</td>
          </tr>
          <tr>
            <td class="text-left">Marks/FTE/Day</td>
            <td class="text-right">{{ JobSummary.performance?.marks_fte_day }}</td>
          </tr>
          <tr>
            <td class="text-left">Marks/Person/Day</td>
            <td class="text-right">{{ JobSummary.performance?.marks_person_day }}</td>
          </tr>
          <tr>
            <td class="text-left">FTE Ratio</td>
            <td class="text-right">{{ JobSummary.performance?.fte_ratio }}</td>
          </tr>
          <tr>
            <td class="text-left">Halls/Day</td>
            <td class="text-right">{{ JobSummary.performance?.halls_day }}</td>
          </tr>
          <tr>
            <td class="text-left">#FTE</td>
            <td class="text-right">{{ JobSummary.performance?.fte }}</td>
          </tr>
          <tr>
            <td class="text-left">#Intern/Helper</td>
            <td class="text-right">{{ JobSummary.performance?.intern_helper }}</td>
          </tr>
          <tr>
            <td class="text-left">#FTE Engineer Days</td>
            <td class="text-right">{{ JobSummary.performance?.fte_engineer_days }}</td>
          </tr>
          <tr>
            <td class="text-left">#Intern/Helper Days</td>
            <td class="text-right">{{ JobSummary.performance?.intern_helper_days }}</td>
          </tr><br />
          <tr style="color: #838383;">
            Notes <br /><br />
          </tr>
          </tbody>
        </v-table>
        <div style="height: 200px; border: 1px solid grey;"></div>

        </table>
      </div>
    </div>
  </main>

    </div>
  </template>
  
<script setup lang="ts">
/* __placeholder__ */
import type { ISummary } from '@/types';
import { onMounted} from 'vue';
import { ref, type Ref } from 'vue';
import { useRoute} from 'vue-router';
import { getJobSummary } from '@/service/job/jobSummary';
import { Download } from '@element-plus/icons-vue';

const date = new Date();
const formattedDate = `${date.getDate()}-${date.getMonth() + 1}-${date.getFullYear()}`;


const route = useRoute();

const JobSummary: Ref<ISummary> = ref({
    job: undefined,
    client: undefined,
    performance: undefined
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

    // fetch job summary
    let summaryRes = await getJobSummary(id);
    if (summaryRes) {
      JobSummary.value = summaryRes;
      console.log(JobSummary)
    } else {
      // fail to fetch job data
    }
  }
});

const onDownloadClick = () => {
  window.print();
};
</script>


<style scoped>
.heading {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: x-large;
  color: #838383;
  font-weight: 600;
  padding: 30px;
  background-color: #f6f6f6;
  border-radius: 20px;
}

*:not(.el-tag) {
  --el-color-primary: #639843;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: large;
}

.invoice-box {
  /* max-width: 800px; */
  margin: auto;
  padding: 30px;
  background-color: white;
  border: 1px solid #eee;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
  font-size: 16px;
  line-height: 24px;
}

.invoice-box table {
  width: 100%;
  line-height: inherit;
  text-align: left;
}

.invoice-box table td {
  padding: 5px;
  vertical-align: top;
}

.invoice-box table tr td:nth-child(2) {
  text-align: right;
}

.invoice-box table tr.top table td {
  padding-bottom: 20px;
}

.invoice-box table tr.top table td.title {
  font-size: 45px;
  line-height: 45px;
  color: #333;
}

.invoice-box table tr.information table td {
  padding-bottom: 40px;
}

.invoice-box table tr.heading td {
  background: #eee;
  border-bottom: 1px solid #ddd;
  font-weight: bold;
}


@media only screen and (max-width: 600px) {
  .invoice-box table tr.top table td {
    width: 100%;
    display: block;
    text-align: center;
  }

  .invoice-box table tr.information table td {
    width: 100%;
    display: block;
    text-align: center;
  }
}

@page {
  size: auto;
  margin: 4mm;
}
</style>