type Ingredient = {
    id: number;
    name: string;
    quantity: number;
    unit: string;
};

type Stage = {
    id: number;
    order: number;
    description: string;
};

type Author = {
    id: number;
    name: string;
}

type Comment = {
    id: number;
    content: string;
    author: Author;
}

export type Recipe = {
    id: number;
    name: string;
    ingredients: Ingredient[];
    stages: Stage[];
    author: Author;
    comments: Comment[];
    likesCount: number;
};

export type RootStackParamList = {
    RecipeList: undefined;
    RecipeDetails: { recipe: Recipe; };
};
