import {Role} from "./role"
export interface UserData {
  lastName: string;
  firstName: string;
  email: string;
  password: string;
  role: Role;
}
