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

'''

#imports
import sys
import scholarly #https://github.com/OrganicIrradiation/scholarly
import orcid #https://github.com/ORCID/python-orcid
import qwikidata #https://qwikidata.readthedocs.io/en/stable/index.html

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
def crawlGoogleScholar(researcher):
  search_query = scholarly.search_author(researcher)
  first_result = next(search_query).fill()
  #first_result.interests
  print(first_result.interests)

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
def callWikiData():
  #want to call 'pip install wptools' https://github.com/siznax/wptools
  #but running into countless errors
    #need pycurl
      #needs python 3.5
    #then try wptools
  pass

#generate the csv and JSON files for each researcher
def generateOutput():
  pass

#orchestrates the script
def main():
  print("In the main method...")
  if len(sys.argv) > 2:
    researchers = readInput(sys.argv[2])
  else:
    researchers = ["Montana State University", "Montana State University, Jason Clark"]

  for researcher in range(len(researchers)):
    if researcher is not 0:
      print("Calling Google Scholar method...")
      crawlGoogleScholar(researchers[researcher])

if __name__ == "__main__":
  main()
