import { Component } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {PlaySocketService} from "../play-socket.service";

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.css']
})
export class PlayComponent {
  socketUrl = '';
  typePlay = '';
  hashCodePlay = '';

  constructor(
    private socketService: PlaySocketService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.typePlay = params['play_type'];
      this.hashCodePlay = params['play_hash_code'];
    });
    this.socketUrl = `ws://localhost:8000/ws/play/${this.typePlay}/${this.hashCodePlay}/`;
    this.socketService.connectToSocketServer(this.socketUrl);
    this.socketService.onMessageReceived((msg: string) => {
      console.log(msg);
    });
  }
}
