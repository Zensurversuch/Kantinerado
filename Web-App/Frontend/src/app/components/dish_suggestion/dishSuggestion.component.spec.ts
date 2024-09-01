import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DishSuggestionComponent } from './dishSuggestion.component';

describe('DishSuggestionComponent', () => {
  let component: DishSuggestionComponent;
  let fixture: ComponentFixture<DishSuggestionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DishSuggestionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DishSuggestionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
