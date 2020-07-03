export interface ApiModule {
    id: string;
    documentation: string;
    fields: any;
}

export interface ApiPlugin {
    data: any;
    documentation: string;
    id: string;
    modules: ApiModule[];
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
