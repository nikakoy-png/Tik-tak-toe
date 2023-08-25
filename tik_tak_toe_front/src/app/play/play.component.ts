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
      console.log(parsedMsg);
      this.gameBoard = parsedMsg['board'];
      this.gameBoard = this.generateGameBoard();
    });
  }

  generateGameBoard(): string[][] {
    if (!this.gameBoard) {
      return [];
    }

    const board: string[][] = [];
    for (let i = 0; i < this.gameBoard.length; i++) {
      const row: string[] = [];
      for (let j = 0; j < this.gameBoard[i].length; j++) {
        row.push((this.gameBoard[i][j] === 0) ? ' ' : 'X');
      }
      board.push(row);
    }
    return board;
  }
}
