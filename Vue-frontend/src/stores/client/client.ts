import {
  clientAddRequest,
  clientDeleteRequest,
  clientEditRequest,
  clientGetHallListRequest,
  clientGetListWithPaginationRequest,
  clientGetNameListRequest,
  clientGetRequest,
  clientGetVenuesSummaryRequest
} from '@/service/client/client';
import type { IClient } from '@/types';
import type { AxiosError } from 'axios';
import { defineStore } from 'pinia';

interface IClientStore {
  clients: Array<IClient>;
  itemsPerPage: number;
  totalPages: number;
  page: number;
  sortBy: string;
  sortOrder: boolean; // true indicates ascending, false for descending
  search: string;
}

const useClientStore = defineStore('client', {
  state: (): IClientStore => ({
    clients: [],
    itemsPerPage: 10,
    totalPages: 1,
    page: 1,
    sortBy: '',
    sortOrder: true,
    search: ''
  }),
  actions: {
    async getClient(id: string): Promise<undefined | IClient> {
      // connect to backend
      try {
        const result = await clientGetRequest(id);

        return result.client;
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Cannot not find requested client');
        }
        return this.$state.clients.find((client) => client.id === id);
      }
    },
    async getClientSummary(venue_names: Array<string>, postPandemic: boolean, year: number): Promise<undefined | IClient> {
      // connect to backend
      const result = await clientGetVenuesSummaryRequest(venue_names, postPandemic,  year);

      return result.clients;
    },
    async getClientListWithPagination(): Promise<Array<IClient>> {
      try {
        let result;
        if (!this.$state.sortOrder) {
          result = await clientGetListWithPaginationRequest(
            this.$state.itemsPerPage,
            this.$state.page,
            this.$state.sortBy,
            this.$state.search,
            'DSC'
          );
        } else {
          result = await clientGetListWithPaginationRequest(
            this.$state.itemsPerPage,
            this.$state.page,
            this.$state.sortBy,
            this.$state.search
          );
        }

        this.$state.clients = result.clients;
        this.$state.totalPages = result.total_num_pages;

        return result.clients;
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Fail to load job list');
        }
        // simulate backend pagination
        this.$state.totalPages = Math.ceil(this.$state.clients.length / this.$state.itemsPerPage);
        const firstItem = (this.$state.page - 1) * this.$state.itemsPerPage;

        // change order
        if (this.$state.sortBy !== '' && !this.$state.sortOrder) {
          return this.$state.clients
            .slice(firstItem, firstItem + this.$state.itemsPerPage)
            .toReversed();
        }
        return this.$state.clients.slice(firstItem, firstItem + this.$state.itemsPerPage);
      }
    },
    async getClientNameList(): Promise<Array<any>> {
      // connect to backend
      try {
        const result = await clientGetNameListRequest();

        return result.clients.map((client) => client.venue_name);
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Fail to load client name list');
        }
        return Array.from(this.$state.clients, (client) => client.venue_name);
      }
    },
    async getHallList(id: string): Promise<Array<String>> {
      // connect to backend
      try {
        const result = await clientGetHallListRequest(id);

        return result.halls;
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Fail to load client list');
        }
        const client: IClient | undefined = this.$state.clients.find((client) => client.id === id);
        if (client !== undefined) {
          return Array.from(client?.halls, (hall) => hall.hall);
        } else {
          return [];
        }
      }
    },
    async addClient(client: IClient): Promise<void> {
      // connect to backend
      try {
        const result = await clientAddRequest(client);
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Fail to create new client');
        }
      }
    },
    async editClient(id: string, client: IClient): Promise<void> {
      // connect to backend
      try {
        const result = await clientEditRequest(client);
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Fail to modify client info');
        }
      }
    },
    async deleteClient(id: string): Promise<void> {
      // connect to backend
      try {
        const result = await clientDeleteRequest(id);
      } catch (error) {
        if ((error as AxiosError).response?.status === 400) {
          alert('Fail to delete client');
        }
      }
    }
  }
});

export default useClientStore;
