export enum MealTypes {
    Frühstück,
    Mittagessen,
    Abendessen,
    Nachtisch
}

export const MealTypesArray: string[] = Object.values(MealTypes).filter(value => typeof value === 'string').map(value => value.toString());
