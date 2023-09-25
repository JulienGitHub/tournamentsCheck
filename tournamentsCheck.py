from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
from os.path import exists
import json

while True:
	try:		
		openTournaments = []
		if(exists('tournaments.json')):
			file_object = open('tournaments.json')
			openTournaments = json.load(file_object)
			file_object.close()
		page = requests.get('https://rk9.gg/events/pokemon')
		soup = BeautifulSoup(page.content, "html.parser")
		tournaments = soup.find_all('table', attrs={'id':'dtUpcomingEvents'})
		tbody = tournaments[0].find('tbody')
		if(tbody):
			trs = tbody.find_all('tr')
			for tr in trs:
				tds = tr.find_all('td')
				if(len(tds) == 5):
					tName = tds[2].text.replace('\n', '').lstrip(' ').rstrip(' ')
					linkRef = ''
					links = tds[4].find_all('a', href=True)
					for link in links:
						if('tcg' in link.text.lower()):
							linkRef = 'https://rk9.gg' + link['href']
					if(len(linkRef)>0):
						tournamentAlreadyDiscovered = False
						for tournament in openTournaments:
							if(tournament['url'] == linkRef):
								tournamentAlreadyDiscovered = True
							
						if(not(tournamentAlreadyDiscovered)):
							print('new Tournament!!!')
							newData = {'name':tName, 'url':linkRef, 'opened':'0'}
							openTournaments.append(newData)
							file_object = open('tournaments.json', 'w')
							json.dump(openTournaments, file_object, indent = 4, sort_keys=True, ensure_ascii=False)
							file_object.close()
			else:
				print('no news @ ' + datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
				time.sleep(15*60)
		else:
			print('no news @ ' + datetime.now().strftime("%Y/%m/%d - %H:%M:%S"))
			time.sleep(15*60)
	except Exception as e:
		print(e)
		file_object = open('exceptions.txt', 'a')
		file_object.write(str(e) + '\n')
		file_object.close()
