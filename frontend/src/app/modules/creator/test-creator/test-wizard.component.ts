import {Component, EventEmitter, Input, Output, ViewChild} from '@angular/core';
import {ClrWizard} from "@clr/angular";
import {ApiInputData, ApiPlugin} from "../../../definitions/api";
import {HttpService} from "../../../services/http.service";

@Component({
    selector: 'app-test-wizard',
    templateUrl: './test-wizard.component.html',
    styleUrls: ['./test-wizard.component.scss']
})
export class TestWizard {
    @ViewChild("wizard") wizard: ClrWizard;
    @Input() show: boolean;
    @Input() plugins: ApiPlugin[];
    @Output() showChange: EventEmitter<boolean> = new EventEmitter<boolean>();
    data: ApiInputData = {
        name: "Hello World",
        description: "Hello",
        plugins: [
            {
                modules: [],
                data: {},
                id: "testinfra"
            }
        ]
    }
    chosenPlugins: any[] = []

    constructor(private http: HttpService) {
    }

    changeVisibility() {
        this.show = !(this.show);
        this.showChange.emit(this.show);
    }

    selectionChanged() {
        this.chosenPlugins.forEach((plugin: ApiPlugin) => {
            const plugin_added = Boolean(this.data.plugins.find((used_plugin: ApiPlugin) => used_plugin.id === plugin.id))

            if (!plugin_added) {
                this.data.plugins.push({
                    "modules": [],
                    "data": {},
                    "id": plugin.id,
                })
            }
        })
        // Remove unchecked plugins
        this.data.plugins = this.data.plugins.filter(plugin => Boolean(this.chosenPlugins.find(pl => pl.id === plugin.id)))
    }

    getPluginData(pluginId: string) {
        return this.data.plugins.find(plugin => plugin.id === pluginId)
    }

    finishWizard() {
        console.log(this.data);
        this.http.launchTest(this.data).subscribe(res => console.log(res))
    }
}
