import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { MatAutocompleteModule, MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatInputModule } from '@angular/material/input';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { RouterOutlet } from '@angular/router';
import { airports } from '../data';

@Component({
  selector: 'app-root',
  standalone: true,
  providers: [provideNativeDateAdapter()],
  imports: [
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatAutocompleteModule,
    MatDatepickerModule,
    ReactiveFormsModule,
    RouterOutlet,
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class AppComponent implements OnInit {
  title = 'Flight Checker';
  flightSearchForm!: FormGroup;
  options = airports as {
    airportName: string;
    iataCode: string;
    city: string;
  }[];
  filteredOptionsFrom!: Observable<
    { airportName: string; iataCode: string; city: string }[]
  >;
  filteredOptionsTo!: Observable<
    { airportName: string; iataCode: string; city: string }[]
  >;

  constructor(private formBuilder: FormBuilder) {}

  ngOnInit() {
    this.flightSearchForm = this.formBuilder.group({
      from: [],
      to: [],
      departureDate: [''],
      passengers: [''],
    });

    this.filteredOptionsFrom = this.flightSearchForm
      .get('from')!
      .valueChanges.pipe(
        startWith([]),
        map((value) => this._filter(value || []))
      );

    this.filteredOptionsTo = this.flightSearchForm.get('to')!.valueChanges.pipe(
      startWith(''),
      map((value) => this._filter(value || []))
    );
  }

  onFromOptionSelected(field:string, event: MatAutocompleteSelectedEvent): void {
    const selectedOption = event.option.value;
    this.flightSearchForm.get(field)!.setValue(selectedOption);
  }
  
  

  private _filter(value: { airportName: string; iataCode: string; city: string }): { airportName: string; iataCode: string; city: string }[] {
    const filterValue = value.iataCode.toLowerCase();
    return this.options.filter((option) =>
      option.iataCode.toLowerCase().includes(filterValue)
    );
  }
}
