from heapq import heappop, heappush, heapify
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Notebook
from yahoofinancials import YahooFinancials
import yfinance as yf
import matplotlib.pyplot as plt
import stockquotes
import pandas as pd

# Creating Base Root
root = Tk()

#Adjusting the size, naming, and creating icon
root.geometry('300x200')
root.title("Portfolio Tracker")
root.iconbitmap('c:/Users/jchur/Documents/College/Python App/pie-chart-32.ico')

# Creating different frames (input is for file, secondWindowFrame is for labels, thirdWindowFrame is for stock data, bottomWindowFrame is for buttons)
inputFrame = Frame(root)
secondWindowFrame = Frame(root)
thirdWindowFrame = Frame(root)
bottomWindowFrame = Frame(root)

# Colors for pie chart
colorList = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']


fileLocationFile = pd.read_csv('filelocation.csv')
v = StringVar()
fileLocation = ''

if fileLocationFile.iloc[0][1] != 'blank':
    v.set(fileLocationFile.iloc[0][1])
    fileLocation = fileLocationFile.iloc[0][1]

df = None
df_checker = False

def import_csv_data():
    # importing csv data to a df
    global v
    global df_checker
    global fileLocation
    csv_file_path = askopenfilename()
    tempFrame = pd.DataFrame({'File Location' : [csv_file_path]})
    tempFrame.to_csv('filelocation.csv')
    v.set(csv_file_path)
    fileLocation = csv_file_path

def submit_button():
    # submit button to transition to second window dataframe
    global fileLocation
    global df
    try:
        df = pd.read_csv(fileLocation)
        inputFrame.destroy()
        secondWindowCreator()
    except:
        window = Toplevel()
        label = Label(window,text="Must submit a file").pack()
        button_close = Button(window, text="Close",command = window.destroy).pack()

def sort(unsorted,names):
    # sort function that orders stock name and value from largeset position to smallest
    sortedNames = []
    maxList = []
    heapify(maxList)
    translateDict = {}
    retList = []

    for x in range(len(unsorted)):
        translateDict[unsorted[x]] = (x,names[x])
        heappush(maxList,-1*unsorted[x])

    while len(maxList) != 0:
        element = -1*heappop(maxList)
        retList.append(element)
        sortedNames.append(translateDict[element][1])

    return (retList,sortedNames)

def pieChartCreator(sizes,labels,colors):
    # using passed data to create pie chart in new window
    sizes,sortedNames = sort(sizes,labels)

    plt.pie(sizes,labels=sortedNames,colors=colors,autopct='%1.f%%',pctdistance=.9)
    plt.axis('equal')
    plt.show()

def plotChartMaker(ticker):
    # not working yet but shows the max length stock chart for ticker
    tickerHolder = yf.Ticker(ticker)
    tickerHolderdf = tickerHolder.history(period='max')
    tickerHolderdf['Close'].plot(title=str(ticker) + " stock price")
    plt.show()

def colorChooser(varName):
    if varName>= 0:
        return '#00FF7F'
    else:
        return '#F08080'

