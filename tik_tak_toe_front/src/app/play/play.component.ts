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
      const parsedMsg = JSON.parse(msg);
      this.curr_tur = parsedMsg['curr_tur']
      this.gameBoard = parsedMsg['board'];
      this.generateGameBoard();
    });
  }

  handleCellClick(Oy: number, Ox: number): void {
    const message = {
      "Oy": Oy,
      "Ox": Ox,
      "curr_tur": this.curr_tur,
    }
    const messageString = JSON.stringify(message);
    this.socketService.sendMessage(messageString);
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
