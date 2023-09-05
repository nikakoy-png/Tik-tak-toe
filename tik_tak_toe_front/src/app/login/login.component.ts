import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {ApiService} from '../api.service';
import {CookieService} from 'ngx-cookie-service';
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;

  ngOnInit() {
    this.loginForm = new FormGroup({
      username: new FormControl(''),
      password: new FormControl(''),
    });
  }

  constructor(
    private formBuilder: FormBuilder,
    private cookieService: CookieService,
    private apiService: ApiService,
    private router: Router
  ) {
  }

  private saveTokenToCookie(token: string): void {
    this.cookieService.set('token', token);
  }

  onSubmit(): void {
    if (this.loginForm.valid) {
      console.log('ok')
      console.log(this.loginForm)
      const formData = this.loginForm.value;
      this.apiService.login(formData).subscribe(
        (response) => {
          this.saveTokenToCookie(response.access);
          this.router.navigate(['main']);
        },
        (error) => {
          console.error('Error: ', error);
        }
      );
    }
  }
}
