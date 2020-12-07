from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect,reverse
from images.models import *
from django.db.models import Count
from images.filters import TagsFilter,CategoryFilter
from taggit.models import Tag
from django.core.paginator import Paginator
from . import filters
# from wildarts.forms import ContactusForm,ReportForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST


from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required

from images.models import Pictures
from django.http import HttpResponse
from account.models import User

from images.forms import CreatePostForm, UpdatePostForm



def homepage(request,tag_slug=None):
    pictures = Pictures.objects.all().order_by("-date_published")
    
    
    category_filter =CategoryFilter(request.GET,queryset=pictures)
    tags_filter = TagsFilter(request.GET,queryset=pictures)
    
    pagifilter = tags_filter.qs

    

    paginator = Paginator(pagifilter,10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)


    new_request = ''
    for i in request.GET:
        if i != 'page':
            val = request.GET.get(i)
            new_request += f"&{i}={val}"

    context = {
        'pictures':pictures,
        'filter': tags_filter,
        'page_obj':page_obj,
        'new_request':new_request,
        'category_filter':category_filter,
    }

    return render(request,'images/home.html',context)

def picture_detail(request, slug):
    picture_detail = get_object_or_404(Pictures, slug=slug)

 

    picture = get_object_or_404(Pictures,slug=slug)

    picture_detail_tags = picture_detail.tags.values_list('id',flat = True)
    similar_pictures =  Pictures.objects.filter(tags__in= picture_detail_tags).exclude(id= picture_detail.id)
    similar_pictures =  similar_pictures.annotate(same__tags= Count('tags')).order_by('-same__tags','-date_published')

    # new_report = None
    
    # if request.method == 'POST':
    #     reportform = ReportForm(request.POST)
    #     if reportform.is_valid():
    #         new_report = reportform.save(commit=False)
    #         new_report.picture = picture
    #         new_report.save()
    #         messages.add_message(request, messages.INFO, 'Reported')
    #         return redirect("picture_detail", slug=slug)
    # else:
    #     reportform = ReportForm()

    context= {
        'picture_detail':picture_detail,
        'similar_pictures':similar_pictures,
        # 'reportform':reportform,
        # 'new_report':new_report, 
    }

    return render(request, 'images/picture_detail.html', context)


# def about_us(request):
#     return render(request, 'wildarts/about_us.html')

# def terms_of_use(request):
#     return render(request, 'wildarts/terms_of_use.html')

# def privacy_policy(request):
#     return render(request, 'wildarts/privacy_policy.html')

# def contactus(request):
#     if request.method =='POST':
#         form = ContactusForm(request.POST)
#         if form.is_valid:
#             form.save()
#             messages.add_message(request, messages.INFO, 'Submitted Succesfully.')
#             return redirect(reverse('contactus'))
            
#     else:
#         form = ContactusForm()
#         return render(request,'wildarts/contactus.html',{'form':form})

@login_required(login_url='must_authenticate')
def create_image_post(request):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('must_authenticate'))

    form = CreatePostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit=False)
        author = User.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form.save_m2m()
        form = CreatePostForm()
        messages.success(request,"Art Created")
        return redirect(reverse('home'))

    context['form'] = form

    return render(request, "images/create_ad.html", context)

@login_required(login_url='must_authenticate')
def edit_image_post_view(request, slug):

    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    image_post = get_object_or_404(Pictures, slug=slug)

    if image_post.author != user:
        return HttpResponse('You are not the author of that post.')

    if request.POST:
        form = UpdatePostForm(
            request.POST or None, request.FILES or None, instance=image_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            context['success_message'] = "Updated"
            image_post = obj
            messages.success(request,"Art Edited")
            return redirect(reverse('home'))

    form = UpdatePostForm(
        initial={
            "title": image_post.title,
            "description": image_post.description,
            "image": image_post.image,
            "category":image_post.category,
            # "tags":image_post.tags.all,        
        }
    )

    context['form'] = form
    return render(request, 'images/edit_ad.html', context)

@login_required(login_url='must_authenticate')
def delete_image_post_view(request, slug):

    delete_image = Pictures.objects.get(slug=slug)
    if request.method == 'POST':
        delete_image.delete()
        messages.success(request,"Art deleted")
        return redirect(reverse('home'))



@login_required(login_url='must_authenticate')
@require_POST
def image_like(request):
    image_id =request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image  = Pictures.objects.get(id =image_id)
            if action  == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})



