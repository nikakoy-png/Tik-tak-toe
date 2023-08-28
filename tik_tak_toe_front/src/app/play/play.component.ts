import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PlaySocketService } from '../play-socket.service';
import { HttpClient } from '@angular/common/http';
import { Subscription, interval } from 'rxjs';

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.scss']
})
export class PlayComponent implements OnInit, OnDestroy {
  socketUrl = '';
  typePlay = '';
  hashCodePlay = '';

  winner!: any;
  currentlyTurn!: any;
  players: any[] = [];
  curr_tur!: any;
  gameBoard!: any[][];

  private timerSubscription: Subscription;

  constructor(
    private socketService: PlaySocketService,
    private route: ActivatedRoute,
    private http: HttpClient
  ) {
    this.timerSubscription = interval(1000).subscribe(() => {
      this.getTimerData();
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.typePlay = params['play_type'];
      this.hashCodePlay = params['play_hash_code'];
    });
    this.socketUrl = `ws://localhost:8000/ws/play/${this.typePlay}/${this.hashCodePlay}/`;
    this.socketService.connectToSocketServer(this.socketUrl);
    this.socketService.onMessageReceived((msg: any) => {
      console.log(msg);
      const parsedMsg = JSON.parse(msg);
      console.log(parsedMsg);
      this.players = parsedMsg['players'] !== null ? parsedMsg['players'] : this.players;
      this.curr_tur = parsedMsg['curr_tur'];
      this.gameBoard = parsedMsg['board'];
      this.currentlyTurn = parsedMsg['curr_player']['username'];
      if (this.gameBoard) {
        this.generateGameBoard();
      }
    });
  }

  ngOnDestroy(): void {
    this.timerSubscription.unsubscribe();
  }

  handleCellClick(Oy: number, Ox: number): void {
    if (this.gameBoard[Oy][Ox].value === ' ') {
      const message = {
        "Oy": Oy,
        "Ox": Ox,
        "curr_tur": this.curr_tur,
      };
      const messageString = JSON.stringify(message);
      this.socketService.sendMessage(messageString);
    }
  }

  generateGameBoard(): void {
    this.gameBoard = this.gameBoard.map((row, rowIndex) => {
      return row.map((cellValue, colIndex) => ({
        value: cellValue === 0 ? ' ' : (cellValue === 1 ? 'X' : 'O'),
        rowIndex,
        colIndex
      }));
    });
  }

  getTimerData(): void {
    const apiUrl = `http://localhost:8000/api/get_timer_turn/`;
    const requestData = {
      play_hash_code: this.hashCodePlay
    };
    this.http.get<any>(apiUrl, { params: requestData }).subscribe(
      response => {
        console.log(response);
      },
      error => {
        console.error(error);
      }
    );
  }
}
