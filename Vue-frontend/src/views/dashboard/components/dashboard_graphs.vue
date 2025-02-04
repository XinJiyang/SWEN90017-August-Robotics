<template>
  <div>
    <button
      @click="selectPostPandemicGraph"
      class="fixed-buttons"
      style="
        margin-right: 35px;
        margin-bottom: 1em;
        background-color: #639843;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        color: #fff;
        cursor: pointer;
      "
    >
      Average Marks per Day (post pandemic)
    </button>
    <button
      @click="selectPrePandemicGraph"
      class="fixed-buttons"
      style="
        background-color: #639843;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        color: #fff;
        cursor: pointer;
      "
    >
      Average Marks per Day (pre pandemic)
    </button>
    <button
      @click="selectLineChart"
      class="fixed-buttons"
      style="
        margin-left: 35px;
        background-color: #639843;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        color: #fff;
        cursor: pointer;
      "
    >
      Line Chart for FTE Days and Intern Days
    </button>
    <div class="year-selector">
      <label for="yearSelect">Select Year:</label>
      <select id="yearSelect" v-model="selectedYear" @change="displayGraphForYear">
        <option value="all">All</option>
        <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
      </select>
    </div>
    <v-select
      v-model="selectedClients"
      :items="clients"
      label="Select Clients"
      multiple
      chips
      solo-inverted
      @change="displayGraph()"
    />
    <div v-if="noDataMessage">
      <p style="color: red">{{ noDataMessage }}</p>
    </div>
    <div v-if="showChart" style="height: 500px">
      <Bar :options="chartOptions" :data="chartData" />
    </div>
    <div v-if="showLineChart" style="height: 500px">
      <Line :options="lineChartOptions" :data="lineChartData" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, reactive, watch } from 'vue';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement
} from 'chart.js';
import { Bar } from 'vue-chartjs';
import { Line } from 'vue-chartjs';
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement
);

import useClientStore from '@/stores/client/client';

const showChart = ref(false);
const showLineChart = ref(false);
const chartData = ref<{
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor: string;
    borderColor: string;
    borderWidth: number;
  }[];
}>({
  labels: [],
  datasets: []
});

const selectedYear = ref('all');
const availableYears = ref([2018, 2019, 2018, 2020, 2021, 2022, 2023, '']);

const lineChartData = ref({
  labels: [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
  ],
  datasets: [
    {
      label: 'Total FTE Days',
      data: [], 
      borderColor: '#f87979',
      fill: false,
      datalabels: {
        align: 'end',
        anchor: 'end',
        formatter: function(value, context) {
    
          return context.dataset.years[context.dataIndex];
        }
      },
      years: [] // This should hold the year data for each data point
    },
    {
      label: 'Total Intern Days',
      data: [], // your data
      borderColor: '#2962FF',
      fill: false,
      datalabels: {
        align: 'end',
        anchor: 'end',
        formatter: function(value, context) {
          return context.dataset.years[context.dataIndex];
        }
      },
      years: [] // This should hold the year data for each data point
    }
  ]
});

const chartOptions = {
  scales: {
    x: { title: { display: true, text: 'Client' } },
    y: { title: { display: true, text: 'Values' } }
  }
};

const clients = ref([]);
const selectedClients = ref([]);
const diagramType = ref('');
const clientStore = useClientStore();
const noDataMessage = ref('');
console.log(selectedClients.value);

onMounted(async () => {
  try {
    const response = await clientStore.getClientNameList();

    console.log(response);
    clients.value = response;
  } catch (error) {
    console.error('There was an error!', error);
  }
});

const selectLineChart = () => {
  diagramType.value = 'lineChart';
};

const selectPostPandemicGraph = () => {
  diagramType.value = 'postPandemicDiagram';
};

const selectPrePandemicGraph = () => {
  diagramType.value = 'prePandemicDiagram';
};

const displayGraph = () => {
  displayPostPandemicGraph();
  displayPrePandemicGraph();
  displayLineChart();
};
const displayPostPandemicGraph = async () => {
  if (selectedClients.value.length) {
    let result;

    if (selectedYear.value == 'all') {
      result = await clientStore.getClientSummary(selectedClients.value, true, undefined);
    } else {
      result = await clientStore.getClientSummary(selectedClients.value, true, selectedYear.value);
    }

    if (!result || result.length === 0) {
      noDataMessage.value = 'No data available for post-pandemic in the selected year';
      return;
    } else {
      noDataMessage.value = ''; // reset the error message when there is valid data
    }

    

    chartData.value = {
      labels: result.map((c) => c.venue_name),
      datasets: [
        {
          label: 'Total FTE Days',
          data: result.map((c) => c.total_fte_days),
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        },
        {
          label: 'Average Marks per Day',
          data: result.map((c) => c.average_marks_per_day),
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }
      ]
    };
  }
  showChart.value = true;
  showLineChart.value = false;
};

