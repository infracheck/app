import {ApiTestsResult} from './api';

export class TestSet {
  settings: {
    name: string;
    description: string;
    hosts: string[];
    user: string;
    target_os: string;
    password: string;
  };
  testset: Test[];


  constructor() {
    this.settings = {
      description: '',
      hosts: [],
      name: '',
      password: '',
      target_os: 'linux',
      user: ''
    };
    this.testset = [];
  }
}

export class Test {
  id: string;
  data: any;

  constructor(test: ApiTestsResult) {
    this.id = test.id;
    this.data = {};
  }
}
