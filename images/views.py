from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST

from .forms import ImageCreationForm
from .models import Image
from bookmarks.common.decorators import ajax_required
# Create your views here.
@login_required
def image_create_view(request):
    if request.method =='POST':
        #form is sent
        form = ImageCreationForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            #assign current user to the item
            new_item.user =  request.user
            new_item.save()
            messages.success(request, 'Image added successfully')

            #redirect to new created item view
            return redirect(new_item.get_absolute_url())
    else:
        #build form with data provided by the bookmarklet via GET
        form = ImageCreationForm(data = request.GET)

    return render(request, 'images/image/create.html', {'section':'images', 'form':form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    if image:
        print('Image found')
    return render(request, 'images/image/detail.html', {'section':'images', 'image':image})

@ajax_required
@login_required
@require_POST
def image_like_view(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_likes.add(request.user)
            else:
                image.user_likes.remove(request.user)
            return JsonResponse({ 'status': 'ok' })
        except:
            pass
    return JsonResponse({'status':'error'})

@login_required
def image_list_view(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer, deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            #If request is ajax and the page is out of range, return empty page
            return HttpResponse('')
        #if page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section':'images','images':images})
    return render(request, 'images/image/list.html', {'section':'images', 'images':images})
