# recipes
Cooking recipes share

## Backend
- Django Rest Framework (DRF)
run tests:
$env:DJANGO_ENV="TEST"; python manage.py test

## Frontend
- React

### Pages
- All recipes (pagination): 
  - recipe_name, author_name
  - add recipe
  - delete (my) recipe
- recipe {id} page:
  - look up
  - add ingredient
  - delete ingredient
  - add stage
  - delete stage
  - reorder stages

## Database
1. Postgresql

### Models
- [x] recipes (id, recipe_name, author_id)
- [x] Authors (id, author_name)
- [x] Ingredients (id, ingredient_name, quantity, unit, recipe_id)
- [x] Stages (id, order, description, recipe_id)
- [x] Comments (id, content, recipe_id)

2. Redis
### Sets
- [ ] RecipeLikes (author_id, recipe_id)
- [ ] CommentsLike (author_id, comment_id)
