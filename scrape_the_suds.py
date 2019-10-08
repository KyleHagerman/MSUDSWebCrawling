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

INPUT: this program will read a csv list of researchers in to search for their profiles as the second command line argument.

OUTPUT: this program will generate csv and JSON files for each researcher.

'''

#this method reads the input, if there is none then find Jason
def readInput(filepath):
  file = open(filepath, "r")
  csv_researchers = file.read()
  researchers = csv_researchers.split(",", -1)
  return researchers

#set any variables required to crawl the web
def crawlingSetUp():
  pass

#crawl Google Scholar for skills
def crawlGoogleScholar():
  pass

#crawl ORCiD for skills
def crawlORCiD():
  pass

#crawl MS Academic for skills
def crawlMSAcademic():
  pass

#crawl Research Gate for skills
def crawlResearchGate():
  pass

#crawl LinkedIn for skills
def crawlLinkedIn():
  pass

#make a call to Wiki Data to retrieve a URI for a specific skill
def callWikiData():
  pass

#generate the csv and JSON files for each researcher
def generateOutput():
  pass

#orchestrates the script
def main():
  if sys.argv[2]:
    researchers = readInput(sys.argv[2])
  else:
    researchers = ["Jason Clark"]

if __name__ == "main":
  main()
