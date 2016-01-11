#!/usr/bin/python -tt
# Brock Donovan 11/22/2015
##########################
#########################
# Write a script to scrape fb and tw data from site 
# and output its data in csv format for easy importing

from bs4 import BeautifulSoup
import lxml
from urllib2 import urlopen
import re
import csv  

# create soup of webpage data
def create_soup(url):
  html = urlopen(url).read()
  soup = BeautifulSoup(html, 'lxml')
  return soup

# get: First,Last,Party,State,Facebook,,Twitter,Videos,,Photos,Other
# write to file so don't need to return anything
def get_social(members,labels,file): 
  myfile = open(file,'wb')
  wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
  wr.writerow(labels)
  for member in members[1:]: 
    individual = []
    for i in member.select('td'):
      if i.getText() != ' \n':
        individual.append(i.getText().strip())
      elif i.select('[href]'):
        link = str(i.select('[href]')[0]).split('"')[1]
        individual.append(link)
    wr.writerow(individual)
  myfile.close()

def main():
  base_url_house = "http://govsm.com/w/House"
  base_url_senate = "http://govsm.com/w/senate"
  
  house_soup = create_soup(base_url_house)
  senate_soup = create_soup(base_url_senate)
  #get labels
  labels = []
  for i in house_soup.table.tr.find_all('th'):
      labels.append(i.string)
  labels = [item.strip() for item in labels if str(labels)]
  
  # get just table of reps
  reps = house_soup.table.find_all('tr')
  get_social(reps,labels,'house_social_accounts.csv')

  sens = senate_soup.table.find_all('tr')
  get_social(sens,labels,'senate_social_accounts.csv')


if __name__=="__main__":
  import sys 
  reload(sys)
  sys.setdefaultencoding("utf-8")
  main()