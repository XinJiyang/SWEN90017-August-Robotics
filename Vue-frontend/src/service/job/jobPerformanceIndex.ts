import request from '..';

/**
 * Retrive the performance index for a specific job
 * @param id - job id
 * Sample response:
 * {
 *      "start_date": "11/02/2019",
 *      "end_date": "20/02/2019",
 *      "total_marks": 2912,
 *      "performance":
 *           {
 *            "marks_day" : 0,
 *            "marks_fte_day" : 0,
 *            "marks_person_day" : 0,
 *            "fte_ratio" : 0.0%,
 *            "halls_day" : 0,
 *            "fte" : 0,
 *            "intern_helper" : 0,
 *            "intern_helper_days" : 0,
 *            "fte_engineer_days" : 0
 *            }
 * }
 */
export function getJobPerformanceIndex(id: string): Promise<any> {
  return request.get({
    url: '/job/' + id + '/performance'
  });
}
