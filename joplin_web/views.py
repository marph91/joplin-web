# coding: utf-8
"""
   joplin-web
"""
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from joppy.api import Api
from joplin_web.forms import NoteForm, FolderForm, TagForm
from joplin_web.utils import tag_for_notes
import logging

from rich import console
console = console.Console()

logger = logging.getLogger("joplin_web.app")

joplin = Api(token=settings.JOPLIN_WEBCLIPPER_TOKEN)


def home(request, *args, **kwargs):
    template_name = "index.html"
    form_folder = FolderForm()
    form_tag = TagForm()
    res = joplin.get_all_notes()
    notes = tag_for_notes(res)

    form = NoteForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            parent_id = form.cleaned_data['parent_id']
            tags = form.cleaned_data['tags']
            data = dict()
            data['tags'] = tags
            res = joplin.add_note(title=title, body=text, parent_id=parent_id, **data)
            form = NoteForm()
    else:
        form = NoteForm()

    context = {"notes": notes, "form": form, 'form_tag': form_tag, 'form_folder': form_folder}

    return render(request, template_name, context)


def edit_note_and_tags(request, note_id, *args, **kwargs):
    """
    edit one note and provide its tags too
    :param request
    :param note_id the note to modify
    :return HttpResponse
    """
    template_name = "index.html"
    # to keep only the data of the folder if provided
    folder_id = request.GET.get('folder_id', '')
    tag_id = request.GET.get('tag_id', '')
    if folder_id:
        notes = joplin.get_all_notes(notebook_id=folder_id)
        # res = joplin.get_folders_notes(folder_id)
        # notes = tag_for_notes(res)
    elif tag_id:
        notes = joplin.get_all_notes(tag_id=tag_id)
    else:
        notes = joplin.get_all_notes()

    note = joplin.get_note(note_id, fields="body,id,parent_id,title")

    data = note
    tags = joplin.get_all_tags(note_id=data['id'])

    if request.POST:
        form = NoteForm(request.POST, initial={'parent_id': data['parent_id']})
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            parent_id = form.cleaned_data['parent_id']
            data = dict()
            data['tags'] = form.cleaned_data['tags']
            res = joplin.modify_note(id_=note_id, title=title, body=text, parent_id=parent_id, **data)
            # res = joplin.update_note_tags(note_id=note_id, title=title, body=text, parent_id=folder, **data)
    else:
        form = NoteForm()
        tags_list = []
        for tag in tags:
            tags_list.append(tag['id'])
        form.initial['tags'] = tags_list
        form.initial['parent_id'] = data['parent_id']
        form.initial['title'] = data['title']
        form.initial['text'] = data['body']

    context = {"notes": notes,
               "note": note,
               "note_id": note_id,
               "folder_id": folder_id,
               "tag_id": tag_id,
               "form": form}

    return render(request, template_name, context)


def notes_folder(request, folder_id, *args, **kwargs):
    """
    get all the notes of that folder
    :param request
    :param folder_id: id of the folder we want to filter
    :return HttpResponse
    """
    template_name = "index.html"
    res = joplin.get_all_notes(notebook_id=folder_id)
    form = NoteForm()
    context = {"notes": res, "form": form, 'folder_id': folder_id}
    return render(request, template_name, context)


def notes_tag(request, tag_id, *args, **kwargs):
    """
    get all the notes of that tag
    :param request
    :param tag_id: id of the tag we want to filter
    :return HttpResponse
    """
    template_name = "index.html"
    res = joplin.get_all_notes(tag_id=tag_id)
    form = NoteForm()
    context = {"notes": res, "form": form, 'tag_id': tag_id}

    return render(request, template_name, context)


def create_folder(request):
    form = FolderForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            title = form.cleaned_data['title']
            joplin.add_notebook(title=title)
    return HttpResponseRedirect(reverse('home'))


def create_tag(request):
    form = TagForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            title = form.cleaned_data['title']
            joplin.add_tag(title=title)
    return HttpResponseRedirect(reverse('home'))


def delete_note(request, note_id, *args, **kwargs):
    """
    delete a note
    :param request
    :param note_id: id of the folder we want to delete
    :return HttpResponse
    """
    joplin.delete_note(note_id)
    return HttpResponseRedirect(reverse('home'))


def delete_tag(request, tag_id, *args, **kwargs):
    """
    delete a tag
    :param request
    :param tag_id: id of the tag we want to delete
    :return HttpResponse
    """
    joplin.delete_tag(tag_id)
    return HttpResponseRedirect(reverse('home'))


def delete_folder(request, folder_id, *args, **kwargs):
    """
    delete a folder
    :param request
    :param folder_id: id of the folder we want to delete
    :return HttpResponse
    """
    joplin.delete_notebook(folder_id)
    return HttpResponseRedirect(reverse('home'))
