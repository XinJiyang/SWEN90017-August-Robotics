import request from '..';

/**
 * Retrive the performance index for a specific job
 * @param id - job id
 * Sample response:
 * {
 *  "job": {
 *    "id": 19,
 *    "venue_name": "Museum",
 *    "region": "Afghanistan",
 *    "start_date": "2023-08-19",
 *    "end_date": "2023-08-29",
 *    "status": "NEW"
 *  },
 *  "client": {
 *    "id": 1,
 *    "venue_name": "Museum",
 *    "region": "Afghanistan",
 *    "email": "user1@gmail.com",
 *    "phone": "0432751552"
 *  },
 *  "performance": {
 *    "id": 5,
 *    "total_halls": 2,
 *    "total_shows": 4,
 *    "total_marks": 33,
 *    "marks_day": 3,
 *    "marks_fte_day": 11,
 *    "marks_person_day": 33,
 *    "marks_window": 10,
 *    "marks_hall": 16,
 *    "halls_day": 0.2,
 *    "fte": 1,
 *    "intern_helper": 0,
 *    "fte_engineer_days": 3,
 *    "intern_helper_days": 0,
 *    "fte_ratio": 1,
 *    "p_job": 19
 *  }
 * }
 */
export function getJobSummary(id: string): Promise<any> {
    return request.get({
      url: '/job/summary/' + id
    });
  }
  