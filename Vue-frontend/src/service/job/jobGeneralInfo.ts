import request from '..';
import type { IEmployee } from '@/types';

/**
 * Retrive the general info for a specific job
 * @param id - job id
 * Sample response:
 * {
 *      "start_date": "11/02/2019",
 *      "end_date": "20/02/2019",
 *      "total_mark_day": 9,
 *      "employees":
 *          [
 *              {
 *                   "name": "Amy",
 *                   "type": "Helper",
 *                   "days": 4,
 *                   "hall": "A1"
 *               }
 *          ]
 * }
 */
export function getJobGeneralInfo(id: string): Promise<any> {
  return request.get({
    url: '/job/generalInfo/' + id
  });
}

/**
 * Update the employee part for a specific job
 * @param id - job id
 * @param employees - list of employees
 * Sample request:
 * {
 *      "employees":
 *          [
 *              {
 *                   "name": "Amy",
 *                   "type": "Helper",
 *                   "days": 4,
 *                   "hall": "A1"
 *               }
 *          ],
 *      "total_marking_day": 1
 * }
 */
export function editJobGeneralInfo(id: string, employees: Array<IEmployee>): Promise<any> {
  return request.post({
    url: '/job/generalInfo/' + id,
    data: {
      employees: employees
    }
  });
}

/**
 * Update the total marking day(s) for a specific job
 * @param id - job id
 * @param total_mark_day - total marking day(s)
 * Sample request:
 * {
 *      "total_marking_day": 1
 * }
 */
export function editTotalMarkingDay(id: string, total_mark_day: number): Promise<any> {
  return request.post({
    url: '/job/generalInfo/markingDays/' + id,
    data: {
      total_mark_day: total_mark_day
    }
  });
}
