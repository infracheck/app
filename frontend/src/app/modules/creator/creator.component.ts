import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-test-creator',
  templateUrl: './creator.component.html',
  styleUrls: ['./creator.component.scss']
})
export class CreatorComponent implements OnInit {

  constructor() {

    console.log("HEY TERE");
  }

  ngOnInit(): void {
  }

}
