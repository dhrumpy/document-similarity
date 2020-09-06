import requests  
import re
from bs4 import BeautifulSoup  
import time
from time import sleep

import warnings
warnings.filterwarnings('ignore')


url = 'https://pubmed.ncbi.nlm.nih.gov/?term=neurodegenerative+diseases&filter=simsearch1.fha&size=100'
r = requests.get(url)
print('Connecting to pubmed database...')
soup = BeautifulSoup(r.text, 'html.parser')
result = soup.find('meta', attrs={'name': 'log_displayeduids'})
PMIDs = result.attrs['content'].split(',')

base_url = 'https://pubmed.ncbi.nlm.nih.gov/'
endpoints = [base_url+ PMID for PMID in PMIDs]

nAbstract = 100

start = time.time()
print('Getting all top {} abstracts, related to the key word "neurodegenerative diseases":'.format(nAbstract))
with open('corpus.txt', 'a+') as file_object:
    for i in range(nAbstract):
        sleep(3)
        url = endpoints[i]
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = soup.find('div', attrs={'class': 'abstract'})
        nStrong = len(result.find_all('strong'))

        strongs = [result.find_all('strong')[i].contents[0] for i in range(nStrong)]
        strongs = [re.sub('\n', '', strong).strip() for strong in strongs]
        try:
            strongs.remove('Keywords:')
        except:
            pass

        text = result.getText()
        text = re.sub('\n', '', text)
        text = text.split('Abstract')[1]
        text = text.split('Keywords')[0]
        text = re.sub('  ', '', text)

        if not len(strongs):
            text = text.lower()
            file_object.write(text)
            file_object.write('\n')
        else:
            for idx, strong in enumerate(strongs):
                if idx==0:
                    text = re.sub(strong, '', text)
                else: 
                    text = re.sub(strong, ' ', text)
            
            text = text.lower()
            file_object.write(text)
            file_object.write('\n')

        print('Abstract {} fetched, PMID: {}'.format(i+1, PMIDs[i]))
            
      
            
       

file_object.close()
end = time.time()
print('Finished in {} seconds'.format(end-start))
