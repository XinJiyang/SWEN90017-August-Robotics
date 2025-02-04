import type { Country } from '@/utils/country';
import type { IClient } from './client';

export enum JobStatus {
  NEW = 'NEW',
  ONGOING = 'On Going',
  CANCEL = 'Cancel',
  FINISH = 'Finished'
}

export interface IPerfromance {
  total_halls: number;
  total_shows: number;
  total_marks: number;
  marks_day: number;
  marks_fte_day: number;
  marks_person_day: number;
  fte_ratio: number;
  halls_day: number;
  fte: number;
  intern_helper: number;
  intern_helper_days: number;
  fte_engineer_days: number;
}

export interface ISummary {
  job?: IJobSummary;
  client?: IClient;
  performance?: IPerfromance;
}

export interface IEmployee {
  name: string;
  // unsure about what are possible types so keep it as string for now
  type: string;
  days: Number;
  hall: string;
}

export interface IMarkingJob {
  id: string;
  mj_hall: IHall;
  show: string;
  colour: string;
  pre_corners: Number | null;
  pre_numbers: Number | null;
  pre_others: Number | null;
  pre_area: Number | null;
  fin_corners: Number | null;
  fin_numbers: Number | null;
  fin_others: Number | null;
  fin_area: Number | null;
}

export interface IJob {
  id?: string;
  venue_name: string;
  region?: Country;
  show?: string;
  start_date?: Date;
  end_date?: Date;
  status: JobStatus;
  markingJob: Array<IMarkingJob>;
  performance?: IPerfromance;
  employees: Array<IEmployee>;
}

export interface IJobSummary {
  id?: string;
  venue_name: string;
  region?: Country;
  start_date?: Date;
  end_date?: Date;
  status: JobStatus;
}

export interface IHall {
  id: string;
  hall: string;
  area: Number;
  h_client_id: Number;
}

export const jstatus: Array<JobStatus> = [
  JobStatus.NEW,
  JobStatus.ONGOING,
  JobStatus.CANCEL,
  JobStatus.FINISH
];
