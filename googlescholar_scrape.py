# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 09:16:17 2023

@author: maris
"""

import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime, timedelta


# this function for the getting inforamtion of the web page
def get_paperinfo(paper_url):

  #download the page
  response=requests.get(url,headers=headers)

  # check successful response
  if response.status_code != 200:
    print('Status code:', response.status_code)
    raise Exception('Failed to fetch web page ')

  #parse using beautiful soup
  paper_doc = BeautifulSoup(response.text,'html.parser')

  return paper_doc

# this function for the extracting information of the tags
def get_tags(doc):
  paper_tag = doc.select('[data-lid]')
  link_tag = doc.find_all('h3',{"class" : "gs_rt"})
  author_tag = doc.find_all("div", {"class": "gs_a"})
  age_tag = doc.find_all("span",{"class":"gs_age"})

  return paper_tag,age_tag,link_tag,author_tag

# it will return the title of the paper
def get_papertitle(paper_tag):
  
  paper_names = []
  
  for tag in paper_tag:
    name = tag.select('h3')[0].get_text()
    if "]" in name:
        name = name[name.rfind("]")+2:]
    paper_names.append(name)

  return paper_names


# function for the getting link information
def get_link(link_tag):

  links = []

  for i in range(len(link_tag)) :
    if link_tag[i].a is None: 
        links.append('')    
    else:
        links.append(link_tag[i].a['href'])

  return links 

# function for the getting autho , year and publication information
def get_author_year_publi_info(authors_tag):
  years = []
  publication = []
  authors = []
  for i in range(len(authors_tag)):
      authortag_text = (authors_tag[i].text).split()
      if re.search(r'\d+', authors_tag[i].text) is not None:
          year = int(re.search(r'\d+', authors_tag[i].text).group())
      else:
          year = 0
      years.append(year)
      publication.append(authortag_text[-1])
      author = authortag_text[0] + ' ' + re.sub(',','', authortag_text[1])
      authors.append(author)
  
  return years , publication, authors


def get_pub_age(age_tag):
    ages = []
    gsdates = []
    for i in range(len(age_tag)):
        age = int(re.search(r'\d+', age_tag[i].text).group())
        ages.append(age)
        gsdatetime = datetime.now() + timedelta(days=-age)
        gsdate = gsdatetime.strftime("%m/%d/%Y")
        gsdates.append(gsdate)
    return ages, gsdates



# adding information in repository
def add_in_paper_repo(papername,year,author,publi,link,ages,gsdates):
  # creating final repository
  paper_repos_dict = {
                    'Paper Title' : [],
                    'Year' : [],
                    'Author' : [],
                    'Publication' : [],
                    'Url of paper' : [],
                    'GS date': [],
                    'Age upon search': []}
    
  paper_repos_dict['Paper Title'].extend(papername)
  paper_repos_dict['Year'].extend(year)
  paper_repos_dict['Author'].extend(author)
  paper_repos_dict['Publication'].extend(publi)
  paper_repos_dict['Url of paper'].extend(link)
  paper_repos_dict['GS date'].extend(gsdates)
  paper_repos_dict['Age upon search'].extend(ages)

  return pd.DataFrame(paper_repos_dict)


def scrape_google_scholar(search_terms):
    separator = "+and+"
    terms_string = separator.join(search_terms)
    
    for i in range (0,50,10):
    
      # get url for the each page
      url = "https://scholar.google.com/scholar?start={}&q={}&hl=en&scisbd=1&as_sdt=0,39".format(i,terms_string)
    
      # function for the get content of each page
      doc = get_paperinfo(url)
    
      # function for the collecting tags
      paper_tag,age_tag,link_tag,author_tag = get_tags(doc)
      
      # paper title from each page
      papername = get_papertitle(paper_tag)
    
      # year , author , publication of the paper
      year , publication , author = get_author_year_publi_info(author_tag)
      
      # url of the paper
      link = get_link(link_tag)
      
      # ages of the paper
      ages, gsdates = get_pub_age(age_tag)
    
      # add in paper repo dict
      final = add_in_paper_repo(papername,year,author,publication,link, ages, gsdates)
      
      # use sleep to avoid status code 429
      sleep(10)
      
      return final
  

search_terms = ["%22children%22", "emotion"]
output = scrape_google_scholar(search_terms)
  