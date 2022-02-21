# coding: utf-8
"""
   joplin-web
"""
from django import forms
from django.conf import settings
from joppy.api import Api

joplin = Api(token=settings.JOPLIN_WEBCLIPPER_TOKEN)


def get_children_folders(my_folders, folders):
    for folder in folders:
        my_folders.append((folder['id'], '-> '+folder['title']))

    return my_folders


def get_folders():
    """

    """
    folders = joplin.get_all_notebooks()

    my_folders = []
    for folder in folders:
        my_folders.append((folder['id'], folder['title']))
        #if 'children' in folder:
        #    my_folders.append(get_children_folders(my_folders, folder['children']))

    return my_folders


def get_tags():
    """

    """
    tags = joplin.get_all_tags()

    my_tags = []
    for tag in tags:
        my_tags.append((tag['id'], tag['title']))

    return my_tags


class NoteForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        {'class': 'form-control', 'placeholder': 'Title'}))
    tags = forms.MultipleChoiceField(required=False,
                                     widget=forms.SelectMultiple({'class': 'form-control'}),
                                     choices=get_tags())
    parent_id = forms.ChoiceField(label="Folder",
                                  widget=forms.Select({'class': 'form-control'}),
                                  choices=get_folders())
    text = forms.CharField(widget=forms.Textarea({'class': 'form-control', 'rows': 20}))


class FolderForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Title'}))


class TagForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Title'}))

