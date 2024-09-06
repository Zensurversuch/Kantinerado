import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SuggestionCard } from './suggestion-card.component';

describe('SuggestionCardComponent', () => {
  let component: SuggestionCard;
  let fixture: ComponentFixture<SuggestionCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SuggestionCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SuggestionCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
