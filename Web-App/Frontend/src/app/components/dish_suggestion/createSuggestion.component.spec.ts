import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateSuggestionComponent } from './createSuggestion.component';

describe('DishSuggestionComponent', () => {
  let component: CreateSuggestionComponent;
  let fixture: ComponentFixture<CreateSuggestionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateSuggestionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateSuggestionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
