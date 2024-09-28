import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
} from '@angular/forms';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { NgIf,NgFor } from '@angular/common';
import { MatAutocompleteModule, MatAutocompleteSelectedEvent } from '@angular/material/autocomplete';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { provideNativeDateAdapter } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import {MatButtonModule} from '@angular/material/button';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import {MatDivider} from '@angular/material/divider';
import {MatCardModule} from '@angular/material/card';
import {MatIcon} from '@angular/material/icon';
import {MatGridListModule} from '@angular/material/grid-list';
import { RouterOutlet } from '@angular/router';
import { airports } from '../data';
import {FlightService} from '../services/flightService'

@Component({
  selector: 'app-root',
  standalone: true,
  providers: [provideNativeDateAdapter(), FlightService],
  imports: [
    NgIf,
    NgFor,
    MatDivider,
    MatIcon,
    MatSlideToggleModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatAutocompleteModule,
    MatGridListModule,
    MatButtonModule,
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
  isLoading: boolean = false;
  response =[]

  constructor(private formBuilder: FormBuilder, private flightService: FlightService) {}

  ngOnInit() {
    this.flightSearchForm = this.formBuilder.group({
      from: [],
      to: [],
      departureDate: [''],
      passengers: [''],
      no_cache: [true]
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

  searchFlightFare() {
    if (this.flightSearchForm.valid) {
      this.isLoading = true; 
      const formData = this.flightSearchForm.value;
      this.flightService.getFlightPrices(
        formData.from.iataCode,
        formData.to.iataCode,
        formData.departureDate,
        formData.passengers
      ).then(
        (results) => {
          console.log('Flight search results:', results);
          this.response = results.data;
          // Handle the search results here (e.g., update a property to display in the template)
          this.isLoading = false; 
        },
      ).catch(
        (error) => {
          console.error('Error searching flights:', error);
          // Handle any errors here (e.g., show an error message to the user)
          this.isLoading = false; 
        }
      );
    } else {
      console.log('Form is invalid');
      // Optionally, you can mark all form controls as touched to trigger validation messages
      Object.values(this.flightSearchForm.controls).forEach(control => {
        control.markAsTouched();
      });
    }
  }  

  calculateDuration(departureTime: string, arrivalTime: string): string {
    const departure = new Date(departureTime);
    const arrival = new Date(arrivalTime);
    const durationMs = arrival.getTime() - departure.getTime();
    const hours = Math.floor(durationMs / (1000 * 60 * 60));
    const minutes = Math.floor((durationMs % (1000 * 60 * 60)) / (1000 * 60));
    return `${hours}h ${minutes}m`;
  }


  clearFlightSearchForm() {
    this.flightSearchForm.reset({
      from: null,
      to: null,
      departureDate: '',
      passengers: '',
      no_cache: [true]
    });
  }
  

  private _filter(value: { airportName: string; iataCode: string; city: string }): { airportName: string; iataCode: string; city: string }[] {
    const filterValue = value.iataCode.toLowerCase();
    return this.options.filter((option) =>
      option.iataCode.toLowerCase().includes(filterValue)
    );
  }
}
