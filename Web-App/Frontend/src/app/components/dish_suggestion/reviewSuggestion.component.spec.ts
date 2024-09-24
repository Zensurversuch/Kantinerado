import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReviewSuggestionComponent } from './reviewSuggestion.component';

describe('SuggestionReviewComponent', () => {
  let component: ReviewSuggestionComponent;
  let fixture: ComponentFixture<ReviewSuggestionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReviewSuggestionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReviewSuggestionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
