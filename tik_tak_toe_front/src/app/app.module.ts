import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { RegistrationComponent } from './registration/registration.component';
import { LoginComponent } from './login/login.component';
import {HttpClientModule} from "@angular/common/http";
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {AppRoutingModule} from "./app-routing.module";
import { MainComponent } from './main/main.component';
import { SearchComponent } from './search/search.component';
import {SearchSocketService} from "./search-socket.service";
import { PlayComponent } from './play/play.component';
import { UserComponent } from './user/user.component';


@NgModule({
  declarations: [
    AppComponent,
    RegistrationComponent,
    LoginComponent,
    MainComponent,
    SearchComponent,
    PlayComponent,
    UserComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    AppRoutingModule,
  ],
  providers: [SearchSocketService],
  bootstrap: [AppComponent]
})
export class AppModule { }
