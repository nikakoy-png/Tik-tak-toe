import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import {ApiService} from "../api.service";
import {UserDto} from "../models/User.dto";
import {CookieService} from "ngx-cookie-service";

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {
  constructor(private router: Router, private api: ApiService, private cookieService: CookieService) {}

  SelfUser!: UserDto | null;
  users!: UserDto[];

  ngOnInit() {
    this.api.getUserByToken(this.cookieService.get('token')).subscribe(data => { this.SelfUser = data });
    this.api.getUsersOrderByRating().subscribe(data => { this.users = data });
  }

  searchPlay(boardSize: string) {
    this.router.navigate(['/search-play', `${boardSize}`])
  }
}
