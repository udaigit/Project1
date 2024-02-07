from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
import re
from . import util
import markdown
import random


def index(request):
    list_entry = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": list_entry
    })

"""
This function creates a new page and stores it in the entries folder
"""
def new_page(request):
    title_content = request.GET
    #check if None is being passed 
    exists = False
    try:
        title = title_content["title"]
        content=title_content["desc"]
    except MultiValueDictKeyError:
        return render(request, "encyclopedia/new_page.html")
    else:
        #check if the page entry already exists
        exists = check_exists(title)
        if exists:
            return render(request, "encyclopedia/new_page.html",{'exists':exists})
        else:
            #Add markdown title for the page
            content = f"# {title}\n"+content
            util.save_entry(title, content)
            return render(request, "encyclopedia/new_page.html",{'exists':exists})

#this function checks if the entry submitted by the user already exists or not
#Returns True if the entry exists and False if it does not.
def check_exists(entry):
    list_entry = util.list_entries()
    if entry in list_entry:
        return True
    else:
        return False

#generates a random title in the entries and renders it
def random_page(request):
    list_entry = util.list_entries()
    #choose a random entry from the list
    length = len(list_entry)
    rand_num = random.randint(0, length-1)
    title=list_entry[rand_num]
    return redirect(title_page, title)
   
#searches for a give title. If not found then search for substrings that match the title
#and if any display them to user as a list where they can click and go to that page
def search_page(request):
    #print("search_page method is called")
    searchItem = request.GET['q'] #'q' is the name of the form element - see layout.html
    #print(searchItem)
    list_entry = util.list_entries() 
    found = match_exact(searchItem, list_entry)
    if found:
        #match found 
        return redirect(title_page, searchItem)
    else:
        #match not found
        #find all the matches of substrings from the list entries
        entries = match_substring(list_entry, searchItem)
        #print ("Substring matching entries: ", entries)
        return render(request, "encyclopedia/search_page.html",\
                {"search":searchItem, "entries":entries})

#This function returns True for the first match found in list entries 
#It returns False if no matches are found in the list entries   
def match_exact(item, list_items):
    for element in list_items:
        if element.lower() == item.lower():
            return True
    return False

#returns the list of all items matching the search pattern entered by user
def match_substring(list_entry, searchItem):
    matches = list()
    for item in list_entry:
        if re.match(f".*{searchItem.lower()}.*",item.lower()):
            #print("matching item", item)
            matches.append(item)   
    return matches
    

def title_page(request, title):
    p_html=""
    #process the title and retrieve content   
    lines = util.get_entry(title)
    if lines:
        p_html = process(lines)
        p_title = extract_title_body(p_html)
        title_html = markdown_title_HTML(p_title)
        body_html = markdown_body_HTML(p_title)  
        return render(request, "encyclopedia/title_page.html",\
                            {'title':title,'e_title':title_html,'md_html':body_html})
    else:
        return render(request,"encyclopedia/error_page.html",{"item":title})

#processes the content to only include spaces
def process(content):
    p_html=""
    for letter in content:
            if not letter.isspace():
                p_html=p_html+letter
            else:
                p_html+=" "    
    return p_html

#extracts the title from the markdown content         
def extract_title_body(contents):
    return re.match(r".*#[ ]+([A-za-z]+)[ ]+(.+)$", contents, re.M)

#convert markdown title to HTML
def markdown_title_HTML(m):
    return markdown.markdown("#"+m.group(1))

#convert markdown body to HTML
def markdown_body_HTML(m):
    return markdown.markdown(m.group(2))