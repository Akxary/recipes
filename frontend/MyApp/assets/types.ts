type Ingredient = {
    name: string;
    quantity: number;
    unit: string;
};

type Stage = {
    description: string;
};

type Author = {
    id: number;
    name: string;
}

export type Recipe = {
    id: number;
    name: string;
    ingredients: Ingredient[];
    stages: Stage[];
    author: Author;
    commentsCount: number;
    likesCount: number;
};
export type RootStackParamList = {
    RecipeList: undefined;
    RecipeDetails: { recipe: Recipe; };
};
