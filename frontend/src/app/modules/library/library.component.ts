import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {HttpService} from '../../services/http.service';
import {Preset} from '../../definitions/Preset';

@Component({
  selector: 'app-library',
  templateUrl: './library.component.html',
  styleUrls: ['./library.component.scss']
})
export class LibraryComponent implements OnInit {
  selectedPreset: Preset;
  presets: Preset[];
  edit = false;
  success = 0; // 0: nothing, 1: saved successfully, 2: deleted successfully, 3: error

  constructor(private acr: ActivatedRoute, private http: HttpService) {
    this.acr.data.subscribe(data => {
      this.presets = data.presets;
      this.selectedPreset = this.presets[0];
    });
  }

  ngOnInit() {
  }

  deletePreset(preset: Preset) {
    this.http.deletePreset(preset._id.$oid).subscribe(
      () => {
        this.success = 2;
        this.reloadPresets();
      },
      err => {
        this.success = 3;
      });
  }

  private reloadPresets() {
    this.selectedPreset = null;
    this.http.getAllPresets().subscribe(presets => this.presets = presets);
  }

  savePreset(preset: Preset) {
    this.http.savePreset(preset).subscribe(
      () => {
        this.reloadPresets();
        this.success = 1;
      },
      err => {
        this.success = 3;
      });
  }

  createPreset() {
    this.selectedPreset = {
      id: '',
      description: '',
      testset: []
    };
    this.edit = true;
  }
}
