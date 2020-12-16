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
    #assign searchForm class to form variable
    form = searchForm(request.POST)
    if form.is_valid():
      query = form.cleaned_data["query"]
      #check to see if search query is an esisting entry
      if util.get_entry(query):
        #redirect to entry url if so
        return redirect("/" + query)
      #return list of pages if substring is in entry, or error page
      else:
        #empty list, will be populated if substring in entry
        partialResults = []
        #get entries
        entries = util.list_entries()
        query = query.lower()

        for entry in entries:
          entry = entry.lower()
          if query in entry:
            partialResults.append(entry)
        return render(request, "encyclopedia/search.html", {
          "partialResults": partialResults
        })
      return render(request, "encyclopedia/error.html")
  # else:
  #   return render(request, "encyclopedia/error.html")

def new(request):
  return render(request, "encyclopedia/new.html")