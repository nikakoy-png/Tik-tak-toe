import {Component} from '@angular/core';
import {SearchSocketService} from "../search-socket.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent {
  socketUrl = '';
  typePlay = '';

  constructor(
    private socketService: SearchSocketService,
    private route: ActivatedRoute
  ) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.typePlay = params['play_type'];
    });
    this.socketUrl = `ws://localhost:8000/ws/search-play/${this.typePlay}/`;
    this.socketService.connectToSocketServer(this.socketUrl);
    this.socketService.onMessageReceived((msg: string) => {
      console.log(msg);
    });
  }

  ngOnDestroy(): void {
    this.socketService.disconnectFromSocketServer();
  }
}
