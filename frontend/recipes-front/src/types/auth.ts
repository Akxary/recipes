import type { StringLiteral } from "typescript";
import type { InjectionKey } from "vue";

export type UpdateTokenFunction = (newToken: string) => void;

export const UpdateTokenKey = Symbol() as InjectionKey<UpdateTokenFunction>;

export interface User {
    name: string;
    email: string;
}

export interface State {
    userToken: string | null;
    user: User | null;
}

export const StateKey = Symbol() as InjectionKey<State>;