import axios, { AxiosInstance } from 'axios';
import { API_BASE_URL } from '.';

export class FlightService {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: API_BASE_URL,
    });
  }

  async getFlightPrices(
    origin: string,
    destination: string,
    date: string,
    passengers: number = 1,
    max_results: number = 1,
    no_cache: boolean = false
  ): Promise<any> {
    try {
      const formattedDate = new Date(date).toISOString().split('T')[0];

      const response = await this.axiosInstance.get('/api/flights/price', {
        params: {
          origin,
          destination,
          date: formattedDate,
          passengers,
          max_results,
          no_cache,
        },
      });
  
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(`API request failed: ${(error as Error).message}`);
      } else {
        throw new Error('An unexpected error occurred');
      }
    }
  }
  
}
