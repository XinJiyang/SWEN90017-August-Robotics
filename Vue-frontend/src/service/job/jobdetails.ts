import request from '..';
import type { IMarkingJob, JobStatus,  IHall} from '@/types';

/**
 * Retrieve detail of a specific job
 * @param id - job id
 * Sample response:
 * {
 *      "venue_name": "Hamburg",
 *      "start_date": "05/08/2023",
 *      "end_date": "05/08/2023",
 *      "status": "New Job",
 *      "markingJob":
 *          [
 *              {
 *                  "hall" : "A1",
 *                   "show" : "XXX",
 *                   "color" : "XXX",
 *                   "pre_corners" : 0,
 *                   "pre_numbers" : 0,
 *                   "pre_others" : 0,
 *                   "pre_area" : 0,
 *                   "fin_corners" : 0,
 *                   "fin_numbers" : 0,
 *                   "fin_others" : 0,
 *                   "fin_area" : 0
 *              }
 *          ]
 * }
 */
export function getJobDetail(id: string) {
  return request.get({
    url: '/job/detail/' + id
  });
}

/**
 * Update the basic information of a specific job, which includes start_date, end_date and status
 * @param id - job id
 * @param start_date - new start date for job
 * @param end_date - new end date for job
 * @param status - new status for job
 * Sample request:
 * {
 *      "start_date": "05/08/2023",
 *      "end_date": "05/08/2023",
 *      "status": "New Job"
 * }
 */
export function editBasicJobDetail(
  id: string,
  start_date: Date,
  end_date: Date,
  status: JobStatus
) {
  return request.patch({
    url: '/job/' + id,
    data: {
      start_date: start_date,
      end_date: end_date,
      status: status
    }
  });
}

/**
 * Update the list of marking jobs of a specific job
 * @param id - job id
 * @param markingJobs - list of marking jobs for job
 * Sample request:
 * {
 *      "markingJobs":
 *          [
 *              {
 *                  "hall" : "A1",
 *                   "show" : "XXX",
 *                   "color" : "XXX",
 *                   "pre_corners" : 0,
 *                   "pre_numbers" : 0,
 *                   "pre_others" : 0,
 *                   "pre_area" : 0,
 *                   "fin_corners" : 0,
 *                   "fin_numbers" : 0,
 *                   "fin_others" : 0,
 *                   "fin_area" : 0
 *              }
 *          ]
 * }
 */
export function editMarkingJobs(id: string, markingJobs: Array<IMarkingJob>) {
  return request.patch({
    url: '/job/' + id + '/markingJobs',
    data: markingJobs
    
  });
}

export function getJobDetailList(id: string) {
  return request.get({
    url: '/job/' + id + '/markingJobs'
  });
}

export function addNewJobDetail(jobId:string, job: IMarkingJob) {
  return request.post({
    url: 'job/'+jobId+'/markingJobs',
    data: job
  });
}
export function editJobDetail(job: IMarkingJob) {
  return request.patch({
    url: 'job/detail/id/edit',
    data: job
  });
}

export function deleteJobDetail(job: IMarkingJob) {
  return request.delete({
    url: 'job/detail/id/delete'
  });
}

export function getHall(id: string) {
  return request.get({
    url: 'client/hall/'+id
  });
}

export function getJobHalls(id: string) {
  return request.get({
    url: 'client/job/'+id+'/halls'
  });
}
