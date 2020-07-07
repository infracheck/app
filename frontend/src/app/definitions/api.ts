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

export class InputTypes {
    Text = "string";
    Number = "number";
    Boolean = "boolean";
    TextList = "Array<string>";
    NumberList = "Array<number>";
}
