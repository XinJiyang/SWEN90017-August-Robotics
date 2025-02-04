<template>
  <v-table>
    <thead>
      <tr>
        <th class="text-left">Start Date: &nbsp;{{ start_date }}</th>
        <th class="text-left">End Date: &nbsp;{{ end_date }}</th>
        <th class="text-left">Total Marks: &nbsp;{{ data.total_marks }}</th>
      </tr>
    </thead>
  </v-table>

  <v-card-title>
    <h4 class="text-center">Data Statistics</h4>
  </v-card-title>
  <v-card-text>
    <v-table>
      <template v-slot:default>
        <tbody>
          <tr>
            <td class="text-left">Statistics</td>
            <td class="text-right">Results</td>
          </tr>
          <tr>
            <td class="text-left">Marks/Day</td>
            <td class="text-right">{{ data.marks_day }}</td>
          </tr>
          <tr>
            <td class="text-left">Marks/FTE/Day</td>
            <td class="text-right">{{ data.marks_fte_day }}</td>
          </tr>
          <tr>
            <td class="text-left">Marks/Person/Day</td>
            <td class="text-right">{{ data.marks_person_day }}</td>
          </tr>
          <tr>
            <td class="text-left">FTE Ratio</td>
            <td class="text-right">{{ data.fte_ratio }}</td>
          </tr>
          <tr>
            <td class="text-left">Halls/Day</td>
            <td class="text-right">{{ data.halls_day }}</td>
          </tr>
          <tr>
            <td class="text-left">#FTE</td>
            <td class="text-right">{{ data.fte }}</td>
          </tr>
          <tr>
            <td class="text-left">#Intern/Helper</td>
            <td class="text-right">{{ data.intern_helper }}</td>
          </tr>
          <tr>
            <td class="text-left">#FTE Engineer Days</td>
            <td class="text-right">{{ data.fte_engineer_days }}</td>
          </tr>
          <tr>
            <td class="text-left">#Intern/Helper Days</td>
            <td class="text-right">{{ data.intern_helper_days }}</td>
          </tr>
        </tbody>
      </template>
    </v-table>
  </v-card-text>
</template>

<script setup lang="ts">
import type { IPerfromance } from '@/types';

const props = defineProps<{ data: IPerfromance; start_date: Date; end_date: Date }>();
</script>
