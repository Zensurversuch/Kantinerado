import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateMealPlanComponent } from './create-meal-plan.component';

describe('CreateMealPlanComponent', () => {
  let component: CreateMealPlanComponent;
  let fixture: ComponentFixture<CreateMealPlanComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateMealPlanComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateMealPlanComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