def secondWindowCreator():

    geometryString = len(df.index)*54 + 162
    geometryString = str(geometryString) + 'x500'
    root.geometry(geometryString)

    labels = []
    colors = []
    sizes = []
    total = 0
    newTotal = 0
    pastCloseTotal = 0

    Label(thirdWindowFrame,text='Ticker').grid(row=0,column=0,sticky="nsew",padx=1,pady=1)
    Label(thirdWindowFrame,text='#').grid(row=0,column=1,sticky="nsew",padx=1,pady=1)
    Label(thirdWindowFrame,text='Name').grid(row=0,column=2,sticky="nsew",padx=1,pady=1)
    Label(thirdWindowFrame,text='Sector').grid(row=0,column=3,sticky="nsew",padx=1,pady=1)
    Label(thirdWindowFrame,text='Average Entry').grid(row=0,column=4,sticky="nsew",padx=1,pady=1)
    Label(thirdWindowFrame,text='Total Cost').grid(row=0,column=5,sticky="nsew",padx=1,pady=1)
    Label(thirdWindowFrame,text='Current Value').grid(row=0,column=6,sticky="nsew",padx=1,pady=1)
    Label(thirdWindowFrame,text='% Growth').grid(row=0,column=7,sticky="nsew",padx=1,pady=1)
    Label(thirdWindowFrame,text='Day Change').grid(row=0,column=8,sticky="nsew",padx=1,pady=1)

    thirdWindowFrame.grid_columnconfigure(0,weight=1)
    thirdWindowFrame.grid_columnconfigure(1,weight=1)
    thirdWindowFrame.grid_columnconfigure(2,weight=1)
    thirdWindowFrame.grid_columnconfigure(3,weight=1)
    thirdWindowFrame.grid_columnconfigure(4,weight=1)
    thirdWindowFrame.grid_columnconfigure(5,weight=1)
    thirdWindowFrame.grid_columnconfigure(6,weight=1)
    thirdWindowFrame.grid_columnconfigure(7,weight=1)
    thirdWindowFrame.grid_columnconfigure(8,weight=1)

    for x in df.index:

        currentTicker = df.iloc[x][0]
        currentInfo = yf.Ticker(currentTicker).info
        currentCost = stockquotes.Stock(currentTicker).current_price *df.iloc[x][1]
        labels.append(currentInfo['shortName'])
        colors.append(colorList[x])
        sizes.append(currentCost)

        previousCloseValue = currentInfo['previousClose'] * df.iloc[x][1]
        dayGrowth = (currentCost - previousCloseValue)/ previousCloseValue * 100
        dayGrowth = round(dayGrowth,2)

        dayGrowthColor = colorChooser(dayGrowth)

        entranceCost = df.iloc[x][2]*df.iloc[x][1]
        percentageGrowth = (currentCost - entranceCost) / entranceCost * 100
        percentageGrowth = round(percentageGrowth,2)

        total += entranceCost
        newTotal += currentCost
        pastCloseTotal += previousCloseValue

        currentCost = '$' + str(round(currentCost,2))
        entranceCost = '$' + str(entranceCost)
        percentageGrowth = str(percentageGrowth) + '%'
        averageEntry = '$'+ str(df.iloc[x][2])
        dayGrowth = str(dayGrowth) + '%'

        Button(thirdWindowFrame,text=currentTicker,bd=0,command=lambda: plotChartMaker(currentTicker)).grid(row=x+1,column=0,sticky="nsew",padx=1,pady=1)
        Label(thirdWindowFrame,text=df.iloc[x][1]).grid(row=x+1,column=1,sticky="nsew",padx=1,pady=1)
        Label(thirdWindowFrame,text=currentInfo['shortName']).grid(row=x+1,column=2,sticky="nsew",padx=1,pady=1)
        try:
            value = currentInfo['sector']
        except:
            value = "Index Fund"
        Label(thirdWindowFrame,text=value).grid(row=x+1,column=3,sticky="nsew",padx=1,pady=1)
        Label(thirdWindowFrame,text=averageEntry).grid(row=x+1,column=4,sticky="nsew",padx=1,pady=1)
        Label(thirdWindowFrame,text=entranceCost).grid(row=x+1,column=5,sticky="nsew",padx=1,pady=1)
        Label(thirdWindowFrame,text=currentCost).grid(row=x+1,column=6,sticky="nsew",padx=1,pady=1)
        Label(thirdWindowFrame,text=percentageGrowth).grid(row=x+1,column=7,sticky="nsew",padx=1,pady=1)
        Label(thirdWindowFrame,text=dayGrowth,bg=dayGrowthColor).grid(row=x+1,column=8,sticky="nsew",padx=2,pady=1)

        thirdWindowFrame.grid_columnconfigure(0,weight=1)
        thirdWindowFrame.grid_columnconfigure(1,weight=1)
        thirdWindowFrame.grid_columnconfigure(2,weight=1)
        thirdWindowFrame.grid_columnconfigure(3,weight=1)
        thirdWindowFrame.grid_columnconfigure(4,weight=1)
        thirdWindowFrame.grid_columnconfigure(5,weight=1)
        thirdWindowFrame.grid_columnconfigure(6,weight=1)
        thirdWindowFrame.grid_columnconfigure(7,weight=1)
        thirdWindowFrame.grid_columnconfigure(8,weight=1)

    portfolioGrowth = (newTotal-total) / total * 100
    portfolioGrowth = str(round(portfolioGrowth,2)) + "%"
    portfolioDailyGrowth = (newTotal-pastCloseTotal)/pastCloseTotal *100

    dayPortfolioGrowthColor = colorChooser(portfolioDailyGrowth)

    portfolioDailyGrowth = str(round(portfolioDailyGrowth,2)) + '%'
    newTotal = '$' + str(round(newTotal,2))
    total = '$' + str(round(total,2))

    Label(secondWindowFrame,text='Portfolio Breakdown').grid(row=1,column=0)
    Label(secondWindowFrame,text='Portfolio Cost').grid(row=0,column=1)
    Label(secondWindowFrame,text='Portfolio Value').grid(row=0,column=2)
    Label(secondWindowFrame,text='Portfolio Growth').grid(row=0,column=3)
    Label(secondWindowFrame,text='Portfolio Daily Growth').grid(row=0,column=4)
    Label(secondWindowFrame,text=total).grid(row=1,column=1)
    Label(secondWindowFrame,text=newTotal).grid(row=1,column=2)
    Label(secondWindowFrame,text= portfolioGrowth).grid(row=1,column=3)
    Label(secondWindowFrame,text=portfolioDailyGrowth,bg=dayPortfolioGrowthColor).grid(row=1,column=4)

    Button(bottomWindowFrame,text='Refresh',command=secondWindowCreator).grid(row=0,column=0)
    Button(bottomWindowFrame,text='Portfolio Pie Chart',command=lambda: pieChartCreator(sizes,labels,colors)).grid(row=0,column=1)
    Button(bottomWindowFrame,text='Close',command=root.destroy).grid(row=0,column=2)

    secondWindowFrame.pack()
    thirdWindowFrame.pack(fill="both")
    bottomWindowFrame.pack()

Label(inputFrame,text='File Path',padx=20,pady=20).grid(row=0,column=0)
entry = Entry(inputFrame, textvariable=v).grid(row=0, column=1,columnspan=2)
Button(inputFrame, text='Find Data Set',command=import_csv_data,padx=10,pady=15).grid(row=1, column=0)
Button(inputFrame, text='Submit', command = submit_button,padx=20,pady=15).grid(row=1,column=1)
Button(inputFrame, text='Close',command=root.destroy,padx=20,pady=15).grid(row=1, column=2)

root.geometry('350x150') #width x heights
inputFrame.pack()

root.mainloop()
