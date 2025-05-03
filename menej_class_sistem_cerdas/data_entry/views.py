from django.shortcuts import render, get_object_or_404, redirect
from .forms import AddressForm, PenggunaForm, ContentForm
from django.views.decorators.http import require_POST, require_http_methods

from .models import Pengguna, Content
from django.http import JsonResponse
from .models import Content  # Pastikan ini diimport juga kalau belum


# Create your views here.
def set_data_entry(request):    
    from django.shortcuts import render
from .forms import PenggunaForm

def set_data_entry(request):
    form = PenggunaForm()  # Inisialisasi form

    if request.method == "POST":
        form = PenggunaForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}  
    return render(request, 'data_entry/input_data_1.html', context)

def set_pengguna(request):
    list_pengguna = Pengguna.objects.all().order_by('-id')
    context = None
    form = PenggunaForm(None)
    email_p = None
    if request.method == "POST":
        form = PenggunaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['email'] = email
            request.session.modified = True
            form.save()
            list_pengguna = Pengguna.objects.all().order_by('-id')
            context = {
                'form': form,
                'list_pengguna' : list_pengguna,
                'email_p' : email_p,
            }
            return render(request, 'data_entry/input_data_1.html',context)
    else:
        context = {
            'form': form,
            'list_pengguna' : list_pengguna,
        }
    return render(request, 'data_entry/input_data_1.html',context)

def view_pengguna(request):
    pass

def view_pengguna(request, id):
    try:
        pengguna = Pengguna.objects.get(pk=id)
        return render(request, 'data_entry/pengguna_detail.html', {'user_id': pengguna.id})
    except Pengguna.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def get_pengguna_detail_api(request, user_id):
    try:
        pengguna = Pengguna.objects.get(pk=user_id)
        data = {
            'email': pengguna.email,
            'address_1': pengguna.address_1,
            'address_2': pengguna.address_2,
            'city': pengguna.city,
            'state': pengguna.state,
            'zip_code': pengguna.zip_code,
            'tanggal_join': pengguna.tanggal_join.strftime('%Y-%m-%d')  # Format date as string
        }
        return JsonResponse(data)
    except Pengguna.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

def update_pengguna(request, id):
    pengguna = get_object_or_404(Pengguna, pk=id)

    if request.method == 'POST':
        form = PenggunaForm(request.POST, instance=pengguna)
        if form.is_valid():
            form.save()
            return redirect('data_entry:view_pengguna', id=pengguna.id)  # atau redirect ke list
    else:
        form = PenggunaForm(instance=pengguna)

    return render(request, 'data_entry/update_pengguna.html', {'form': form, 'pengguna': pengguna})

@require_POST
def delete_pengguna(request, id):
    pengguna = get_object_or_404(Pengguna, pk=id)
    pengguna.delete()
    return redirect('data_entry:set_pengguna')  # sesuaikan dengan nama halaman list

# set_content baru, mirip kayak set_pengguna
def set_content(request):
    form = ContentForm(None)
    list_content = Content.objects.all().order_by('-id')  # Ambil semua content terbaru
    context = None
    pengguna = None
    email = None

    if request.session.get('email', None):
        email = request.session.get('email', None)
        pengguna = Pengguna.objects.get(email=email)
        initial_data = {'author': pengguna}
        form = ContentForm(initial=initial_data)

    if request.method == "POST":
        form = ContentForm(request.POST)
        if form.is_valid():
            form.save()
            # Setelah save, refresh list content
            list_content = Content.objects.all().order_by('-id')
            context = {
                'form': form,
                'list_content': list_content,
                'email': email,
                'pengguna': pengguna,
            }
            return render(request, 'data_entry/create_content.html', context)
    else:
        context = {
            'form': form,
            'list_content': list_content,
            'email': email,
            'pengguna': pengguna,
        }
    return render(request, 'data_entry/create_content.html', context)

def view_content(request, id):
    content = get_object_or_404(Content, pk=id)
    return render(request, 'data_entry/view_content.html', {'content': content})

def update_content(request, id):
    content = get_object_or_404(Content, pk=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            return redirect('data_entry:set_content')
    else:
        form = ContentForm(instance=content)
    return render(request, 'data_entry/update_content.html', {'form': form, 'content': content})

@require_http_methods(["POST"])
def delete_content(request, id):
    content = get_object_or_404(Content, pk=id)
    content.delete()
    return redirect('data_entry:set_content')