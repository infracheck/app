import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {PluginResolver} from './resolver/test-resolver.service';
import {LatestTestsResolverService} from './resolver/latest-tests-resolver.service';
import {PresetResolverService} from './resolver/preset-resolver.service';


const routes: Routes = [
  {
    path: 'start',
    loadChildren: () => import('./modules/start/start.module').then(m => m.StartModule),
    resolve: {
      presets: PresetResolverService,
      tests: PluginResolver
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
    loadChildren: () => import('./modules/results/results.module').then(m => m.ResultsModule),
    resolve: {
      latest: LatestTestsResolverService
    }
  },
  {
    path: 'results/:id',
    loadChildren: () => import('./modules/results/results.module').then(m => m.ResultsModule),
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
