def scrap():
	def notifyme(title,message):
		plyer.notification.notify(title=title,
			message=message,
			app_icon=kingbondl.ico,
			timeout=20)
	url='https://www.worldometers.info/coronavirus/'
	r=requests.get(url)
	#print(r.text)       Print the response in console
	soup=BeautifulSoup(r.content,'html.parser')
	#print(soup.prettify())
	tablebody=soup.find('tbody')
	#print(tablebody) it will give data in table format
	ttt=tablebody.find_all('tr')
	#print(ttt)		it will give data in list format
	notifycountry=data_country.get()
	if(notifycountry==''):
		notifycountry='india'
	countries,total_cases,new_cases,total_deaths,new_deaths,total_recovered,active_cases=[],[],[],[],[],[],[]
	serious,totalcases_permillion,totaldeaths_permillion,totaltests,totaltests_permillion=[],[],[],[],[]
	headers=['countries','total_cases','new_cases','total_deaths','new_deaths','total_recovered','active_cases','serious','totalcases_permillion','totaldeaths_permillion','totaltests','totaltests_permillion']

	for i in ttt:
		id=i.find_all('td')  		
		#print(id[0].text)				print data, 0 index data to change in text format
		if(id[0].text.strip().lower()==notifycountry):
			totalcases1=int(id[1].text.strip().replace(',',''))
			totaldeaths1=id[3].text.strip()
			newcases1=id[2].text.strip()
			newdeaths1=id[4].text.strip()
			notifyme('corona virus Deaths in {}'.format(notifycountry),'totalcase:{}\n total deaths:{}\n New cases:{}\n New deaths:{}'.format(totalcases1,totaldeaths1,newcases1,newdeaths1))

		countries.append(id[0].text.strip())
		total_cases.append(int(id[1].text.strip().replace(',', '')))
		new_cases.append(id[2].text.strip())
		total_deaths.append(id[3].text.strip())
		new_deaths.append(id[4].text.strip())
		total_recovered.append(id[5].text.strip())
		active_cases.append(id[6].text.strip())
		serious.append(id[7].text.strip())
		totalcases_permillion.append(id[8].text.strip())
		totaldeaths_permillion.append(id[9].text.strip())
		totaltests.append(id[10].text.strip())
		totaltests_permillion.append(id[11].text.strip())
	#print(countries)
	#print(total_cases)

	df=pd.DataFrame(list(zip(countries,total_cases,new_cases,total_deaths,new_deaths,total_recovered,active_cases,serious,totalcases_permillion,totaldeaths_permillion,totaltests,totaltests_permillion)),columns=headers)
	sor=df.sort_values('total_cases',ascending=False)
	for k in formatlist:
		if(k=='html'):
			path2='{}/alldata.html'.format(path)
			sor.to_html(r'{}'.format(path2)) # r-- read

		if(k=='json'):
			path2='{}/alldata.json'.format(path)
			sor.to_json(r'{}'.format(path2)) # r-- read

		if(k=='csv'):
			path2='{}/alldata.csv'.format(path)
			sor.to_csv(r'{}'.format(path2)) # r-- read
	if(len(formatlist!=0)):
		messagebox.showinfo("Notififcation",'Corona Data is saved{}'.format(path2),parent=root)

import plyer
import requests
from bs4 import BeautifulSoup
from tkinter import*
from tkinter import messagebox,filedialog
import pandas as pd
root=Tk()
root.title("Corona Notify")
root.geometry('580x300+300+100')
root.configure(bg='light sky blue')
root.iconbitmap('kingbondl.ico')
formatlist=[]

def download():
	global path
	if(len(formatlist)!=0):
		path=filedialog.askdirectory()
		#print(path)
	else:
		pass
	scrap()
	formatlist.clear()
	inhtml.configure(state='normal')
	injson.configure(state='normal')
	incsv.configure(state='normal')

def inhtml():
	formatlist.append('html')
	inhtml.configure(state='disabled')
def injson():
	formatlist.append('json')
	injson.configure(state='disabled')
def incsv():
	formatlist.append('csv')
	incsv.configure(state='disabled')

#Labels
IntroLabel=Label(root,text='Virus Notification Application',font=('arial',15,'italic bold'),bg='yellow',width=50)
IntroLabel.place(x=0,y=0)

CountryEntryLabel=Label(root,text='Country Name : ',font=('arial',15,'italic bold'),bg='light sky blue',width=20)
CountryEntryLabel.place(x=5,y=70)

DataLabel=Label(root,text='Data Notify Type : ',font=('arial',15,'italic bold'),bg='light sky blue',width=20)
DataLabel.place(x=10,y=140)

#Entry Country Box Name
data_country=StringVar()
CountryEntryName=Entry(root,textvariable=data_country,font=('New-Roman',15,'italic bold'),relief=RIDGE,foreground='green',bd=2,width=25)
CountryEntryName.place(x=220,y=70)

#Buttons
htmlButton=Button(root,text='HTML',font=('arial',15,'italic bold'),bg='yellow',activebackground='purple4',relief=RIDGE,activeforeground='white',bd=4,width=8,command=inhtml)
htmlButton.place(x=220,y=140)

jsonButton=Button(root,text='JSON',font=('arial',15,'italic bold'),bg='yellow',activebackground='purple4',relief=RIDGE,activeforeground='white',bd=4,width=8,command=injson)
jsonButton.place(x=340,y=140)

csvButton=Button(root,text='CSV',font=('arial',15,'italic bold'),bg='yellow',activebackground='purple4',relief=RIDGE,activeforeground='white',bd=4,width=8,command=incsv)
csvButton.place(x=460,y=140)

SubmitButton=Button(root,text='Submit',font=('arial',15,'italic bold'),bg='yellow',activebackground='blue',relief=RIDGE,activeforeground='white',bd=4,width=8,command=download)
SubmitButton.place(x=110,y=220)

ExitButton=Button(root,text='Exit',font=('arial',15,'italic bold'),bg='yellow',activebackground='red',relief=RIDGE,activeforeground='white',bd=4,width=8)
ExitButton.place(x=260,y=220)

root.mainloop()