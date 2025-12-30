from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import BioProfile, Link

# --- Public Profile View (Already exists, just keeping it here) ---
class ProfileDetailView(DetailView):
    model = BioProfile
    template_name = 'links/profile.html'
    context_object_name = 'profile'
    slug_url_kwarg = 'slug'
    queryset = BioProfile.objects.all()

# --- 1. SIGN UP VIEW ---
class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'links/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'links/signup.html', {'form': form})

# --- 2. DASHBOARD VIEW ---
@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        profile = request.user.bioprofile
        links = profile.links.all()
        return render(request, 'links/dashboard.html', {'profile': profile, 'links': links})

# --- 3. EDIT PROFILE VIEW ---
@method_decorator(login_required, name='dispatch')
class EditProfileView(UpdateView):
    model = BioProfile
    template_name = 'links/edit_profile.html'
    fields = ['slug', 'bio', 'avatar', 'theme']
    success_url = '/dashboard/'
    
    def get_object(self):
        return self.request.user.bioprofile
    
@login_required
def add_link(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        url = request.POST.get('url')
        Link.objects.create(
            profile=request.user.bioprofile,
            title=title,
            url=url,
            order=0 # Simple default order
        )
    return redirect('dashboard')

@login_required
def delete_link(request, link_id):
    link = Link.objects.get(id=link_id, profile=request.user.bioprofile)
    link.delete()
    return redirect('dashboard') 

from django.http import JsonResponse

# ... existing views ...

@login_required
def reorder_links(request):
    """
    Receives a list of link IDs in the new order and updates the DB.
    """
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]') # SortableJS sends an array
        for index, link_id in enumerate(ids):
            try:
                link = Link.objects.get(id=link_id, profile=request.user.bioprofile)
                link.order = index
                link.save()
            except Link.DoesNotExist:
                pass # Skip if ID is invalid or belongs to another user
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)