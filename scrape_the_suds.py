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
       ARG1: python
       ARG2: script_name
       ARG3: string of what institution you are targeting
       ARG4: CSV list or string of single researcher name
       User will be prompted to enter a number indicating the file output type

OUTPUT: This program will generate csv and JSON files for each researcher.

TODO: Store data records in specified format.
Pull in csv list of researchers with institution at the beginning of the list / Prompt user of script to enter institution name?

Pass another command line argument for file type at the end.
  either JSON, CSV, or SQL Insert Statment
  one file generated for each researcher, place in directory?
  create full program menu to prompt user for each input
    series of while loops for each input
    print outcome and ask user if it's what they meant to pass to the program
    take input until they confirm it's correct

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
import os.path

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
def crawlGoogleScholar(researcher, institution, header_list):
  #format strings for seaching
  formatted_researcher = formatStringForSearch(researcher)
  formatted_institution = formatStringForSearch(institution)
  print("Formatted researcher: " + formatted_researcher)
  print("Formatted institution: " + formatted_institution)

  #put the search URI together
  uri = "https://scholar.google.com/citations?view_op=search_authors&mauthors=" + formatted_researcher + "+" + formatted_institution + "&hl=en&oi=ao"
  print(uri)

  #make the HTTP request for the search
  request = requests.get(uri, headers=header_list)

  #check for HTTP codes other than 200
  if request.status_code != 200:
      print('Status:', request.status_code, 'Problem with the Google Scholar search request. Exiting.')
      exit()

  #retrieve the html to sort through
  soup = BeautifulSoup(request.text, 'html.parser')

  #find the first result in the search displayed on the page
  search_results = soup.find_all(class_='gs_ai gs_scl gs_ai_chpr')
  #pull the HTML link from the search result
  URI_tail = search_results[0].a['href']

  # for link in soup.find_all(class_='gs_ai gs_scl gs_ai_chpr'):
  #   URI_tail = link.a['href']
  #   break
      # tagValue = link.string.strip('\r\n\t')
      # print('skill data: \n' + tagValue)
      # skillList.append({"skill": tagValue, "length": len(tagValue)})

  #add the domain name for Google Scholar
  URI_head = "https://scholar.google.com/"

  #put the URI together
  uri = URI_head + URI_tail

  #make the second HTTP request for the researcher's profile page
  request = requests.get(uri, headers=header_list)

  #check for HTTP codes other than 200
  if request.status_code != 200:
      print('Status:', request.status_code, 'Problem with the Google Scholar profile request. Exiting.')
      exit()

  #get the HTML soup
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
def callWikiData(skill, header_list):
  #need to build uri for query and add skill to it
  formatted_skill = formatStringForSearch(skill)
  print("Formatted Skill in WikiData call: " + formatted_skill)

  #put the search query together
  URI_head = "http://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&titles="
  URI_tail = "&format=json&normalize=&languages=en"
  Full_URI = URI_head + formatted_skill + URI_tail
  print("Full URI: " + Full_URI)

  #make the HTTP request
  request = requests.get(Full_URI, headers=header_list)

  #if the request did not go through properly, inform the user and cancel
  if request.status_code != 200:
      print('Status:', request.status_code, 'Problem with the WikiData request. Exiting.')
      exit()

  contents = request.json()
  entities = contents["entities"]
  #print(request.content)
  # response = urlopen(request)
  # contents = json.loads(response.read())
  # print(response)
  #print(contents)
  for entity in entities:
    print("The entity you have reconciled: ")
    print(entity)
    return entity

#generate the csv and JSON files for each researcher
def generateOutput():
  pass

'''
This function formats strings by replacing spaces with "+" signs for use in URI's
'''
def formatStringForSearch(string_with_space):
  pieces = string_with_space.split(" ")
  string_with_plus = pieces[0]
  for chunk in range(1, len(pieces)):
    string_with_plus = string_with_plus + "+" + pieces[chunk]

  return string_with_plus

#orchestrates the script
def main():
  print("In the main method...")

  #exit condition for while loop, output type must be selected
  output_type_invalid = True

  #will run until file output type is valid
  while(output_type_invalid):

    #prompt user for file output type
    print("Please select a file output type by number. Your choices are:")
    print("1. CSV")
    print("2. JSON")
    print("3. SQL Insert")
    #get input
    output_type = input()

    #set file output type and apply exit condition
    if output_type is "1":
      output_type_invalid = False
      output_type = "CSV"
    elif output_type is "2":
      output_type_invalid = False
      output_type = "JSON"
    elif output_type is "3":
      output_type_invalid = False
      output_type = "SQL"
    else:
      #input was not valid, loop
      print("Invalid input. Please try again.")

  #initialize list to store input
  researchers = []
  #the institution we are filtering by
  institution = ""
  #if we have an argument for analysis, check if it's a file
  if len(sys.argv) > 3 and os.path.exists(sys.argv[3]) and os.path.isfile(sys.argv[3]):
    researchers = readInput(sys.argv[3])
    institution = sys.argv[2]
  #if its not a file, guess that its a string
  elif len(sys.argv) > 3:
    researchers.append(sys.argv[3])
    institution = sys.argv[2]
  #Jason and MSU is the default to test
  else:
    researchers = ["Jason A. Clark"]
    institution = "Montana State University"

  print("Your list of researchers: ")
  print(researchers)
  print("Your institution to filter by: " + institution)
  print()

  #set the list of headers to be sent in each HTTP request
  header_list = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

  #for each researcher in the list, find their skills and reconcile with WikiData
  for researcher in range(len(researchers)):
    researcher_skills = []
    print("Calling Google Scholar method...")
    retrieved_skills = crawlGoogleScholar(researchers[researcher], institution, header_list)
    for skill in range(len(retrieved_skills)):
      researcher_skills.append(retrieved_skills[skill])

    print("Skill List: ")
    print(researcher_skills)

    for skill in range(len(researcher_skills)):
      URI = callWikiData(researcher_skills[skill]['skill'], header_list)
      researcher_skills.insert(skill + 1, URI)

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

  OUTPUT SQL statement as text file with this as contents:
  INSERT INTO `datasets` (`recordInfo_recordIdentifier`, `dataset_category1`, `dataset_category1_URI`, `dataset_category2`, `dataset_category2_URI`, `dataset_category3`, `dataset_category3_URI`, `dataset_category4`, `dataset_category4_URI`, `dataset_category5`, `dataset_category5_URI`, `status`) VALUES ([value-1], [value-2], [value-3], [value-4], [value-5], [value-6], [value-7], [value-8], [value-9], [value-10], [value-11], `r`)
  '''

if __name__ == "__main__":
  main()