const displayPrePandemicGraph = async () => {
  if (selectedClients.value.length) {
    let result;

    if (selectedYear.value == 'all') {
      result = await clientStore.getClientSummary(selectedClients.value, false, undefined);
    } else {
      result = await clientStore.getClientSummary(selectedClients.value, false, selectedYear.value);
    }

    if (!result || result.length === 0) {
      noDataMessage.value = 'No data available for pre-pandemic in the selected year';
      return;
    } else {
      noDataMessage.value = ''; // reset the error message when there is valid data
    }

    chartData.value = {
      labels: result.map((c) => c.venue_name),
      datasets: [
        {
          label: 'Total FTE Days',
          data: result.map((c) => c.total_fte_days),
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        },
        {
          label: 'Average Marks per Day',
          data: result.map((c) => c.average_marks_per_day),
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }
      ]
    };
  }
  showChart.value = true;
  showLineChart.value = false;
};

const displayLineChart = async () => {
  diagramType.value = 'lineChart';
  if (selectedClients.value.length) {
    try {
      let result;

      if (selectedYear.value == 'all') {
        result = await clientStore.getClientSummary(selectedClients.value, undefined, undefined);
      } else {
        result = await clientStore.getClientSummary(
          selectedClients.value,
          undefined,
          selectedYear.value
        );
      }
      const clientSummaries = result;

      const labels = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
      ];

      let datasets = [];

      clientSummaries.forEach((client, clientIndex) => {
        const fteDays = new Array(12).fill(0);
        const internDays = new Array(12).fill(0);
        const years = new Array(12).fill(null);

        client.monthly_working_days.forEach((month) => {
          const monthIndex = labels.indexOf(month.month);
          if (monthIndex !== -1) {
            fteDays[monthIndex] = month.total_fte_days;
            internDays[monthIndex] = month.total_intern_days;
            years[monthIndex] = month.year;
          }
        });

        // Add FTE dataset
        datasets.push({
          label: `${client.venue_name} - FTE Days`,
          data: fteDays,
          borderColor: getRandomColor(), 
          backgroundColor: 'transparent',
          fill: false,
          pointRadius: 5,
          pointHoverRadius: 7,
          years: years
        });

        // Add Intern dataset
        datasets.push({
          label: `${client.venue_name} - Intern Days`,
          data: internDays,
          borderColor: getRandomColor(), 
          backgroundColor: 'transparent',
          fill: false,
          pointRadius: 5,
          pointHoverRadius: 7,
          years: years
        });
      });

      lineChartData.value = {
        labels: labels,
        datasets: datasets
      };

      showChart.value = false;
      showLineChart.value = true;
    } catch (error) {
      console.error('There was an error fetching the client summary!', error);
    }
  }
};

watch([selectedYear, selectedClients, diagramType], () => {
  if (selectedClients.value.length > 0) {
    if (diagramType.value === 'postPandemicDiagram') {
      displayPostPandemicGraph();
    } else if (diagramType.value === 'prePandemicDiagram') {
      displayPrePandemicGraph();
    } else if (diagramType.value === 'lineChart') {
      displayLineChart();
    }
  }
});

const getRandomColor = () => {
  const r = Math.floor(Math.random() * 256);
  const g = Math.floor(Math.random() * 256);
  const b = Math.floor(Math.random() * 256);
  return `rgb(${r},${g},${b})`;
};

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        stepSize: 5,
        min: 0,
        max: 100
      }
    }
  },

  plugins: {
    tooltip: {
      callbacks: {
        label: function(context) {
          var label = context.dataset.label || '';
          
          if (label) {
            label += ': ';
          }
          if (context.parsed.y !== null) {
            label += context.parsed.y;
          }
          
          // Add year information here from the dataset
          const year = context.dataset.years[context.dataIndex];
          if (year) {
            label += ' (Year: ' + year + ')';
          }
          return label;
        }
      }
    }
  }
};
</script>

<style scoped>
.year-selector {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.year-selector label {
  margin-right: 10px;
  color: #333;
  font-size: 16px;
  font-weight: bold;
}

.year-selector select {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
}

.year-selector select:focus {
  border-color: #639843;
}
</style>
