export enum MealType {
    Frühstück,
    Mittagessen,
    Abendessen,
    Nachtisch
}

export const MealTypesArray: string[] = Object.values(MealType).filter(value => typeof value === 'string').map(value => value.toString());
