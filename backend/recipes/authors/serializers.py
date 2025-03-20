from authors.models import Authors


from rest_framework import serializers


class ShortAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ["id", "email", "author_name"]

class AuthorInstance:
    author: Authors

class AbstractAuthorSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Authors.objects.all())

    def to_representation(self, instance: AuthorInstance) -> dict:
        representation = super().to_representation(instance)
        author_instance = instance.author
        representation["author"] = ShortAuthorSerializer(author_instance).data["author_name"]
        return representation