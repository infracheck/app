export interface ApiModule {
    id: string
    documentation: string
    fields: any
    code: string
}

export interface ApiPlugin {
    data: any
    documentation: string
    id: string
    modules: ApiModule[]
}

export interface ApiHistory {
    id: string
    date: string
    name: string
    description: string
    succeeded: number
    failures: number
    errors: number
    total: number
    message: string
    data: any
}

export enum InputTypes {
    Text = "string",
    Password = "password",
    Number = "number",
    Boolean = "boolean",
    TextList = "Array<string>",
    NumberList = "Array<number>",
}

export interface ApiInputPluginData {
    id: string
    data: any
    modules: ApiInputModuleData[]
}

export interface ApiInputModuleData {
    id: string
    fields: any
}

export interface ApiInputData {
    name: string
    description: string,
    plugins: ApiInputPluginData[]
}
