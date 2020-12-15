from django.shortcuts import render, redirect
from django.http import HttpResponse

from django import forms
from . import util

class searchForm(forms.Form):
    # here you define all the form inputs you want the user to fill out:
    # CharField is a text input with a label of 'query'
    query = forms.CharField()

def index(request):
  return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
  })

def entry(request, title):
  if util.get_entry(title):
    return render(request, "encyclopedia/entry.html", {
      "entryText": util.get_entry(title),
      "pageTitle": title
    })
  else:
    return render(request, "encyclopedia/error.html")

def search(request):
  if request.method == "POST":
    form = searchForm(request.POST)
    if form.is_valid():
      query = form.cleaned_data["query"]
      if util.get_entry(query):
        return redirect("/" + query)
  return render(request, "encyclopedia/test.html")
