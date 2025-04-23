<script lang="ts">
import { defineComponent, type PropType } from 'vue';
interface Stage {
    num: number
    description: string
}
interface Recipe {
    name: string
    author: string
    stages: Array<Stage>
}

export default defineComponent({
    props: {
        recipe: {type: Object as PropType<Recipe>, required: true, default:{}}
    },
    mounted() {
        this.recipe.stages.sort((a:Stage, b:Stage)=>a.num-b.num);
    }
})
</script>

<template>
    <h2> {{ recipe.name }}</h2>
    <p>Автор: {{ recipe.author }}</p>
    <div v-for="(stage, idx) of recipe.stages">
        {{ stage.num }}) {{ stage.description }}
    </div>
</template>