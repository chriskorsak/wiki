from django.shortcuts import render
from django.http import HttpResponse


from . import util


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
