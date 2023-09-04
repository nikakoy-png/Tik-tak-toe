import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {ApiService} from "../api.service";
import {AppRoutingModule} from "../app-routing.module";
import {Router} from "@angular/router";

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {
  registrationForm!: FormGroup;

  ngOnInit(): void {
    this.registrationForm = this.formBuilder.group({
      email: new FormControl('', [
        Validators.required,
      ]),
      username: new FormControl('', [
        Validators.required,
        Validators.minLength(4),
      ]),
      password: new FormControl('', [
        Validators.required,
      ]),
      password_confirm: new FormControl('', [
        Validators.required,
      ]),
    });
  }

  constructor(private formBuilder: FormBuilder,
              private apiService: ApiService,
              private router: Router) {
  }

  onSubmit(): void {
    if (this.registrationForm.valid) {
      const formData = this.registrationForm.value;
      this.apiService.register(formData).subscribe(
        (response) => {
          console.log('successfully')
          this.router.navigate(['login'])
        },
        (error) => {
          console.log('Error: ', error)
        }
      );
    }
  }
}
