export enum Weekday {
  Montag,
  Dienstag,
  Mittwoch,
  Donnerstag,
  Freitag,
  Samstag
}
export const WeekdayArray: string[] = Object.values(Weekday).filter(value => typeof value === 'string').map(value => value.toString());
