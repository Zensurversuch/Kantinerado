export enum DietaryCategories {
    Fleisch,
    Vegetarisch,
    Vegan
}

export const DietaryCategoriesArray: string[] = Object.values(DietaryCategories).filter(value => typeof value === 'string').map(value => value.toString());
