import { Injectable } from '@angular/core';
import {Socket} from "ngx-socket-io";

@Injectable({
  providedIn: 'root'
})
export class SearchSocketService {
  constructor(private socket: Socket) { }

  sendMessage(message: string): void {
    this.socket.emit(message);
  }

  onMessageReceived(): any {
    return this.socket.fromEvent('test')
  }
}
