import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
#from flask import Flask, jsonify
#from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)


'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/screen_scrape_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    calNum = db.Column(db.String(100))
    protNum = db.Column(db.String(100))
    def __init__(self, title, calNum, protNum):
        self.title = title
        self.calNum = calNum
        self.protNum = protNum '''

backEndData2 = []


def getTitle(link):
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")
    titleOfFood = soup.find("div",class_="labelrecipe").text
    print(titleOfFood)
    backEndData2.append(titleOfFood)

def getCal(link):
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")

    calorie_count = soup.find("td",class_="nutfactscaloriesval")
    if calorie_count == None:
        print("N/A")
        backEndData2.append("N/A")
    else: 
        calorie_count = soup.find("td",class_="nutfactscaloriesval").text
        print("Calories " + calorie_count)
        backEndData2.append("Calories " + calorie_count)

def getProt(link):
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")
    
    prot_count = soup.find_all("span",class_="nutfactstopnutrient")
    for i in prot_count:
        item = {}
        item['Text'] = i.find(string=re.compile("Protein"))
        if item["Text"]!=None:
            if (len(item["Text"]) > 8):
                print(item["Text"])
                backEndData2.append(item["Text"])


#input is link from official UT page (JCL,J2,KINS,ETC.)
input = "https://hf-foodpro.austin.utexas.edu/foodpro/shortmenu.aspx?sName=University+Housing+and+Dining&locationNum=12&locationName=J2+Dining&naFlag=1"
page1 = requests.get(input)
soup1 = BeautifulSoup(page1.text,"html.parser")
all_items1 = soup1.find_all("td",valign="top",align="left")

breakfastLink = ""
lunchLink = ""
dinnerLink = ""
temp = ""
mealLinks = ["none","none","none"]
x = 0
for i in all_items1:
    temp = i.find("a").attrs["href"] #should return breakfast link and lunch link
    mealLinks[x] = temp
    x = x+1
breakfastLink = "https://hf-foodpro.austin.utexas.edu/foodpro/" + mealLinks[0]
lunchLink = "https://hf-foodpro.austin.utexas.edu/foodpro/" + mealLinks[1]
dinnerLink = "https://hf-foodpro.austin.utexas.edu/foodpro/" + mealLinks[2]

#####################################################

print("Breakfast:")
backEndData2.append("Breakfast: ")
url2 = breakfastLink
page2 = requests.get(url2)
soup2 = BeautifulSoup(page2.text,"html.parser")
all_items2 = soup2.find_all("div",class_="longmenucoldispname")
for nutLink in all_items2:
    item = {}
    item['Link'] = nutLink.find("a").attrs["href"]
    getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
    getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
    getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
    print()

"""

print()
print()
print("Lunch:")
backEndData2.append("Lunch: ")
url2 = lunchLink
page2 = requests.get(url2)
soup2 = BeautifulSoup(page2.text,"html.parser")
all_items2 = soup2.find_all("div",class_="longmenucoldispname")
for nutLink in all_items2:
    item = {}
    item['Link'] = nutLink.find("a").attrs["href"]
    getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
    getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
    getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
    print()

print()
print()
print("Dinner:")
backEndData2.append("Dinner: ")
url2 = dinnerLink
page2 = requests.get(url2)
soup2 = BeautifulSoup(page2.text,"html.parser")
all_items2 = soup2.find_all("div",class_="longmenucoldispname")
for nutLink in all_items2:
    item = {}
    item['Link'] = nutLink.find("a").attrs["href"]
    getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
    getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
    getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
    print() 
    
    
    """

'''
#Data API Route
@app.route("/backEndData")
def backEndData():
    return (backEndData2)

if __name__ == "__main__":
    app.run(debug=True) '''
