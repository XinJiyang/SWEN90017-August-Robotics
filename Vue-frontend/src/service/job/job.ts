import request from '..';
import type { IJob } from '@/types';

export function jobGetRequest(id: string) {
  return request.get({
    url: '/job/' + id
  });
}

/**
 * Retrieve jobs with provided number of jobs per page and the page number
 * @param itemsPerPage - number of jobs displayed per page
 * @param page - the page number for required jobs
 * @param attribute - the attribute for sorting
 * @param search - the keyword that user want to search
 * @param sortOrder - sorting order, 'ASC' means ascending, 'DES' means descending
 * Sample response:
 * {
 *    "total_num_pages": 4,
 *    "jobs":
 *      [
 *        {
 *            "id": 1,
 *            "venue_name": "Hamhurg",
 *            "region": "Germany",
 *            "start_date": "05/08/2023",
 *            "end_date": "10/08/2023",
 *            "status": "New Job",
 *        }
 *      ]
 * }
 */
export function jobGetListWithPaginationRequest(
  itemsPerPage: number = 10,
  page: number = 1,
  attribute: string = '',
  search: string = '',
  sortOrder: string = 'ASC'
) {
  let url = '/job/list/itemsPerPage=' + itemsPerPage + '&page=' + page;

  if (search !== '' && search !== null) {
    url += '&search=' + search;
  }

  if (attribute !== '') {
    url += '/sortBy=' + attribute + '&sortingOrder=' + sortOrder;
  }

  return request.get({
    url: url
  });
}

export function jobAddRequest(job: IJob) {
  return request.post({
    url: '/job/add',
    data: job
  });
}

export function jobEditRequest(id:string, job: IJob) {
  return request.patch({
    url: '/job/'+id,
    data: job
  });
}

export function jobDeleteRequest(id: string) {
  return request.delete({
    url: '/job/delete/ID=' + id
  });
}
