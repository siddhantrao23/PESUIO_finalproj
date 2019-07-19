from bs4 import BeautifulSoup
import requests
import csv

url = "https://karki23.github.io/Weather-Data/"		#url to scrape from

def scrape(link):		#scraping the particular link
	link_data = requests.get(url+link).text
	link_soup = BeautifulSoup(link_data, "lxml")
	table = link_soup.find('table')
	i=0
	rows_content = []

	for row in table.find_all('tr'):
		content = []
		if(i==0):
			for col in row.find_all('th'):
				content.append(col.text)
		else:
			for col in row.find_all('td'):
				if(col != []):
					content.append(col.text)
		rows_content.append(content)
		i+=1

	#writing table data to csv file
	with open("datasets/"+link.replace('.html','')+'.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(rows_content)


def main():
	data = requests.get(url+"assignment.html").text
	soup = BeautifulSoup(data, "lxml")
	for link in soup.find_all('a'):
		scrape(link.get("href"))

if(__name__ == "__main__"):
	main()