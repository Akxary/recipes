from django.db import models
from recipes.model_mixins import CreatedAtMixin



class Authors(CreatedAtMixin):
    # email: models.EmailField = models.EmailField(unique=True, null=False, blank=False)
    email: models.EmailField = models.EmailField(
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )
    author_name: models.CharField = models.CharField(max_length=256)
    # is_anonymous: models.BooleanField = models.BooleanField()
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS= []
