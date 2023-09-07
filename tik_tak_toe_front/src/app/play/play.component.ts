import {Component, OnInit, OnDestroy} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {PlaySocketService} from '../play-socket.service';
import {HttpClient} from '@angular/common/http';
import {Subscription, interval} from 'rxjs';
import {ApiService} from "../api.service";
import {environment} from "../environments/environment";
import {TimerSocketService} from "../timer-socket.service";

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.scss']
})
export class PlayComponent implements OnInit {
  socketUrl = '';
  socketUrlTimer = '';
  typePlay = '';
  hashCodePlay = '';
  endGame = false;
  timer: number | undefined;

  isRequest = false;

  winner: any | null;
  currentlyTurn: any;
  players: any[] = [];
  curr_tur: any;
  gameBoard: any[][] = [];


  constructor(
    private socketService: PlaySocketService,
    private socketServiceTimer: TimerSocketService,
    private route: ActivatedRoute,
    private router: Router,
  ) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.typePlay = params['play_type'];
      this.hashCodePlay = params['play_hash_code'];
    });

    this.socketUrl = `${environment.SocketUrl}play/${this.typePlay}/${this.hashCodePlay}/`;
    this.socketService.connectToSocketServer(this.socketUrl);

    this.socketUrlTimer = `${environment.SocketUrl}timer/${this.hashCodePlay}/`;
    this.socketServiceTimer.connectToSocketServer(this.socketUrlTimer);

    this.socketServiceTimer.onMessageReceived((msg: any) => {
      const parsedMsg = JSON.parse(msg);
      this.timer = parsedMsg['remaining_time'];
      if (this.timer === 0) {
        const message = {
          "type": 'timerEqualZero',
        };
        const messageString = JSON.stringify(message);
        this.socketService.sendMessage(messageString);
      }
    });

    this.socketService.onMessageReceived((msg: any) => {
      const parsedMsg = JSON.parse(msg);
      if (parsedMsg['type'] === 'INFO') {
        this.isRequest = false;
        this.players = parsedMsg['players'] !== null ? parsedMsg['players'] : this.players;
        this.curr_tur = parsedMsg['curr_tur'];
        this.gameBoard = parsedMsg['board'];
        this.currentlyTurn = parsedMsg['curr_player'];
        if (this.gameBoard) {
          this.generateGameBoard();
        }
      }
      if (parsedMsg['type'] === 'PLAY') {
        this.endGame = true;
        this.winner = parsedMsg['player'];
        this.socketServiceTimer.disconnectFromSocketServer();
        this.handleGameEnd(this.winner);
        this.socketService.disconnectFromSocketServer();
      }
    });
  }

  handleCellClick(Oy: number, Ox: number): void {
    console.log(this.endGame)
    if (this.gameBoard[Oy][Ox].value === ' ' && !this.endGame && !this.isRequest) {
      this.isRequest = true;
      const message = {
        "type": 'turn',
        "Oy": Oy,
        "Ox": Ox,
        "curr_tur": this.curr_tur,
      };
      const messageString = JSON.stringify(message);
      this.socketService.sendMessage(messageString);
    }
  }

  handleGameEnd(winner: any): void {
    console.log('Game ended with winner:', winner);
    this.socketServiceTimer.disconnectFromSocketServer();
    this.socketService.disconnectFromSocketServer();

    setTimeout(() => {
      this.router.navigate(['main']);
    }, 5000);
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
}
