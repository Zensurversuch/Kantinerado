import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SuggestionReviewComponent } from './suggestion-review.component';

describe('SuggestionReviewComponent', () => {
  let component: SuggestionReviewComponent;
  let fixture: ComponentFixture<SuggestionReviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SuggestionReviewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SuggestionReviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
