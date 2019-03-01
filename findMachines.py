import urllib2
from bs4 import BeautifulSoup

def get_Machines() :
	machines_page = 'https://apps.cs.utexas.edu/unixlabstatus/'
	html_page = urllib2.urlopen(machines_page)

	soup = BeautifulSoup(html_page, 'html.parser')

	machines_list = []
	for row in soup.find_all('tr') :
	 	machine_data = row.get_text(" ", strip="True").split()
		if machine_data[1] == "up" :
			make_float = float(machine_data[-1])
			machines_list.append((str(machine_data[0]), make_float))

	machines_list.sort(key=lambda tup: tup[1])
	return [machines_list[0][0], machines_list[1][0], machines_list[2][0], machines_list[3][0]]