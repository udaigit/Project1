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
    title_content = request.GET #getting the contents from the page as a dictionary
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
            util.save_entry(title, content)
            return redirect(title_page, title)

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
    searchItem = request.GET['q'] #'q' is the name of the form element - see layout.html
    list_entry = util.list_entries() 
    found = match_exact(searchItem, list_entry)
    if found:
        #match found 
        return redirect(title_page, searchItem)
    else:
        #match not found
        #find all the matches of substrings from the list entries
        entries = match_substring(list_entry, searchItem)
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
            matches.append(item)   
    return matches
    

def title_page(request, title):
    #process the title and retrieve content   
    lines = util.get_entry(title)
    if lines:
        #extract and convert the title from cmd file
        m_title = extract_title(lines)
        title_html = markdown.markdown(m_title.group(1).strip())
        
        #extract and convert the body
        p_body = extract_body(lines.strip())
        body_html = markdown.markdown(p_body.group(1).strip())
        body_html = body_html.strip("\r")
        return render(request, "encyclopedia/title_page.html",\
                            {'title':title,'e_title':title_html,'md_html':body_html})
    else:
        return render(request,"encyclopedia/error_page.html",{"item":title})

#extracts the title from the markdown content         
def extract_title(contents):
    return re.match(r".*(#[ ]+[A-Za-z]+)(?:[.\*\.\f\n\r\t\w! ]*)", contents)

#extracts the title from the markdown content         
def extract_body(contents):
    return re.match(r".*#[ ]+(?:[A-Za-z]+)([./\*\(\)\]\[\.\-\f\n\r\t\w!# ]*)", contents)

old_title=""
#This page recieves the entry argument from index.html page
def edit_page(request, entry): #the variable names must be same in both files i.e., "entry"
    global old_title
    web_page = request.GET
    #Just display the title and content to the user. Title is not editable
    if not web_page:
        #process the title and retrieve content   
        lines = util.get_entry(entry)
        #save the title we are currently processing
        old_title = entry.strip()
        return render(request,"encyclopedia/edit_page.html", {'f_title':entry.strip(), 'f_body':lines.strip()})
    #Save the edited content after user saves the button. The title is same. A new file
    #with same title but old content is overwritted by the new content is created. 
    else:
        #content from text area
        lines = web_page['edit_desc']  
        util.save_entry(old_title, lines.strip())
        return redirect(title_page, old_title.strip())
