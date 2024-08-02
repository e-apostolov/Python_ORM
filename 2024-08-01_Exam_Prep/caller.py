import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from django.db.models import Q, Count, Avg, Max
from main_app.models import Author, Article, Review

# Create queries within functions


def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        query = Q(query_name & query_email)
    elif search_name is not None:
        query = query_name
    else:
        query = query_email

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors:
        return ""

    return '\n'.join(f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}" for a in authors)


def get_top_publisher():
    top_publisher = Author.objects.get_authors_by_article_count().first()

    if not top_publisher or top_publisher.articles_count == 0:
        return ""

    return f"Top Author: {top_publisher.full_name} with {top_publisher.articles_count} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(reviews_count=Count('review')).order_by('-reviews_count', 'email').first()
    if not top_reviewer or top_reviewer.reviews_count == 0:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.reviews_count} published reviews."


def get_latest_article():
    last_article = Article.objects.prefetch_related('authors', 'review_set').order_by('-published_on').first()

    if last_article is None:
        return ""

    authors_names = ", ".join(a.full_name for a in last_article.authors.all().order_by('full_name'))
    number_of_reviews = last_article.review_set.count()
    average_rating = last_article.review_set.aggregate(avg=Avg('rating'))['avg'] or 0.0

    return f"The latest article is: {last_article.title}. " \
           f"Authors: {authors_names}. " \
           f"Reviewed: {number_of_reviews} times. Average Rating: {average_rating:.2f}."


def get_top_rated_article():
    top_rated_article = Article.objects.annotate(
        avg_rating=Avg('review__rating'),
        num_reviews=Count('review__id')
    ).filter(
        num_reviews__gt=0
    ).order_by(
        '-avg_rating', 'title'
    ).first()

    if not top_rated_article:
        return ""

    average_rating = top_rated_article.avg_rating or 0.0

    return f"The top-rated article is: {top_rated_article.title}, with an average rating of {average_rating:.2f}, reviewed {top_rated_article.num_reviews} times."


def ban_author(email=None):

    author = Author.objects.filter(email__exact=email).first()

    if email is None or author is None:
        return "No authors banned."

    reviews_count = author.review_set.count()

    author.is_banned = True
    author.save()
    author.review_set.all().delete()

    return f"Author: {author.full_name} is banned! {reviews_count} reviews deleted."
