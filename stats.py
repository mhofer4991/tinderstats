import matplotlib.pyplot as plt
import numpy as np
import http.client
import re
import sys
import jsonpickle
import pylab
from pathlib import Path
from pylab import polyfit, poly1d
from scipy import stats
import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def days_between(d1):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = date.today()
    rdelta = relativedelta(d2, d1)
    #return abs((d2 - d1).days)
    return rdelta.years

def plotHist(x,y):
	
	plt.bar(x, y)
	plt.xlabel('Age')
	plt.ylabel('Amount of matches')
	plt.title("Age of gurls")
	plt.grid()
	plt.tight_layout()			
	plt.savefig("ages.png")
	plt.close()

def plotNames(name_dict):

	sorted_r = [(k, name_dict[k]) for k in sorted(name_dict, key=name_dict.get, reverse=False)]
	sorted_r = list(filter(lambda x: x[1] > 1,sorted_r))
	sorted_r = sorted_r[(len(sorted_r) - 5):]
	#print(sorted_r)
	sorted_d = dict(sorted_r)
	
	names = list(sorted_d.keys())
	values = list(sorted_d.values())
	y_pos = np.arange(len(names))
		
	plt.barh(y_pos, values)
	plt.gca().set_yticks(y_pos)
	plt.gca().set_yticklabels(names)
	plt.title('Top 5 Name of gurls')
	plt.xlabel('Amount')
	plt.tight_layout()
	plt.savefig("names.png")
	#plt.show()
	plt.close()

def plotBios(name_dict):

	sorted_r = [(k, name_dict[k]) for k in sorted(name_dict, key=name_dict.get, reverse=False)]
	sorted_r = list(filter(lambda x: x[1] > 1,sorted_r))
	#sorted_r = sorted_r[(len(sorted_r) - 5):]
	#print(sorted_r)
	sorted_d = dict(sorted_r)
	
	names = list(sorted_d.keys())
	values = list(sorted_d.values())
	y_pos = np.arange(len(names))
		
	plt.barh(y_pos, values)
	plt.gca().set_yticks(y_pos)
	plt.gca().set_yticklabels(names)
	plt.title('Top 5 Name of gurls')
	plt.xlabel('Amount')
	plt.tight_layout()
	plt.savefig("bios.png")
	plt.show()
	plt.close()

def plotWeekdays(name_dict):

	sorted_r = [(k, name_dict[k]) for k in sorted(name_dict, key=name_dict.get, reverse=False)]
	sorted_r = list(filter(lambda x: x[1] > 1,sorted_r))
	#print(sorted_r)
	sorted_d = dict(sorted_r)
	
	names = list(sorted_d.keys())
	values = list(sorted_d.values())
	y_pos = np.arange(len(names))
		
	plt.barh(y_pos, values)
	plt.gca().set_yticks(y_pos)
	plt.gca().set_yticklabels(names)
	plt.title('Matches per week day')
	plt.xlabel('Amount')
	plt.tight_layout()
	plt.savefig("weekdays.png")
	#plt.show()
	plt.close()

def plot_dates(x, y):
	
	fit = polyfit(x, y, 1)
	fit_fn = poly1d(fit)
	
	plt.plot(x, y, x, fit_fn(x), 'k')
	plt.xlabel('Number of weeks after installation')
	plt.ylabel('Matches')
	plt.title("Matches per week")
	plt.grid()
	plt.tight_layout()			
	plt.savefig("dates.png")
	plt.close()

def plot_dates2(x, y):
	
	plt.plot(x, y)
	plt.xlabel('Number of weeks after installation')
	plt.ylabel('Matches')
	plt.title("Matches per week")
	plt.grid()
	plt.tight_layout()			
	plt.savefig("dates2.png")
	plt.close()

filename = "input.json"
if len(sys.argv) > 1:
	filename = sys.argv[1]

text = ""

with open(filename, "r", encoding="utf8") as input:
	text = input.read()

obj = json.loads(text)

matches = obj['matches']

ages = list(map(lambda x: [x['id'], days_between(x['person']['birth_date'].split('T')[0])],matches))

age_count = np.zeros(30, dtype=np.int)
age_count = list(age_count)

for age in ages:
	age_count[age[1]] = age_count[age[1]] + 1

plotHist(np.arange(30)[18:30], age_count[18:30])


names = list(map(lambda x: [x['id'], x['person']['name']], matches))
name_dict = {}

for name in names:
	tname = name[1]
	if tname in name_dict:
		name_dict[tname] = name_dict[tname] + 1
	else:
		name_dict[tname] = 1

plotNames(name_dict)

created_dates = list(map(lambda x: (x['id'], datetime.strptime(x['created_date'].split('T')[0], "%Y-%m-%d")), matches))
created_dates = sorted(created_dates, key=lambda x: x[1])

weeks = int((datetime.today() - created_dates[0][1]).days/7)
print(weeks)
weeks_map = np.zeros(weeks + 1, dtype=np.int)

for date in created_dates:
	tdate = date[1]
	diff = int((datetime.today()- tdate).days/7)
	diff2 = weeks - diff
	weeks_map[diff2] = weeks_map[diff2] + 1

plot_dates(np.arange(weeks + 1), weeks_map)
weeks_map2 = list(weeks_map)

for i in range(1, len(weeks_map2)):
	weeks_map2[i] = weeks_map2[i - 1] + weeks_map2[i]
	
plot_dates2(np.arange(weeks + 1), weeks_map2)

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekdays_map = np.zeros(7, dtype=np.int)
weekdays_dict = {}

for date in created_dates:
	tdate = date[1]
	weekdays_map[tdate.weekday()] = weekdays_map[tdate.weekday()] + 1

for i in range(0, len(weekdays_map)):
	weekdays_dict[weekdays[i]] = weekdays_map[i]

plotWeekdays(weekdays_dict)



main_photos = list(map(lambda x: x['person']['photos'][0]['url'], matches))

with open('links.txt','w') as file:
	file.write("\n".join(main_photos))

matches_with_bio = list(filter(lambda x: 'bio' in x['person'],matches))
bios = list(map(lambda x: x['person']['bio'], matches_with_bio))
bios = list(map(lambda x: x.split(" "), bios))
bios = list(map(lambda x: list(set(x)), bios))
bios_dict = {}

for bio in bios:
	ta = list(filter(lambda x: len(x) >= 1,bio))
	for word in ta:
		tbio = word
		if tbio in bios_dict:
			bios_dict[tbio] = bios_dict[tbio] + 1
		else:
			bios_dict[tbio] = 1

#plotBios(bios_dict)

print(bios)


print(weekdays_map)
print(weeks_map)
print(weeks_map2)
#print(len(ages))
#print(age_count)

#print(obj)