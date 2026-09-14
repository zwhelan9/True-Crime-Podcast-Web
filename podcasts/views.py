from django.shortcuts import render, get_object_or_404
from podcasts.models import Category, Podcast, Episode, Review, Favorite
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Avg
from pages.forms import ReviewForm

def home(request):
    categories = Category.objects.all()
 
    featured = Podcast.objects.order_by('-id')[:5]
    trending = Podcast.objects.annotate(
        num_reviews=Count('reviews')
    ).order_by('-num_reviews')[:5]

    return render(request, 'podcasts/home.html', {
        'podcasts': featured,
        'trending': trending,
        'categories': categories
    })

def podcast_detail(request, id):
    podcast = get_object_or_404(Podcast, id=id)
    episodes = Episode.objects.filter(podcast=podcast)
    avg_rating = podcast.reviews.aggregate(
    Avg('rating'))['rating__avg'] or 0
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = podcast in request.user.favorite_podcasts.all()
    return render(request, 'podcasts/podcast_detail.html', {
        'podcast': podcast,
        'episodes': episodes,
        'avg_rating': avg_rating,
        'is_favorited': is_favorited
    })

def podcast_list(request):
    category_id = request.GET.get('category')

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        category_id_post = request.POST.get("category")

        podcast = Podcast.objects.create(
          title=title,
          description=description,
          image=image
        )
        if category_id_post:
            podcast.category.set([category_id_post])

        return redirect('podcast_list')

    podcasts = Podcast.objects.all()
    avg_rating = Podcast.objects.aggregate(Avg('reviews__rating'))['reviews__rating__avg']

    if category_id:
        podcasts = podcasts.filter(category__id=category_id)

    categories = Category.objects.all()

    return render(request, 'podcasts/podcast_list.html', {
        'podcasts': podcasts,
        'categories': categories,
        'avg_rating': avg_rating,
    })

def delete_podcast(request, podcast_id):
    podcast = get_object_or_404(Podcast, id=podcast_id)

    if request.method == "POST":
        podcast.delete()

    return redirect('podcast_list')

def episode_detail(request, id):
    episode = get_object_or_404(Episode, id=id)
    return render(request, 'podcasts/episode_detail.html', {'episode': episode})

def search(request):
    query = request.GET.get('q')
    podcasts = Podcast.objects.all()

    if query:
        podcasts = podcasts.filter(title__icontains=query)

    return render(request, 'podcasts/search.html', {
        'podcasts': podcasts,
        'query': query
    })

@login_required
def add_review(request, id):
    podcast = get_object_or_404(Podcast, id=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.podcast = podcast
            review.save()
    return redirect('podcast_detail', id=id)

@login_required
def toggle_favorite(request, id):
    podcast = get_object_or_404(Podcast, id=id)

    if request.method == "POST":
        if podcast in request.user.favorite_podcasts.all():
            request.user.favorite_podcasts.remove(podcast)
        else:
            request.user.favorite_podcasts.add(podcast)

    return redirect('podcast_detail', id=podcast.id)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Only allow the user who created the review
    if review.user == request.user:
        review.delete()

    return redirect('podcast_detail', id=review.podcast.id)