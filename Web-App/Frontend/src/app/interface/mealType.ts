export enum MealType {
  Fruehstueck,
  Mittagessen,
  Abendessen,
  Nachtisch,
  Suppe
}

export const MealTypesArray: string[] = Object.values(MealType).filter(value => typeof value === 'string').map(value => value.toString());
