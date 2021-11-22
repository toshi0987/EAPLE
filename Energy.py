import csv
import datetime
import numpy as np

class Energy:
	def __init__(self):
		self.energyData()
		self.userData()
		self.dishData()
		
	def energyData(self):
		with open('data/energy.csv') as f:
			reader = csv.reader(f)
			temp_list = [row for row in reader]
		self.energy_label = temp_list[0]
		self.energy_list = [float(temp_list[1][i]) for i in range(6)]
		f.close()
		
	def userData(self):
		with open('data/user.csv') as f:
			reader = csv.reader(f)
			temp = [row for row in reader]
			self.userDataList = temp[1:]
		f.close()
		
	def postUserData(self, date, time, dish):
		with open('data/user.csv', 'a', newline='') as f:
			writer = csv.writer(f)
			writer.writerow([date, time, dish])
		f.close()
		self.userData()
			
	def dishData(self):
		with open('data/dish.csv') as f:
			reader = csv.reader(f)
			temp = [row for row in reader]
			self.dishData = temp[1:]
		self.dishLabel = np.array(self.dishData).T[0].tolist()
		
	def getWeek(self, From):
		date_list = From.split('/')
		From = datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
		To = From - datetime.timedelta(weeks=1)
		data_week = []
		temp = self.userDataList
		for data in self.userDataList:
			date_list = data[0].split('/')
			print(date_list)
			day = datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]))
			if (From >= day) and (day > To):
				data_week.append(data)
		return data_week
		
	def getDay(self, day):
		data_day = []
		temp = self.userDataList
		for data in self.userDataList:
			if day == data[0]:
				data_day.append(data)
		return data_day
	
	def getEnergyData(self, data_list):
		EnergyDataList = [ 0 for i in range(6)]
		for data in data_list:
			for i, j in enumerate(self.dishData[self.dishLabel.index(data[2])]):
				if i != 0:
					EnergyDataList[i-1] += float(j)
		return EnergyDataList
	
	def getWeekList(self):
		now = datetime.datetime.now()
		weekList = []
		weekList.append(now.strftime("%m/%d"))
		for i in range(6):
			now = now - datetime.timedelta(days=1)
			weekList.append(now.strftime("%m/%d"))
		weekList.reverse()
		return weekList
	
	def OverAndShortEnergy(self):
		now = datetime.datetime.now()
		now = now.strftime("%Y/%m/%d")
		dayData = self.getDay(now)
		dayEnergyData = self.getEnergyData(dayData)
		dayEnergyData = (np.array(dayEnergyData)/len(dayData)).tolist()
		OverAndShort = []
		for (i, j) in zip(dayEnergyData, self.energy_list):
			OverAndShort.append((j/3-i)*len(dayData)+j/3)
		self.OverAndShort = OverAndShort
	
	
	def recommendDish(self):
		mini = 100000
		idx = 0
		self.OverAndShortEnergy()
		coefficientList = [ 1 for i in range(6)] #係数リスト #まだ使用していない
		for i, data in enumerate(self.dishData):
			data = [float(i) for i in data[1:]]
			tmp = sum(np.abs((np.array(self.OverAndShort)-np.array(data))).tolist())
			if tmp < mini:
				idx = i
				mini = tmp
		return self.dishData[idx]


c = Energy()
print(c.getWeekList())
print(c.dishData)
c.OverAndShortEnergy()
print(c.OverAndShort)
print(c.recommendDish())
"""
c.OverAndShortEnergy()
print(c.OverAndShort)
print(c.recommendDish())
print(c.userData)
print("------------------")
print(c.getWeek('2021/10/22'))
print("------------------")
print(c.getDay('2021/10/22'))
print("------------------")
print(c.dishData)
print("------------------")
print(c.dishLabel)
print("------------------")
print(c.getEnergyData(c.getDay('2021/10/22')))
"""