import {Component, Input, OnChanges, SimpleChanges} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {PlaySocketService} from "../play-socket.service";

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.scss']
})
export class PlayComponent {
  socketUrl = '';
  typePlay = '';
  hashCodePlay = '';

  winner!: any;

  currentlyTurn!: any;

  players: any[] = [];

  curr_tur!: any;

  gameBoard!: any[][];

  constructor(
    private socketService: PlaySocketService,
    private route: ActivatedRoute,
  ) {
  }


  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.typePlay = params['play_type'];
      this.hashCodePlay = params['play_hash_code'];
    });
    this.socketUrl = `ws://localhost:8000/ws/play/${this.typePlay}/${this.hashCodePlay}/`;
    this.socketService.connectToSocketServer(this.socketUrl);
    this.socketService.onMessageReceived((msg: any) => {
      console.log(msg)
      const parsedMsg = JSON.parse(msg);
      console.log(parsedMsg);
      // if (parsedMsg['type'] === 'PLAY') {
      //   this.winner = parsedMsg['player'];
      // }
      this.players = parsedMsg['players'] !== null ? parsedMsg['players'] : this.players
      this.curr_tur = parsedMsg['curr_tur']
      this.gameBoard = parsedMsg['board'];
      this.currentlyTurn = parsedMsg['curr_player']['username']
      if (this.gameBoard) {
        this.generateGameBoard();
      }
    });
  }

  handleCellClick(Oy: number, Ox: number): void {
    if (this.gameBoard[Oy][Ox].value === ' ') {
      // this.gameBoard[Oy][Ox].value = this.curr_tur === 1 ? 'X' : 'O';
      const message = {
      "Oy": Oy,
      "Ox": Ox,
      "curr_tur": this.curr_tur,
    }
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

}
