import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
    name: 'testName'
})
/**
 * Transforms the id of tests into human readable name
 */
export class TestNamePipe implements PipeTransform {

    transform(name: string): string {
        return name.split('test_')[1].split('[')[0];
    }

}
