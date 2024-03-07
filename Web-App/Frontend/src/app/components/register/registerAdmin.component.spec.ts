import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RegisterAdminComponent } from './registerAdmin.component';



describe('RegisterAdminComponent', () => {
  let component: RegisterAdminComponent;
  let fixture: ComponentFixture<RegisterAdminComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegisterAdminComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(RegisterAdminComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
