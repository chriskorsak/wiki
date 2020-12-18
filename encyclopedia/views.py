from django.shortcuts import render, redirect
from django.http import HttpResponse

from django import forms
from . import util
from markdown2 import Markdown
import random


class searchForm(forms.Form):
  # here you define all the form inputs you want the user to fill out:
  # CharField is a text input with a label of 'query'
  #the variable 'query' has to be the name of the input on the html form
  query = forms.CharField()

class newEntryForm(forms.Form):
  title = forms.CharField()
  content = forms.CharField()

class editEntryForm(forms.Form):
  pageTitle = forms.CharField()

def index(request):
  return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
  })

def entry(request, title):
  if util.get_entry(title):

    ### use imported markdown package to convert markdown to html
    markdowner = Markdown()
    entryText = util.get_entry(title)
    entryText = markdowner.convert(entryText)
    ### end markdown pacakage conversion code

    return render(request, "encyclopedia/entry.html", {
      "entryText": entryText,
      "pageTitle": title
    })
  else:
    return render(request, "encyclopedia/error.html", {
      "errorMessage": f"{title} not found."
    })

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
      # return render(request, "encyclopedia/error.html")

def new(request):
  if request.method == "POST":
    #get form inputs (title, content)
    form = newEntryForm(request.POST)
    if form.is_valid():
      title = form.cleaned_data["title"]
      content = form.cleaned_data["content"]
      #test to see if file name already exists:
      if not util.get_entry(title):
        util.save_entry(title, content)
        return redirect("/" + title)
      else:
        return render(request, "encyclopedia/error.html", {
          "errorMessage": f"A page named {title} already exists."
        })   
  return render(request, "encyclopedia/new.html")

def edit(request):
  if request.method == "POST":
    form = editEntryForm(request.POST)
    if form.is_valid():
      title = form.cleaned_data["pageTitle"]
      return render(request, "encyclopedia/edit.html", {
        "entryText": util.get_entry(title),
        "pageTitle": title
      })

def update(request):
    if request.method == "POST":
      #get form inputs (title, content)
      #using same class for updating as when first creating entry 'newEntryForm'
      form = newEntryForm(request.POST)
      if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        util.save_entry(title, content)
        return redirect("/" + title)

def randomPage(request):
  #get number of entries for random number range
  entries = util.list_entries()
  entryCount = len(entries)
  #create random index variable. minus 1 to not go outside of list range
  randomIndex = random.randint(0, entryCount) - 1
  #assign random index value to title variable
  title = (entries[randomIndex])
  return redirect("/" + title)

