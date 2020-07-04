import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {PluginResolver} from './resolver/test-resolver.service';
import {LatestTestsResolverService} from './resolver/latest-tests-resolver.service';


const routes: Routes = [
    {
        path: 'start',
        loadChildren: () => import('./modules/creator/creator.module').then(m => m.CreatorModule),
        resolve: {
        }
    },
    {
        path: 'docs',
        loadChildren: () => import('./modules/documentation/documentation.module').then(m => m.DocumentationModule),
        resolve: {
            tests: PluginResolver
        }
    },
    {
        path: 'results',
        loadChildren: () => import('./modules/history/results.module').then(m => m.ResultsModule),
        resolve: {
            latest: LatestTestsResolverService
        }
    },
    {
        path: 'results/:id',
        loadChildren: () => import('./modules/history/results.module').then(m => m.ResultsModule),
        resolve: {
            latest: LatestTestsResolverService
        }
    },
    {
        path: '',
        redirectTo: '/start',
        pathMatch: 'full'
    }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule {
}
