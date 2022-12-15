from django.http import HttpResponseRedirect
from django.shortcuts import render
import markdown
from . import util
from random import choice


def index(request):
    """Function to make the home page.

    This index page shows the list of entries created by util.list_entries.
    The function util.list_entries returns all the available entries
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def convert_markdown_to_html(title):
    """Function to convert markdown to HTML.

    Check if the file exists. If it does not exist, return None.
    If the file does exist, convert it to HTML
    """
    content = util.get_entry(title)
    # Source: https://github.com/trentm/python-markdown2/blob/master/README.md
    markdowner = markdown.Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)


def entry(request, title):
    """ Function to show an error message if a page does not exist
    (or otherwise show entry page).
    """
    html_content = convert_markdown_to_html(title)
    if html_content is None:  # file does not exist
        return render(request, "encyclopedia/error.html", {
            # render an error message
            "error_message": "This entry does not exist."
        })
    else:  # if the HTML content is not none,
        # return the content of the markdown in the HTML file
        return render(request, "encyclopedia/entry.html", {
            "title": title,  # use variable to display
            # the title in an entry via entry.html
            # use this variable to display the content
            # #in an entry via entry.html
            "content": html_content
        })


def search(request):
    """ Function to search for an entry (or part of the
    word of that entry).
    """
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_markdown_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                # use variable to call request.POST['q']
                "title": entry_search,
                # use variable to call converting function with entry_search
                "content": html_content
            })
        else:
            # look in util.py for the list of all entries
            all_entries = util.list_entries()
            # create list with entries that contain a part of the search input
            similar_entries = []
            for entry in all_entries:
                # convert everything to lowercase to searches easier
                if entry_search.lower() in entry.lower():
                    # append similar entry in the list
                    similar_entries.append(entry)
            return render(request, "encyclopedia/search.html", {
                "similar_entries": similar_entries
            })


def new_page(request):
    """ Function to create a new entry. """
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        # create new variable to register new page title
        new_page_title = request.POST['title']
        # create new variable to register new page content
        new_page_content = request.POST['content']
        # use the get_entry function to check if the title already exists
        does_title_exist = util.get_entry(new_page_title)
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
    """ Function to edit a yet existing entry. """
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })


def save_edit(request):
    """ Function to save edit. """
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(f"/wiki/{title}")


def random_page(request):
    """ Function to show a random page. """
    all_entries = util.list_entries()
    random_entry = choice(all_entries)
    return HttpResponseRedirect(f"/wiki/{random_entry}")
