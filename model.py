import glob
import numpy as np 
import pandas as pd
import csv
from os import path
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from warnings import simplefilter


head = """Date Location	MinTemp	MaxTemp Rainfall Evaporation Sunshine WindGustDir WindGustSpeed
			WindDir9am WindDir3pm WindSpeed9am WindSpeed3pm	Humidity9am	Humidity3pm	Pressure9am	Pressure3pm	
			Cloud9am Cloud3pm Temp9am Temp3pm RainToday RISK_MM	RainTomorrow""".split()

def split():
	files = glob.glob('datasets/*')
	for file in files:
		data = []
		with open(file, 'r', newline='') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				data.append(row)
		data = np.array(data)

		#removing header row
		data = np.delete(data, 0, 0)

		#splitting the datasets into test and train
		train, test = train_test_split(data, test_size = 0.2, shuffle = True)

		with open('train.csv', 'a', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(train)
		with open('test.csv', 'a', newline='') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(test)

def features(df):
	#feature engineering

	cities = """Adelaide Albany Albury AliceSprings BadgerysCreek Ballarat Bendigo Brisbane Cairns Canberra Cobar
			CoffsHarbour Dartmoor Darwin GoldCoast Hobart Katherine Launceston Melbourne MelbourneAirport Mildura
			Moree MountGambier MountGinini Newcastle Nhil NorahHead NorfolkIsland Nuriootpa PearceRAAF Penrith
			Perth PerthAirport Portland Richmond Sale SalmonGums Sydney SydneyAirport Townsville Tuggeranong
			Uluru WaggaWagga Walpole Watsonia Williamtown Witchcliffe Wollongong Woomera""".split()
	wind = "SW SSW NNE WNW N WSW W S ESE NE NNW SSE ENE NW E SE".split()

	df = df.fillna(0)
	df = df.fillna(df.median())

	df = df.replace(to_replace = 'No', value = 0)
	df = df.replace(to_replace = 'Yes', value = 1)
	
	i_range = [i for i in range(len(cities))]
	d = dict(zip(cities, i_range))
	df = df.replace(d)

	i_range = [i for i in range(len(wind))]
	d = dict(zip(wind, i_range))
	df = df.replace(d)

	df = df.drop(columns="Date")
	return df

def linear():

	#linear regression training
	df = pd.read_csv('train.csv', names = head)

	df = features(df)
	X = df.iloc[:, 0:22].values
	y = df.iloc[:, 22:23].values
	y = y.reshape(y.shape[0], )

	clf = LinearRegression().fit(X,y)
	return(clf)	

def logistic():
	#logistic regression training
	simplefilter(action='ignore', category=FutureWarning)		#to silence the solver warning
	df = pd.read_csv('train.csv', names = head)

	df = features(df)
	X = df.iloc[:, 0:22].values
	y = df.iloc[:, 22:23].values
	y = y.reshape(y.shape[0], )

	clf = LogisticRegression().fit(X,y)
	return(clf)	

def main():
	
	if(not(path.exists('test.csv') or path.exists('train.csv'))):
		split()
	clf1 = linear()
	clf2 = logistic()	
	
	df = pd.read_csv('test.csv', names = head)
	df = features(df)
	X = df.iloc[:, 0:22].values
	y = df.iloc[:, 22:23].values
	y = y.reshape(y.shape[0], )

	print("Linear model accuracy: ", clf1.score(X, y))
	print("Logistic model saccuracy: ", clf2.score(X, y))


if(__name__ == "__main__"):
	main()