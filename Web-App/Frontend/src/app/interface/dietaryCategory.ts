export enum DietaryCategory {
    Fleisch,
    Vegetarisch,
    Vegan
}

export const DietaryCategoriesArray: string[] = Object.values(DietaryCategory).filter(value => typeof value === 'string').map(value => value.toString());
