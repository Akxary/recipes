import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity } from 'react-native';
import { RootStackParamList } from '../assets/types';
import { StackNavigationProp } from '@react-navigation/stack';
import { Recipe } from '../assets/types';


type RecipeListProps = {
    navigation: StackNavigationProp<RootStackParamList, 'RecipeList'>;
};

const RecipeList = ({ navigation }: RecipeListProps) => {
    const [recipes, setRecipes] = useState<Recipe[]>([]);

    useEffect(() => {
        // Замените URL на ваш backend endpoint
        // fetch('https://your-backend.com/api/recipes')
        // .then((res) => res.json())
        // .then((data) => setRecipes(data))
        // .catch((err) => console.error(err));
        const jsonData = require('../assets/json/recipes.json');
        setRecipes(jsonData);
    }, []);

    const renderItem = ({ item }: { item: Recipe }) => (
        <TouchableOpacity
            style={styles.item}
            onPress={() => navigation.navigate('RecipeDetails', { recipe: item })}
        >
            <Text style={styles.name}>{item.name.slice(0, 10)}</Text>
            <Text style={styles.author}>{item.author.name.slice(0, 10)}</Text>
            <Text style={styles.meta}>
            ❤️ {item.likesCount}    🗨 {item.commentsCount}
            </Text>
        </TouchableOpacity>
    );

    return (
        <View style={styles.container}>
            <FlatList
                data={recipes}
                renderItem={renderItem}
                keyExtractor={(item) => item.id.toString()}
                contentContainerStyle={styles.list}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: { flex: 1, padding: 16, backgroundColor: '#fff' },
    list: { paddingBottom: 16 },
    item: { marginBottom: 12, padding: 16, borderWidth: 1, borderColor: '#ddd', borderRadius: 8 },
    name: { fontSize: 16, fontWeight: 'bold' },
    author: { fontSize: 14, color: '#555' },
    meta: { fontSize: 12, color: '#888', marginTop: 8 },
});

export default RecipeList;
