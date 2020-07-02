export interface ApiTestsResult {
  id: string;
  description: string;
  code: string;
  directory: string;
  input: any;
}

export interface ApiLatestTestsResult {
  date: string;
  description: string;
  errors: number;
  failures: number;
  id: string;
  jsonOutput: string;
  name: string;
  skipped: number;
  tests: number;
  processing_time: number;
  testset: {
    name: string,
    host: string,
    success: boolean,
    time: number,
    message?: string,
  }[];
  time: number;
}
