import {Component} from '@angular/core';
import {SearchSocketService} from "../search-socket.service";
import {ActivatedRoute, Router} from "@angular/router";
import {environment} from "../environments/environment";

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
    private route: ActivatedRoute,
    private router: Router
  ) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.typePlay = params['play_type'];
    });
    this.socketUrl = `${environment.SocketUrl}search-play/${this.typePlay}/`;
    this.socketService.connectToSocketServer(this.socketUrl);
    this.socketService.onMessageReceived((msg: any) => {
      const parsedMsg = JSON.parse(msg);
      const type_play = parsedMsg['type_play'];
      const play_hash_code = parsedMsg['play_hash_code'];
      if (parsedMsg["msg"] === "successful") {
         this.socketService.disconnectFromSocketServer();
         this.router.navigate(['/play', `${type_play}`, `${play_hash_code}`]);
      }
    });
  }

  ngOnDestroy(): void {
    this.socketService.disconnectFromSocketServer();
  }
}
