from rest_framework import serializers
from users.models import User
from rest_framework import serializers
from reviews.models import Comment, Review, Category, Genre, Title
from django.db.models import Avg


from reviews.models import Category, Genre, Title, Review
from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Genre


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data

class TitleSerializer(serializers.ModelSerializer):
    category = CategoryField(slug_field='slug', queryset=Category.objects.all(), required=False)
    genre = GenreField(slug_field='slug', queryset=Genre.objects.all(), many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)
        model = Title

    def get_rating(self, obj):
        rating = Review.objects.filter(title_id=obj.id).aggregate(Avg('score'))
        return rating.get('score__avg')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        extra_kwargs = {'score': {'required': True},
                        'text': {'required': True}}

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            review_by_author_title = Review.objects.filter(title=title_id, author_id=self.context['request'].user)
            if review_by_author_title.exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        extra_kwargs = {'review_id': {'required': True}}

