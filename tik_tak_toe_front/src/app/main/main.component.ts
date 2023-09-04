import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {ApiService} from "../api.service";
import {UserDto} from "../models/User.dto";

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {
  constructor(private router: Router, private api: ApiService) {}

  user!: UserDto;

  ngOnInit() {
    this.api.getUserById(1).subscribe(data => { this.user = data; });
  }

  searchPlay(boardSize: string) {
    this.router.navigate(['/search-play', `${boardSize}`])
  }
}
