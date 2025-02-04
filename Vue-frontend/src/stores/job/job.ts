import {
  jobAddRequest,
  jobDeleteRequest,
  jobEditRequest,
  jobGetRequest,
  jobGetListWithPaginationRequest
} from '@/service/job/job';
import type { IJob } from '@/types';
import type { AxiosError } from 'axios';
import { defineStore } from 'pinia';

// define job store structure
interface IJobStore {
  jobs: Array<IJob>;
  itemsPerPage: number;
  totalPages: number;
  page: number;
  sortBy: string;
  sortOrder: boolean; // true indicates ascending, false for descending
  search: string;
}

const useJobStore = defineStore('job', {
  state: (): IJobStore => ({
    // set default values
    jobs: [],
    itemsPerPage: 8,
    totalPages: 1,
    page: 1,
    sortBy: '',
    sortOrder: true,
    search: ''
  }),
  actions: {
    async getJob(id: string): Promise<undefined | IJob> {
      // connect to backend
      try {
        const result = await jobGetRequest(id);

        return result;
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Cannot not find requested client');
        }
        return this.$state.jobs.find((job) => job.id === id);
      }
    },
    async getJobListWithPagination(): Promise<Array<IJob>> {
      try {
        let result;
        if (!this.$state.sortOrder) {
          result = await jobGetListWithPaginationRequest(
            this.$state.itemsPerPage,
            this.$state.page,
            this.$state.sortBy,
            this.$state.search,
            'DSC'
          );
        } else {
          result = await jobGetListWithPaginationRequest(
            this.$state.itemsPerPage,
            this.$state.page,
            this.$state.sortBy,
            this.$state.search
          );
        }

        this.$state.jobs = result.jobs;
        this.$state.totalPages = result.total_num_pages;

        return result.jobs;
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Fail to load job list');
        }
        // simulate backend pagination
        this.$state.totalPages = Math.ceil(this.$state.jobs.length / this.$state.itemsPerPage);
        const firstItem = (this.$state.page - 1) * this.$state.itemsPerPage;

        if (this.$state.sortBy !== '' && !this.$state.sortOrder) {
          return this.$state.jobs
            .slice(firstItem, firstItem + this.$state.itemsPerPage)
            .toReversed();
        }
        return this.$state.jobs.slice(firstItem, firstItem + this.$state.itemsPerPage);
      }
    },
    async addJob(job: IJob) {
      // connect to backend
      try {
        const result = await jobAddRequest(job);

        this.$state.jobs.push(job);
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Fail to add new job');
        }
      }
    },
    async editJob(id:string, job: IJob) {
      // connect to backend
      try {
        const result = await jobEditRequest(id, job);

        const index = this.$state.jobs.findIndex((j) => j.id === job.id);
        this.$state.jobs.splice(index, 1, job);
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Fail to modify job info');
        }
      }
    },
    async deleteJob(id: string) {
      // connect to backend
      try {
        const result = await jobDeleteRequest(id);

        const index = this.$state.jobs.findIndex((job) => job.id === id);
        this.$state.jobs.splice(index, 1);
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Fail to delete job');
        }
      }
    }
  }
});

export default useJobStore;
