import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../assets/types';

type RecipeDetailsProps = {
  route: RouteProp<RootStackParamList, 'RecipeDetails'>;
};

const RecipeDetails = ({ route }: RecipeDetailsProps) => {
  const { recipe } = route.params;
//   const [recipe, setRecipe] = useState<Recipe | null>(null);

//   useEffect(() => {
//     // Замените URL на ваш backend endpoint
//     fetch(`https://your-backend.com/api/recipes/${recipeId}`)
//       .then((res) => res.json())
//       .then((data) => setRecipe(data))
//       .catch((err) => console.error(err));
//   }, [recipeId]);

//   if (!recipe) {
//     return (
//       <View style={styles.container}>
//         <Text>Loading...</Text>
//       </View>
//     );
//   }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{recipe.name}</Text>

      <Text style={styles.subtitle}>Ингредиенты:</Text>
      <FlatList
        data={recipe.ingredients}
        renderItem={({ item }) => (
          <Text style={styles.text}>
            {item.name} - {item.quantity} {item.unit}
          </Text>
        )}
        keyExtractor={(item, index) => `${item.name}-${index}`}
      />

      <Text style={styles.subtitle}>Стадии:</Text>
      <FlatList
        data={recipe.stages}
        renderItem={({ item }) => <Text style={styles.text}>{item.description}</Text>}
        keyExtractor={(item, index) => `${item.description}-${index}`}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 16 },
  subtitle: { fontSize: 18, fontWeight: 'bold', marginTop: 16, marginBottom: 8 },
  text: { fontSize: 14, marginBottom: 8 },
});

export default RecipeDetails;
