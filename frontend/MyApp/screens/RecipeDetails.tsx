import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity, Button, TextInput } from 'react-native';
import { RouteProp } from '@react-navigation/native';
import { RootStackParamList } from '../assets/types';

type RecipeDetailsProps = {
  route: RouteProp<RootStackParamList, 'RecipeDetails'>;
};

const RecipeDetails = ({ route }: RecipeDetailsProps) => {
  const { recipe } = route.params;
  const [showComments, setShowComments] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [ingredients, setIngredients] = useState(recipe.ingredients);
  const [stages, setStages] = useState(recipe.stages);

  // Обработчик добавления ингредиента
  const handleAddIngredient = () => {
    setIngredients([...ingredients, { id: 0, name: '', quantity: 0, unit: '' }]);
  };

  // Обработчик удаления ингредиента
  const handleDeleteIngredient = (index: number) => {
    setIngredients(ingredients.filter((_, i) => i !== index));
  };

  // Обработчик изменения ингредиента
  const handleIngredientChange = (index: number, key: string, value: string) => {
    const updatedIngredients = [...ingredients];
    updatedIngredients[index][key] = value;
    setIngredients(updatedIngredients);
  };

  // Обработчик добавления стадии
  const handleAddStage = () => {
    setStages([...stages, { id:0, order: 1, description: '' }]);
  };

  // Обработчик удаления стадии
  const handleDeleteStage = (index: number) => {
    setStages(stages.filter((_, i) => i !== index));
  };

  // Обработчик изменения стадии
  const handleStageChange = (index: number, value: string) => {
    const updatedStages = [...stages];
    updatedStages[index].description = value;
    setStages(updatedStages);
  };

  // Сохранение изменений
  const handleSave = () => {
    setIsEditing(false);
    // Отправьте данные на сервер с помощью API (fetch/axios)
    console.log('Updated ingredients:', ingredients);
    console.log('Updated stages:', stages);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{recipe.name}</Text>

      {/* Кнопка "Редактировать/Сохранить" */}
      <Button
        title={isEditing ? 'Сохранить' : 'Редактировать'}
        onPress={() => (isEditing ? handleSave() : setIsEditing(true))}
      />

      {/* Ингредиенты */}
      <Text style={styles.subtitle}>Ингредиенты:</Text>
      {isEditing ? (
        <FlatList
          data={ingredients}
          renderItem={({ item, index }) => (
            <View style={styles.editContainer}>
              <TextInput
                style={styles.input}
                placeholder="Название"
                value={item.name}
                onChangeText={(value) => handleIngredientChange(index, 'name', value)}
              />
              <TextInput
                style={styles.input}
                placeholder="Количество"
                value={item.quantity}
                onChangeText={(value) => handleIngredientChange(index, 'quantity', value)}
              />
              <TextInput
                style={styles.input}
                placeholder="Единица измерения"
                value={item.unit}
                onChangeText={(value) => handleIngredientChange(index, 'unit', value)}
              />
              <TouchableOpacity onPress={() => handleDeleteIngredient(index)}>
                <Text style={styles.delete}>Удалить</Text>
              </TouchableOpacity>
            </View>
          )}
          keyExtractor={(_, index) => `ingredient-${index}`}
        />
      ) : (
        <FlatList
          data={ingredients}
          renderItem={({ item }) => (
            <Text style={styles.text}>
              {item.name} - {item.quantity} {item.unit}
            </Text>
          )}
          keyExtractor={(_, index) => `ingredient-${index}`}
        />
      )}
      {isEditing && <Button title="Добавить ингредиент" onPress={handleAddIngredient} />}

      {/* Стадии */}
      <Text style={styles.subtitle}>Стадии:</Text>
      {isEditing ? (
        <FlatList
          data={stages}
          renderItem={({ item, index }) => (
            <View style={styles.editContainer}>
              <TextInput
                style={styles.input}
                placeholder="Описание стадии"
                value={item.description}
                onChangeText={(value) => handleStageChange(index, value)}
              />
              <TouchableOpacity onPress={() => handleDeleteStage(index)}>
                <Text style={styles.delete}>Удалить</Text>
              </TouchableOpacity>
            </View>
          )}
          keyExtractor={(_, index) => `stage-${index}`}
        />
      ) : (
        <FlatList
          data={stages}
          renderItem={({ item }) => <Text style={styles.text}>{item.description}</Text>}
          keyExtractor={(_, index) => `stage-${index}`}
        />
      )}
      {isEditing && <Button title="Добавить стадию" onPress={handleAddStage} />}
      <TouchableOpacity onPress={() => setShowComments((prev) => !prev)}>
        <Text style={styles.subtitle}>
          Комментарии ({recipe.comments.length}) {showComments ? '▲' : '▼'}
        </Text>
      </TouchableOpacity>

      {showComments && !isEditing && (
        <FlatList
          data={recipe.comments}
          renderItem={({ item }) => 
          <View>
            <Text style={styles.underline}>{item.author.name}</Text>
            <Text style={styles.text}>{item.content}</Text>
            
          </View>
        }
          keyExtractor={(item, index) => `${item.id}-${index}`}
        />
      )}
    </View>

  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#fff' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 16 },
  subtitle: { fontSize: 18, fontWeight: 'bold', marginTop: 16, marginBottom: 8 },
  underline: {fontSize: 14, fontStyle: "italic"},
  text: { fontSize: 14, marginBottom: 8 },
  input: { borderWidth: 1, padding: 8, marginBottom: 8, borderRadius: 4, borderColor: '#ccc' },
  editContainer: { marginBottom: 16 },
  delete: { color: 'red', fontWeight: 'bold' },
});

export default RecipeDetails;
