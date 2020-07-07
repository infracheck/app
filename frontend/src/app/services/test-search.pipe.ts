import {Pipe, PipeTransform} from '@angular/core';
import {ApiPlugin} from '../definitions/api';

@Pipe({
    name: 'testSearch'
})
export class TestSearchPipe implements PipeTransform {

    transform(tests: ApiPlugin[], search: string): any {
        search = search.toLowerCase();
        return tests.filter(test =>
            test.id.toLowerCase().includes(search)
        );
    }

}
