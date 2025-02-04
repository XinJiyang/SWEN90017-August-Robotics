import {
    getJobDetailList,
    addNewJobDetail,
    getHall,
    editMarkingJobs,
    getJobHalls,
} from '@/service/job/jobdetails'
import type { AxiosError } from 'axios';
import { defineStore } from 'pinia';
import type { IMarkingJob } from '@/types';

const sampleJobDetails: Array<IMarkingJob> = [
    {
        id: '1',
            mj_hall: 'Hall-A1',
            show: 'NT23',
            color: 'Blue',
            pre_corners: 300,
            pre_numbers: 300,
            pre_others: 200,
            pre_area: 2000^2,
            fin_corners: null,
            fin_numbers: null,
            fin_others: null,
            fin_area: null,
    },
    {
        id: '2',
            mj_hall: 'Hall-A1',
            show: 'OM23',
            color: 'Green',
            pre_corners: 300,
            pre_numbers: 300,
            pre_others: 200,
            pre_area: 2000^2,
            fin_corners: null,
            fin_numbers: null,
            fin_others: null,
            fin_area: null,
    }
]

interface IJobDetailStore {
    jobdetails: Array<IMarkingJob>;
}

const useJobDetailStore = defineStore('jobdetails', {
    state: (): IJobDetailStore => ({
        jobdetails: sampleJobDetails
      }),
    actions: {
        async getJobDetailList(id:string): Promise<Array<IMarkingJob>> {
            // connect to backend
            try {
              //return this.$state.jobdetails;
              const result = await getJobDetailList(id);
      
              this.$state.jobdetails = result.jobdetails;
      
              return result;
            } catch (error) {
              if ((error as AxiosError).response?.status === 400) {
                alert('Fail to load job list');
              }
              return this.$state.jobdetails;
            }
        },
        async addNewJobDetail(id:string, markingJob:IMarkingJob) {
          try {
            const result = await addNewJobDetail(id, markingJob);
    
            this.$state.jobdetails.push(markingJob);
          } catch (error) {
            if ((error as AxiosError).response?.status === 400) {
              alert('Fail to add new marking job');
            }
          }
        },
        async getHall(id:Number) {
          try {
            const result = await getHall(id.toString());
            //this.$state.jobdetails = result.jobdetails;
      
            return result;
          } catch (error) {
            if ((error as AxiosError).response?.status === 400) {
              alert('Fail to get Hall Name');
            }
          }
        },
        async editMarkingJobs(id:string, markingJobs:Array<IMarkingJob>) {
          try {
            const result = await editMarkingJobs(id, markingJobs);
    
            //this.$state.jobdetails.push(markingJob);
          } catch (error) {
            if ((error as AxiosError).response?.status === 400) {
              alert('Fail to edit marking jobs');
            }
          }
        },
        async getJobHalls(id: string){
          try{
            const result = await getJobHalls(id);
            return result;
          } catch (error) {
            if ((error as AxiosError).response?.status === 400) {
              alert('Failed to get job halls');
            }
          }
        }
    }
});

export default useJobDetailStore;