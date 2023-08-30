import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PlaySocketService } from '../play-socket.service';
import { HttpClient } from '@angular/common/http';
import { Subscription, interval } from 'rxjs';
import { ApiService } from "../api.service";

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.scss']
})
export class PlayComponent implements OnInit, OnDestroy {
  socketUrl = '';
  typePlay = '';
  hashCodePlay = '';
  endGame = false;
  timer: number | undefined;

  winner: any;
  currentlyTurn: any;
  players: any[] = [];
  curr_tur: any;
  gameBoard: any[][] = [];

  timerSubscription!: Subscription;

  constructor(
    private socketService: PlaySocketService,
    private route: ActivatedRoute,
    private http: HttpClient,
    private api: ApiService
  ) {
    this.timerSubscription = interval(1000).subscribe(() => {
      if (!this.endGame){
       this.getTimerData();
      }
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
      const parsedMsg = JSON.parse(msg);
      if (parsedMsg['type'] === 'INFO') {
        this.players = parsedMsg['players'] !== null ? parsedMsg['players'] : this.players;
        this.curr_tur = parsedMsg['curr_tur'];
        this.gameBoard = parsedMsg['board'];
        this.currentlyTurn = parsedMsg['curr_player'];
        if (this.gameBoard) {
          this.generateGameBoard();
        }
      }
      if (parsedMsg['type'] === 'PLAY') {
        console.log(parsedMsg)
        this.endGame = true;
        // this.winner = parsedMsg['winner'];
      }
    });
  }

  ngOnDestroy(): void {
    this.timerSubscription.unsubscribe();
  }

  handleCellClick(Oy: number, Ox: number): void {
    if (this.gameBoard[Oy][Ox].value === ' ' && !this.endGame) {
      console.log(this.endGame)
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

  async getTimerData(): Promise<void> {
    try {
      const response: any = await this.api.getTimer(this.hashCodePlay, this.currentlyTurn['id']).toPromise();
      this.timer = response['remaining_time'];
    } catch (error) {
      console.log(error);
    }
  }
}
