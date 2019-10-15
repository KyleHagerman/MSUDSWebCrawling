'''
Kyle Hagerman
Montana State University Dataset Search

This code is based on scripts written by Jason Clark.
It is used to scrape the web for skills by MSU researchers.
Targeted websites are:
    - Google Scholar
    - ORCiD
    - MS Academic
    - ResearchGate
    - LinkedIn

INPUT: This program will read a csv list of researchers in to search for their profiles as the second command line argument.
       The csv file should contain the institution as the first item in the list.

OUTPUT: This program will generate csv and JSON files for each researcher.

TODO: pull Jason's code back in for web scraping. We want to minimize dependencies
Make calls to WikiData API with python requests library.
Store data records in specified format.
Pull in csv list of researchers with institution at the beginning of the list / Prompt user of script to enter institution name?

'''

#imports
import sys
import scholarly #https://github.com/OrganicIrradiation/scholarly
import orcid #https://github.com/ORCID/python-orcid
import qwikidata #https://qwikidata.readthedocs.io/en/stable/index.html
import requests
import json
import urllib
import urllib3
from bs4 import BeautifulSoup

#this method reads the input, if there is none then find Jason
def readInput(filepath):
  file = open(filepath, "r")
  csv_researchers = file.read()
  researchers = csv_researchers.split(",", -1)
  for x in range(len(researchers)):
    if x is not 0:
      researchers[x] = researchers[0] + ", " + researchers[x]
  return researchers

#set any variables required to crawl the web
def crawlingSetUp():
  pass

#crawl Google Scholar for skills
def crawlGoogleScholar(researcher, header_list):
  formatted_researcher = formatStringForSearch(researcher)
  print("Formatted researcher: " + formatted_researcher)
  uri = "https://scholar.google.com/citations?view_op=search_authors&mauthors=" + formatted_researcher + "&hl=en&oi=ao"
  print(uri)
  request = requests.get(uri, headers=header_list)
  #request = requests.get(uri, headers={'User-Agent' : 'jasonclark.info indexing bot'})

  #check for HTTP codes other than 200
  if request.status_code != 200:
      print('Status:', request.status_code, 'Problem with the request. Exiting.')
      exit()

  soup = BeautifulSoup(request.text, 'html.parser')

  for link in soup.find_all(class_='gs_ai gs_scl gs_ai_chpr'):
    URI_tail = link.a['href']
    break
      # tagValue = link.string.strip('\r\n\t')
      # print('skill data: \n' + tagValue)
      # skillList.append({"skill": tagValue, "length": len(tagValue)})

  URI_head = "https://scholar.google.com/"

  uri = URI_head + URI_tail

  request = requests.get(uri, headers=header_list)

  soup = BeautifulSoup(request.text, 'html.parser')

  pageTitle = soup.title.string
  pageFileName = pageTitle.replace(' ', '-').lower()

  print ('Page Title: \n' + pageTitle)
  # print("Soup: ")
  # print(soup)
  # print ('Page URL: \n' + uri)

  #set empty list for about json values
  skillList = []

  #old class: gsc_prf_ila
  #new class: gsc_prf_inta
  for link in soup.find_all(class_='gsc_prf_inta'):
      tagValue = link.string.strip('\r\n\t')
      print('skill data: \n' + tagValue)
      skillList.append({"skill": tagValue, "length": len(tagValue)})

  return skillList

#crawl ORCiD for skills
def crawlORCiD():
  #get authorization code https://members.orcid.org/api/oauth/3legged-oauth
  pass

#crawl MS Academic for skills
def crawlMSAcademic():
  pass

#crawl Research Gate for skills
def crawlResearchGate():
  pass

#crawl LinkedIn for skills
def crawlLinkedIn():
  #get authorization code https://docs.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow
  pass

#make a call to Wiki Data to retrieve a URI for a specific skill
def callWikiData(header_list, skill):
  #need to build uri for query and add skill to it
  formatted_skill = formatStringForSearch(skill)

  print("Formatted Skill in WikiData call: " + formatted_skill)

  URI_head = "http://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&titles="
  URI_tail = "&format=json&normalize=&languages=en"
  Full_URI = URI_head + formatted_skill + URI_tail
  print("Full URI: " + Full_URI)

  request = requests.get(Full_URI, headers=header_list)

  if request.status_code != 200:
      print('Status:', request.status_code, 'Problem with the request. Exiting.')
      exit()

  contents = request.json()
  entities = contents["entities"]
  #print(request.content)
  # response = urlopen(request)
  # contents = json.loads(response.read())
  # print(response)
  #print(contents)

  for entity in entities:
    return entity

#generate the csv and JSON files for each researcher
def generateOutput():
  pass

def formatStringForSearch(string_with_space):
  pieces = string_with_space.split(" ")
  string_with_plus = pieces[0]
  for chunk in range(1, len(pieces)):
    string_with_plus = string_with_plus + "+" + pieces[chunk]

  return string_with_plus

#orchestrates the script
def main():
  print("In the main method...")
  if len(sys.argv) > 2:
    researchers = readInput(sys.argv[2])
  else:
    researchers = ["Montana State University", "Jason A. Clark"]

  header_list = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

  # callWikiData(header_list, "machine learning")
  # pass

  for researcher in range(1, len(researchers)):
    researcher_skills = []
    print("Calling Google Scholar method...")
    retrieved_skills = crawlGoogleScholar(researchers[researcher], header_list)
    for skill in range(len(retrieved_skills)):
      researcher_skills.append(retrieved_skills[skill])

    print("Skill List: ")
    print(researcher_skills)

    skillAdded = 0
    for skill in range(len(researcher_skills)):
      if skillAdded is 0:
        URI = callWikiData(header_list, researcher_skills[skill])
        researcher_skills.insert(skill + 1, URI)
        skillAdded = 1
      else:
        skillAdded = 0
        continue

    print("Skills with URI's: ")
    print(researcher_skills)

  '''
  Jason's code for file creation...


  #create json file if it doesn't exist, open and write parsed values into it
  if not os.path.exists(pageTitle+'-skills.json'):
      open(pageFileName+'-skills.json', 'w').close()

  with open(pageFileName+'-skills.json', 'r+') as jsonFile:
      json.dump(skillList, jsonFile, indent = 4)

  jsonFile.close()

  #create csv file if it doesn't exist, open and write parsed values into it
  if not os.path.exists(pageTitle+'-skills.csv'):
      open(pageFileName+'-skills.csv', 'w').close()

  with open(pageFileName+'-skills.csv', 'r+') as csvFile:
      writeFile = csv.writer(csvFile)
      writeFile.writerow(skillList)

  csvFile.close()
  '''

if __name__ == "__main__":
  main()
