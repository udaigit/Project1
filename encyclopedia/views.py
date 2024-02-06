from django.shortcuts import render, redirect
import re
from . import util
import markdown
from html.parser import HTMLParser
import random


def index(request):
    list_entry = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": list_entry
    })

def new_page(request):
    return render(request, "encyclopedia/new_page.html")

#generates a random title in the entries and renders it
def random_page(request):
    list_entry = util.list_entries()
    #choose a random entry from the list
    length = len(list_entry)
    rand_num = random.randint(0, length-1)
    title=list_entry[rand_num]
    return redirect(title_page, title)
   
#def error_page(request):
    #print("error_page view invoked")
    #return render(request,"encyclopedia/error_page.html" )

def search_page(request):
    print("search_page method is called")
    searchItem = request.GET['q'] #'q' is the name of the form element - see layout.html
    print(searchItem)
    list_entry = util.list_entries() 
    found = False
    if searchItem in list_entry:
        found = True
        return redirect(title_page, searchItem)
    else:
        return render(request, "encyclopedia/search_page.html",\
                {"found":found, "search":searchItem})

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