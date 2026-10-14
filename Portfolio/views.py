from django.shortcuts import render, get_object_or_404,redirect
from .models import ArtistModel, Category, Painting
from django.http import Http404
from .forms import AddCategory,AddPainting,EditAbout,MilestoneForm
from functools import wraps
from .utils import make_web_video

def painter_required(view):
    @wraps(view)
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            raise Http404
        return view(request, *args, **kwargs)
    return wrapper

# Create your views here.
def about(request):
    artist = ArtistModel.objects.select_related("user").first()
    return render(request, 'portfolio/about.html', 
                  {'artist':artist,
                   'category_count':Category.objects.count(),
                   'painting_count':Painting.objects.count()})

def art_category(request):
    categories = Category.objects.all()
    return render(request,'portfolio/category_list.html',{'categories':categories})

def category_detail(request,pk):
    category = get_object_or_404(Category, pk=pk)
    paintings = Painting.objects.filter(category=category).order_by('-pk')
    return render(request, "portfolio/category_detail.html", {
        "category": category,
        "paintings": paintings,
    })

@painter_required
def add_painting(request,category_id):
    category = get_object_or_404(Category,pk=category_id)
    
    if request.method == 'POST':
        form = AddPainting(request.POST,request.FILES)
        if form.is_valid():
            painting = form.save(commit=False)
            painting.category = category
            painting.save()
            if request.FILES.get('video'):
                make_web_video(painting)
            return redirect('category_detail',category.pk)
    else:
        form = AddPainting()
    return render(request, 'portfolio/add_painting.html', {'form': form, 'category': category})

@painter_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategory(request.POST,request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.artist = ArtistModel.objects.first()
            category.save()
            return redirect('category')
    else:
        form = AddCategory()
    return render(request, 'portfolio/add_category.html',{'form': form})

@painter_required
def del_painting(request,pk):
    painting = get_object_or_404(Painting,pk=pk)
    category_id = painting.category.pk
    
    painting.image.delete(save=False)
    if painting.video:
        painting.video.delete(save=False)
    
    painting.delete()
    return redirect("category_detail",category_id)

@painter_required
def edit_painting(request,pk):
    painting = get_object_or_404(Painting,pk=pk)
    category = painting.category
    
    if request.method == 'POST':
        form = AddPainting(request.POST, request.FILES, instance=painting)
        if form.is_valid():
            painting = form.save(commit=False)
            painting.save()
            if request.FILES.get('video'):
                make_web_video(painting)
            return redirect("category_detail",category.pk)
    else:
        form = AddPainting(instance=painting)
    return render(request, "portfolio/add_painting.html", {
        "form": form,
        "category": category,
        "editing": True,
    })

@painter_required
def del_category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    category.cover.delete(save=False)
    category.delete()
    return redirect("category")

@painter_required
def edit_category(request,pk):
    category = get_object_or_404(Category,pk=pk)
    
    if request.method == 'POST':
        form = AddCategory(request.POST,request.FILES,instance=category)
        if form.is_valid():
            category=form.save(commit=False)
            category.save()
            return redirect("category")
    else:
        form = AddCategory(instance=category)
    return render(request,'portfolio/add_category.html',{'form': form,'editing':True})

@painter_required
def edit_about(request):
    artist = ArtistModel.objects.first()
    if artist is None:
        return redirect("about")
    if request.method == 'POST':
        form = EditAbout(request.POST,request.FILES,instance=artist)
        formset = MilestoneForm(request.POST,instance=artist)
        
        if form.is_valid() and formset.is_valid():
            artist = form.save(commit=False)
            artist.save()
            formset.save()
            if request.FILES.get('video'):
                make_web_video(artist)
            return redirect("about")
    else:
        form = EditAbout(instance=artist)
        formset = MilestoneForm(instance=artist)
        
    return render(request,'portfolio/edit_about.html',{'form':form,'formset':formset})
    