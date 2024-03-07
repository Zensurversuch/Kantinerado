import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserOrderSummaryComponent } from './userOrderSummary.component';

describe('LoginComponent', () => {
  let component: UserOrderSummaryComponent;
  let fixture: ComponentFixture<UserOrderSummaryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserOrderSummaryComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UserOrderSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
