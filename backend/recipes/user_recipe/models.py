from django.db import models


from django_enum import EnumField


class CreatedAtMixin(models.Model):
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Authors(CreatedAtMixin):
    # email: models.EmailField = models.EmailField(unique=True, null=False, blank=False)
    email: models.EmailField = models.EmailField(db_index=True, unique=True, null=False, blank=False)
    author_name: models.CharField = models.CharField(max_length=256)


class Recipes(CreatedAtMixin, UpdatedAtMixin):
    recipe_name: models.TextField = models.TextField()
    author: models.ForeignKey = models.ForeignKey(
        Authors,
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    comments: models.Manager["Comments"]
    ingredients: models.Manager["Ingredients"]
    stages: models.Manager["Stages"]

    class Meta(CreatedAtMixin.Meta, UpdatedAtMixin.Meta):
        pass


class Ingredients(models.Model):
    class Units(models.TextChoices):
        BIG_SPOON = "ст.л."
        SMALL_SPOON = "ч.л."
        GRAMM = "г"
        MILLI_LITR = "мл"
        COUNT = "шт."

    ingredient_name: models.CharField = models.CharField(max_length=256)
    quantity: models.IntegerField = models.IntegerField()
    unit: EnumField = EnumField(Units, default=Units.GRAMM)
    recipe: models.ForeignKey[Recipes] = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )


class Stages(models.Model):
    order: models.IntegerField = models.IntegerField()
    description: models.TextField = models.TextField()
    recipe: models.ForeignKey[Recipes] = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name="stages",
    )


class Comments(CreatedAtMixin, UpdatedAtMixin):
    content: models.TextField = models.TextField()
    author: models.ForeignKey = models.ForeignKey(
        Authors,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    recipe: models.ForeignKey[Recipes] = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    class Meta(CreatedAtMixin.Meta, UpdatedAtMixin.Meta):
        pass
