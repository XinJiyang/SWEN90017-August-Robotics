import request from '..';
import type { IClient } from '@/types';

export function clientGetRequest(id: string) {
  return request.get({
    url: '/client/get/ID=' + id
  });
}

// return all venue names
export function clientGetNameListRequest() {
  return request.get({
    url: '/client/list/name'
  });
}

export function clientGetVenuesSummaryRequest(
  venue_names: Array<string>,
  postPandemic: boolean,
  year: number
) {
  return request.post({
    url: '/client/summary',
    data: {
      venue_names: venue_names,
      postPandemic: postPandemic,
      year: year
    }
  });
}

// return all halls for a specific client
export function clientGetHallListRequest(id: string) {
  return request.get({
    url: '/client/list/hall/ID=' + id
  });
}

/**
 * Retrieve clients with provided number of jobs per page and the page number
 * @param itemsPerPage - number of jobs displayed per page
 * @param page - the page number for required jobs
 * @param attribute - the attribute for sorting
 * @param search - the keyword that user want to search
 * @param sortOrder - sorting order, 'ASC' means ascending, 'DES' means descending
 * Sample response:
 * {
 *    "total_num_pages": 4,
 *    "clients":
 *      [
 *        {
 *         "venue_name" : "Melbourne Museum",
 *         "region" : "Australia",
 *         "email" : "XXX@XXX.XXX",
 *         "phone" : "00000000000"
 *         }
 *      ]
 * }
 */
export function clientGetListWithPaginationRequest(
  itemsPerPage: number = 10,
  page: number = 1,
  attribute: string = '',
  search: string = '',
  sortOrder: string = 'ASC'
) {
  let url = '/client/list/itemsPerPage=' + itemsPerPage + '&page=' + page;

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

export function clientAddRequest(client: IClient) {
  return request.post({
    url: '/client/add',
    data: client
  });
}

export function clientEditRequest(client: IClient) {
  return request.patch({
    url: '/client/update',
    data: client
  });
}

export function clientDeleteRequest(id: string) {
  return request.delete({
    url: '/client/delete/ID=' + id
  });
}
