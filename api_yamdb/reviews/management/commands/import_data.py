import csv
import os

from django.core.management.base import BaseCommand

from django.conf import settings
from reviews.models import (Category,
                            Genre,
                            GenreTitle,
                            Title,
                            Review,
                            Comment,
                            User)


class Command(BaseCommand):
    help = 'Импорт данным из CSV файлов'

    def handle(self, *args, **kwargs):
        csv_dir = os.path.join(settings.BASE_DIR, 'static/data')

        self.import_categories(csv_dir)
        self.import_genres(csv_dir)
        self.import_titles(csv_dir)
        self.import_genre_titles(csv_dir)
        self.import_users(csv_dir)
        self.import_reviews(csv_dir)
        self.import_comments(csv_dir)

    def import_categories(self, csv_dir):
        with open(os.path.join(csv_dir, 'category.csv'),
                  'r',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category, created = Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Успешно импортирована category: {category.name}'
                    ))

    def import_genres(self, csv_dir):
        with open(os.path.join(csv_dir, 'genre.csv'),
                  'r',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                genre, created = Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Успешно импортирован genre: {genre.name}'
                    ))

    def import_titles(self, csv_dir):
        with open(os.path.join(csv_dir, 'titles.csv'),
                  'r',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title, created = Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Успешно импортировано title: {title.name}'
                    ))

    def import_genre_titles(self, csv_dir):
        with open(os.path.join(csv_dir, 'genre_title.csv'),
                  'r',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])

                GenreTitle.objects.create(
                    title=title,
                    genre=genre
                )
                self.stdout.write(self.style.SUCCESS(
                    f'Успешно импортирован GenreTitle с '
                    f'Title ID {row["title_id"]} '
                    f'и Genre ID {row["genre_id"]}'
                ))

    def import_users(self, csv_dir):
        with open(os.path.join(csv_dir, 'users.csv'),
                  'r',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user, created = User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Успешно импортирован user: {user.username}'
                    ))

    def import_reviews(self, csv_dir):
        with open(os.path.join(csv_dir, 'review.csv'),
                  'r',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                review, created = Review.objects.get_or_create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Успешно импортирован review: {review.id}'
                    ))

    def import_comments(self, csv_dir):
        with open(os.path.join(csv_dir, 'comments.csv'),
                  'r',
                  encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                comment, created = Comment.objects.get_or_create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date'],
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'Успешно импортирован comment: {comment.id}'
                    ))
