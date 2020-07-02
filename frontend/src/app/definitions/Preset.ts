import {Test} from './TestSet';

export interface Preset {
  _id?: { $oid: string }; // Mongo DB ID
  id: string; // name
  description: string;
  testset: Test[];
}
