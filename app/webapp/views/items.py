from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from webapp.forms import ItemForm
from webapp.models import Item


def add_view(request: WSGIRequest):
    form = ItemForm
    if request.method == 'GET':
        return render(request, 'add_item.html', context={'form': form})
    form = ItemForm(request.POST)
    if not form.is_valid():
        return render(request, 'add_item.html', context={'form': form})
    item = Item.objects.create(**form.cleaned_data)
    url = reverse('show_item', kwargs={'pk': item.pk})
    return HttpResponseRedirect(url)


def items_view(request: WSGIRequest):
    if not request.method == 'POST':
        items = Item.objects.exclude(is_deleted=True)
        context = {
            'items': items,
        }
        return render(request, 'items.html', context)
    else:
        items_to_delete = request.POST.getlist('item')
        print(items_to_delete)
        Item.objects.filter(pk__in=items_to_delete).delete()
        items = Item.objects.exclude(is_deleted=True)
        context = {
            'items': items,
        }
        return render(request, 'items.html', context)


def item_view(request: WSGIRequest, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item.html', context={'item': item, 'status': Item.CHOICES})


def edit_view(request: WSGIRequest, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(initial={
        'description': item.description,
        'description_details': item.description_details,
        'state': item.state,
        'date_to_do': item.date_to_do
    })
    if request.method == 'GET':
        return render(request, 'edit_item.html',
                      context={'item': item, 'form': form})
    form = ItemForm(request.POST)
    if not form.is_valid():
        return render(request, 'edit_item.html',
                      context={'item': item, 'form': form})
    item.description = form.cleaned_data['description']
    item.description_details = form.cleaned_data['description_details']
    item.state = form.cleaned_data['state']
    item.date_to_do = form.cleaned_data['date_to_do']
    item.save()
    return redirect('show_item', pk=item.pk)


def delete_view(request: WSGIRequest, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'delete.html', context={'item': item})


def confirm_delete_view(request: WSGIRequest, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('show_items')
