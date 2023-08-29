import {Component, OnInit, OnDestroy} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {PlaySocketService} from '../play-socket.service';
import {HttpClient} from '@angular/common/http';
import {Subscription, interval} from 'rxjs';
import {ApiService} from "../api.service";

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.scss']
})
export class PlayComponent implements OnInit, OnDestroy {
  socketUrl = '';
  typePlay = '';
  hashCodePlay = '';
  isRequesting = false;

  endGame = false

  timer!: '';
  winner!: any;
  currentlyTurn!: any;
  players: any[] = [];
  curr_tur!: any;
  gameBoard!: any[][];


  timerSubscription!: Subscription;

  constructor(
    private socketService: PlaySocketService,
    private route: ActivatedRoute,
    private http: HttpClient,
    private api: ApiService
  ) {
    this.timerSubscription = interval(1000).subscribe(() => {
      this.getTimerData();
    });
  }

  ngOnInit(): void {
    if (!this.endGame) {
      console.log(1);
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
          this.winner = parsedMsg['winner']['username'];
          this.endGame = true;
        }
      });
    } else {

    }
  }

  ngOnDestroy(): void {
    this.timerSubscription.unsubscribe();
  }

  handleCellClick(Oy: number, Ox: number): void {
    if (!this.isRequesting && this.gameBoard[Oy][Ox].value === ' ' || !this.endGame) {
      this.isRequesting = true;

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
    await this.api.getTimer(this.hashCodePlay, this.currentlyTurn['id']).subscribe(
      (response) => {
        this.timer = response['remaining_time'];
        this.isRequesting = false;
      },
      (error) => {
        console.log(error);
        this.isRequesting = false;
      }
    );
  }
}
