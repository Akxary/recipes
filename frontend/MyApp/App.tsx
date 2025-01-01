import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import RecipeList from './screens/RecipeList';
import RecipeDetails from './screens/RecipeDetails';
import { RootStackParamList } from './assets/types';

const Stack = createStackNavigator<RootStackParamList>();

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="RecipeList">
        <Stack.Screen name="RecipeList" component={RecipeList} options={{ title: 'Recipes' }} />
        <Stack.Screen name="RecipeDetails" component={RecipeDetails} options={{ title: 'Recipe Details' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
