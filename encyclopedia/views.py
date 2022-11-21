from django.http import HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown
import markdown 
from . import util
from random import choice
""" use 'from django.shortcuts import render' to import the render function to render a page
    import the 'Markdown' function from Markdown2 to convert markdown to HTML
    'from . import util' --> the dot means: from the same file directory import this module
    'import random' helps to randomly choose between the entries in the random function
"""

def index(request):
    """Function to make the home page
    
    This index page shows the list of entries created by util.list_entries.
    The function util.list_entries returns all the available entries
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert_markdown_to_html(title):
    """Function to convert markdown to HTML
    
    Check if the file exists. If it does not exist, return None. If the file does
    exist, convert it to HTML
    """
    content = util.get_entry(title)
    # Source: https://github.com/trentm/python-markdown2/blob/master/README.md
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def entry(request, title):
    """ Function to show an error message if a page does not exist (or otherwise 
    show entry page
    
    Call the convert_markdown_to_html function, because this function tells us
    if the page does alraedy exist and if so, it returns the HTML content
    """
    html_content = convert_markdown_to_html(title)
    if html_content == None: # file does not exist
        return render(request, "encyclopedia/error.html", {
            "error_message": "This entry does not exist." # render an error message
        })
    else: # if the HTML content is not none, return the content of the markdown in the HTML file
        return render(request, "encyclopedia/entry.html", {
            "title": title, # use variable to display the title in an entry via entry.html 
            "content": html_content # use this variable to display the content in an entry via entry.html
        })

def search(request):
    """ Function to 
    Use request.POST['q'] because q is the name of the variable in the form (see
    layout.html)
    """
    if request.method == "POST": 
        entry_search = request.POST['q']
        html_content = convert_markdown_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search, # use variable to call request.POST['q']
                "content": html_content # use variable to call converting function with entry_search
            })
        else:
            all_entries = util.list_entries() # look in util.py for the list of all entries 
            similar_entries = [] # create list with entries that contain a part of the search input
            for entry in all_entries:
                if entry_search.lower() in entry.lower(): # convert everything to lowercase to searches easier
                        similar_entries.append(entry) # append similar entry in the list
            return render (request, "encyclopedia/search.html", {
                "similar_entries": similar_entries
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        new_page_title = request.POST['title'] # create new variable to register new page title
        new_page_content = request.POST['content'] # create new variable to register new page content
        does_title_exist = util.get_entry(new_page_title) # use the get_entry function to check if the title already exists 
        if does_title_exist is not None:
            return render(request, "encyclopedia/error.html", {
                "error_message": "This page does already exist"
            })
        else: 
            util.save_entry(new_page_title, new_page_content)
            html_content = convert_markdown_to_html(new_page_title)
            return render(request, "encyclopedia/entry.html", {
                "title": new_page_title,
                "content": html_content
            })

def edit_page(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "title": title, 
            "content": content 
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(f"/wiki/{title}")
        
def random_page(request):
    all_entries = util.list_entries()
    random_entry = choice(all_entries)
    return HttpResponseRedirect(f"/wiki/{random_entry}")

# Personal notes
""" Each encyclopedia entry will be saved as a markdown file inside the entries' 
directory. Each entry page should be converted to html before being displayed.
To do this, use the markdown library and use the markdown.converter() function.

Line 72: convert everything to lowercase to make it easier to search

Line 60: use request.method == "POST" to check what the method is that is being used

"""