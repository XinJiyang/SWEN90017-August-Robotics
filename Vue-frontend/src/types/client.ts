import type { Country } from "@/utils/country";

// What if venue in different regions? Additional attributes like region and id may be needed.
export interface IVenue {
  hall: string;
  area: number;
}

// Need to be refine later
export interface IClient {
  id: string;
  venue_name: string;
  region: Country | undefined;
  email: string;
  phone: string;
  halls: Array<IVenue>;
}