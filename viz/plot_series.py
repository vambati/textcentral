import matplotlib.pyplot as plt
import time
import calendar
import sys
import datetime
import numpy as np

f = open(sys.argv[1],"r")

x = []
y =  [] 

for s in f:
	print s
	date,val = s.split('\t')
	datestamp = time.strptime(date.strip(), "%Y %m %d") 
	days = datestamp.tm_year * 365 + datestamp.tm_mon * 30 + datestamp.tm_mday
	print days,datestamp
	x.append(days)
	y.append(val)

# Sort y based on sorting x 
x,y = zip(*sorted(zip(x, y)))

x =  np.array(x)
y = np.array(y)

plt.title("Tweets on PayPal")
plt.ylabel("Tweets")
plt.grid(True)
plt.plot(x,y)
plt.show()

