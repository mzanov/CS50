from django.shortcuts import render , redirect
import random
import markdown2
from django.http import Http404, HttpResponse
from .forms import NewPageForm, EntryForm

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
# The entryPage method renders a page that displays the contents of that encyclopedia entry.
def entryPage(request, title):
        entry = util.get_entry(title)

        if entry is not None:
              html_content = markdown2.markdown(entry)
              return render(request, "encyclopedia/entry.html", {
            "entry": html_content,
            "entryTitle": title
        })
              
        
        raise Http404("Entry not found")

        
        
    
# Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.
def searchResults(request):
      query = request.GET.get('q','')
      matching_entries = []
      if query:
            entries = util.list_entries()
            matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
            
      if matching_entries:
            return redirect('entry_page', title = matching_entries[0])
      else:
            return render(request, "encyclopedia/search_result.html", {
            "query": query,
            "matching_entries": matching_entries
        })
      

# createNewPage method allows the user to click the Create New Page link to be taken to a page
# where the user can create a new encyclopedia entry
def createNewPage (request):
      if request.method == 'POST':
            form = NewPageForm(request.POST)
            if form.is_valid():
                  title = form.cleaned_data['title']
                  content = form.cleaned_data['content']

                  if util.get_entry(title):
                        raise Http404("Entry with this title already exists!")
                  
                  util.save_entry(title , content)

                  return redirect('entry_page', title=title)
            
      else:
            form = NewPageForm()
      return render(request, 'encyclopedia/createNewPage.html', { 
            'form': form  })
      

# editEntry method allows the user to click a link to be taken to a page
# where the user can edit that entry’s Markdown content in a textarea
def editEntry(request, title):
      entryContent = util.get_entry(title)
      if request.method == 'POST':
            form = EntryForm(request.POST)
            if form.is_valid():
                  content = form.cleaned_data["content"]
                  util.save_entry(title, content)
                  return redirect('entry_page', title=title)
            
      else:
            form = EntryForm(initial={'content': entryContent})
      return render(request, 'encyclopedia/editEntry.html', {
            'form': form, 'title': title    })


# randomEntry method takes a user to a random encyclopedia entry.
def randomEntry(request):
      entries = util.list_entries()
      randomEntry = random.choice(entries)
      return redirect('entry_page', title=randomEntry)
