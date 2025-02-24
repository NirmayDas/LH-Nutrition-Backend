from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

backEndData2 = []

def invalidCheck(link):
    global invalidVariable
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")
    invalid = soup.find("div",class_="labelnotavailable")
    if(type(invalid) == type(None)):
        invalidVariable = False #if invalidVariable is false then proceed
        return
    else:
        invalidVariable = True #invalidVariable is true then skip adding to database

def getTitle(link):
    global tempTitle
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")
    titleOfFood = soup.find("div",class_="labelrecipe").text
    print(titleOfFood)
    backEndData2.append(titleOfFood)
    tempTitle = titleOfFood
    find_menu_for_item(result,tempTitle)


def getCal(link):
    global tempCal
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")

    calorie_count = soup.find("td",class_="nutfactscaloriesval")
    calorie_count = soup.find("td",class_="nutfactscaloriesval").text
    testvariable = calorie_count

    if '-' in testvariable:
        print("detected")
        backEndData2.append("Calories " + '0')
        tempCal = 0
        return
    else:
        #print("Calories: " + calorie_count)
        backEndData2.append("Calories " + calorie_count)
        tempCal = calorie_count

def getServingSize(link2):
    global tempServingSize
    tempServingSize = ''
    temp = requests.get(link2)
    soup = BeautifulSoup(temp.text,"html.parser")
    temp2 = (soup.find("div",class_="nutfactsservsize"))
    temp3 = temp2.findNext()
    realServingSize = temp3.text
    #print('Serving Size: ' + realServingSize)
    tempServingSize = realServingSize #later use to update serializer
    #nutfactsservsize

def getProt(link):
    global tempProt
    tempProt = 0
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")
    prot_count = soup.find_all("span",class_="nutfactstopnutrient")
    testvariable = prot_count[18].text
    if '-' in testvariable:
        print("detected 0")
        backEndData2.append("Fat " + '0g')
        tempProt = 0
        return
    tempString = prot_count[18].text.strip()
    tempString = re.findall('\d+\.\d+|\d+',tempString)
    tempString = [float(i) for i in tempString]
    tempProt = tempString[0]
    #print("Protein: " + str(tempString[0]) + 'g')

def getFat(link):
    global tempFat
    tempFat = 0
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")
    fat_count = soup.find_all("span",class_="nutfactstopnutrient")
    testvariable = fat_count[0].text
    if '-' in testvariable:
        print("detected 0")
        backEndData2.append("Fat " + '0g')
        tempFat = 0
        return
    tempString = fat_count[0].text.strip()
    tempString = re.findall('\d+\.\d+|\d+',tempString)
    tempString = [float(i) for i in tempString]
    tempFat = tempString[0]
    #print("Total Fat: " + str(tempString[0]) + 'g')

def getCholesterol(link):
    global tempChol
    tempChol = 0
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")
    chol_count = soup.find_all("span",class_="nutfactstopnutrient")
    testvariable = chol_count[12].text
    if '-' in testvariable:
        print("detected 0")
        backEndData2.append("Sugar " + '0g')
        tempChol = 0
        return
    tempString = chol_count[12].text.strip()
    tempString = re.findall('\d+\.\d+|\d+',tempString)
    tempString = [float(i) for i in tempString]
    tempChol = tempString[0]
    #print("Cholesterol: " + str(tempString[0]) + 'mg')

def getCarb(link):
    global tempCarb
    tempCarb = 0
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")
    carb_count = soup.find_all("span",class_="nutfactstopnutrient")
    testvariable = carb_count[2].text
    if '-' in testvariable:
        print("detected 0")
        backEndData2.append("Carbs: " + '0g')
        tempCarb = 0
        return
    tempString = carb_count[2].text.strip()
    tempString = re.findall('\d+\.\d+|\d+',tempString)
    tempString = [float(i) for i in tempString]
    tempCarb = tempString[0]
    #print("Total Carbs: " + str(tempString[0]) + 'g')

def getSodium(link):
    global tempSodium
    tempSodium = 0
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")
    sodium_count = soup.find_all("span",class_="nutfactstopnutrient")
    testvariable = sodium_count[16].text
    if '-' in testvariable:
        print("detected 0")
        backEndData2.append("Sodium " + '0g')
        tempSodium = 0
        return
    tempString = sodium_count[16].text.strip()
    tempString = re.findall('\d+\.\d+|\d+',tempString)
    tempString = [float(i) for i in tempString]
    tempSodium = tempString[0]
    #print("Sodium: " + str(tempString[0]) + 'mg')

def getSugar(link):
    global tempSugar
    tempSugar = 0
    temp = requests.get(link)
    soup = BeautifulSoup(temp.text,"html.parser")
    sugar_count = soup.find_all("span",class_="nutfactstopnutrient")
    testvariable = sugar_count[10].text
    if '-' in testvariable:
        print("detected 0")
        backEndData2.append("Sugar " + '0g')
        tempSugar = 0
        return
    tempString = sugar_count[10].text.strip()
    tempString = re.findall('\d+\.\d+|\d+',tempString)
    tempString = [float(i) for i in tempString]
    tempSugar = tempString[0]
    #print("Total Sugars: " + str(tempString[0]) + 'g')

def parse_menu(soup):
    global result
    result = []
    added_menus = set()  # To track added menus and avoid duplicates
    
    # Get all rows in the table
    rows = soup.find_all('tr')

    current_menu = None

    for row in rows:
        # Check for menu categories
        menu_cat = row.find(class_='longmenucolmenucat')
        if menu_cat:
            menu_text = menu_cat.get_text(strip=True)
            if menu_text not in added_menus:
                result.append(f"menu: {menu_text}")
                added_menus.add(menu_text)
            current_menu = menu_text
        
        # Check for items
        item_div = row.find(class_='longmenucoldispname')
        if item_div:
            if current_menu:
                item_text = item_div.get_text(strip=True)
                if not any(item.startswith(f"item: {item_text}") for item in result):
                    result.append(f"item: {item_text}")
    
    #print(result)
    return result

def find_menu_for_item(menu_array, item_title):
    global current_menu
    current_menu = None
    for entry in menu_array:
        if entry.startswith('menu:'):
            # Extract the menu name and remove '--' and 'menu:' parts
            menu_name = entry.replace('menu: ', '').replace('-- ', '').replace(' --', '')
            current_menu = menu_name
        elif entry.startswith('item:') and item_title in entry:
            # Return the current menu if the item title is found
            #print(current_menu)
            return current_menu
    # Return None if item is not found in the array
    return None

global tempCount 
tempCount = 0

def run_scraping_task():
    ##### FIRST ITERATION #############################################################################################
    ##### FIRST ITERATION #############################################################################################
    ##### FIRST ITERATION #############################################################################################
    ##### FIRST ITERATION #############################################################################################
    
    
    #THIS INPUT LINK SHOULD BE THE JCL INPUT LINK
    #input = 'https://hf-foodpro.austin.utexas.edu/foodpro/shortmenu.aspx?sName=University+Housing+and+Dining&locationNum=12(a)&locationName=JCL+Dining&naFlag=1&WeeksMenus=This+Week%27s+Menus&myaction=read&dtdate=8%2f24%2f2024'
    input = 'https://hf-foodpro.austin.utexas.edu/foodpro/shortmenu.aspx?sName=University+Housing+and+Dining&locationNum=12(a)&locationName=JCL+Dining&naFlag=1'
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
    
    print("JCL Dining Hall: ")
    Article.objects.all().delete()   #resets the table except for the ids
    '''
    print("Breakfast:")
    backEndData2.append("Breakfast: ")
    url2 = breakfastLink
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text,"html.parser")
    parse_menu(soup2) #test
    all_items2 = soup2.find_all("div",class_="longmenucoldispname")
    for nutLink in all_items2:
        item = {}
        item['Link'] = nutLink.find("a").attrs["href"]
        invalidCheck("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
        if(invalidVariable == False):
            getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getServingSize("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getFat("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCholesterol("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSodium("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCarb("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSugar("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            b = Article(title = tempTitle, calories = tempCal, protein = tempProt, count=tempCount, meal=1, servingSize=tempServingSize, diningHall=1, sodium=tempSodium,fat=tempFat,chol=tempChol,carbs=tempCarb,sugar=tempSugar,line=current_menu)
            b.save()
            serializer = ArticleSerializer(b)
            print()'''
    
    
    print('\n' + '\n' + "Lunch:")
    backEndData2.append("Lunch: ")
    url2 = breakfastLink #it is only like this since JCL has only 2 meals
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text,"html.parser")
    parse_menu(soup2) #test
    all_items2 = soup2.find_all("div",class_="longmenucoldispname")
    for nutLink in all_items2:
        item = {}
        item['Link'] = nutLink.find("a").attrs["href"]
        invalidCheck("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
        if(invalidVariable == False):
            getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getServingSize("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getFat("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCholesterol("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSodium("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCarb("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSugar("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            b = Article(title = tempTitle, calories = tempCal, protein = tempProt, count=tempCount, meal=2, servingSize=tempServingSize, diningHall=1, sodium=tempSodium,fat=tempFat,chol=tempChol,carbs=tempCarb,sugar=tempSugar,line=current_menu)
            b.save()
            serializer = ArticleSerializer(b)
            print()
    
    
    print('\n' + '\n' + "Dinner:")
    backEndData2.append("Dinner: ")
    url2 = lunchLink # it is only like this since JCL has 2 meals
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text,"html.parser")
    parse_menu(soup2) #test
    all_items2 = soup2.find_all("div",class_="longmenucoldispname")
    for nutLink in all_items2:
        item = {}
        item['Link'] = nutLink.find("a").attrs["href"]
        invalidCheck("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
        if(invalidVariable == False):
            getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getServingSize("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getFat("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCholesterol("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSodium("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCarb("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSugar("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            b = Article(title = tempTitle, calories = tempCal, protein = tempProt, count=tempCount, meal=3, servingSize=tempServingSize, diningHall=1, sodium=tempSodium,fat=tempFat,chol=tempChol,carbs=tempCarb,sugar=tempSugar,line=current_menu)
            b.save()
            serializer = ArticleSerializer(b)
            print()
    
    ##### SECOND ITERATION #############################################################################################
    ##### SECOND ITERATION #############################################################################################
    ##### SECOND ITERATION #############################################################################################
    ##### SECOND ITERATION #############################################################################################
    
    
    #THIS INPUT LINK SHOULD BE J2
    input = "https://hf-foodpro.austin.utexas.edu/foodpro/shortmenu.aspx?sName=University+Housing+and+Dining&locationNum=12&locationName=J2+Dining&naFlag=1"
    page1 = requests.get(input)
    soup1 = BeautifulSoup(page1.text,"html.parser")
    parse_menu(soup1) #test
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
    print("J2 Dining Hall: ")
    print("Breakfast:")
    backEndData2.append("Breakfast: ")
    url2 = breakfastLink
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text,"html.parser")
    parse_menu(soup2) #test
    all_items2 = soup2.find_all("div",class_="longmenucoldispname")
    for nutLink in all_items2:
        item = {}
        item['Link'] = nutLink.find("a").attrs["href"]
        invalidCheck("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
        if(invalidVariable == False):
            getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getServingSize("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getFat("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCholesterol("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSodium("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCarb("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSugar("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            b = Article(title = tempTitle, calories = tempCal, protein = tempProt, count=tempCount, meal=1, servingSize=tempServingSize, diningHall=2, sodium=tempSodium,fat=tempFat,chol=tempChol,carbs=tempCarb,sugar=tempSugar,line=current_menu)
            b.save()
            serializer = ArticleSerializer(b)
            print()
    
    print('\n' + '\n' + "Lunch:")
    backEndData2.append("Lunch: ")
    url2 = lunchLink
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text,"html.parser")
    parse_menu(soup2) #test
    all_items2 = soup2.find_all("div",class_="longmenucoldispname")
    for nutLink in all_items2:
        item = {}
        item['Link'] = nutLink.find("a").attrs["href"]
        invalidCheck("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
        if(invalidVariable == False):
            getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getServingSize("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getFat("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCholesterol("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSodium("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCarb("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSugar("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            b = Article(title = tempTitle, calories = tempCal, protein = tempProt, count=tempCount, meal=2, servingSize=tempServingSize, diningHall=2, sodium=tempSodium,fat=tempFat,chol=tempChol,carbs=tempCarb,sugar=tempSugar,line=current_menu)
            b.save()
            serializer = ArticleSerializer(b)
            print()
    
    print('\n' + '\n' + "Dinner:")
    backEndData2.append("Dinner: ")
    url2 = dinnerLink
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text,"html.parser")
    parse_menu(soup2) #test
    all_items2 = soup2.find_all("div",class_="longmenucoldispname")
    for nutLink in all_items2:
        item = {}
        item['Link'] = nutLink.find("a").attrs["href"]
        invalidCheck("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
        if(invalidVariable == False):
            getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getServingSize("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getFat("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCholesterol("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSodium("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCarb("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSugar("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            b = Article(title = tempTitle, calories = tempCal, protein = tempProt, count=tempCount, meal=3, servingSize=tempServingSize, diningHall=2, sodium=tempSodium,fat=tempFat,chol=tempChol,carbs=tempCarb,sugar=tempSugar,line=current_menu)
            b.save()
            serializer = ArticleSerializer(b)
            print()
    
    
    
    
    ##### THIRD ITERATION #############################################################################################
    ##### THIRD ITERATION #############################################################################################
    ##### THIRD ITERATION #############################################################################################
    ##### THIRD ITERATION #############################################################################################
    
    #THIS INPUT LINK SHOULD BE KINSOLVING
    
    input = 'https://hf-foodpro.austin.utexas.edu/foodpro/shortmenu.aspx?sName=University+Housing+and+Dining&locationNum=03&locationName=Kins+Dining&naFlag=1'
    #input = "https://hf-foodpro.austin.utexas.edu/foodpro/shortmenu.aspx?sName=University+Housing+and+Dining&locationNum=12&locationName=J2+Dining&naFlag=1"
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
    print("Kinsolving Dining Hall: ")
    print("Breakfast:")
    backEndData2.append("Breakfast: ")
    url2 = breakfastLink
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text,"html.parser")
    parse_menu(soup2) #test
    all_items2 = soup2.find_all("div",class_="longmenucoldispname")
    for nutLink in all_items2:
        item = {}
        item['Link'] = nutLink.find("a").attrs["href"]
        invalidCheck("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
        if(invalidVariable == False):
            getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getServingSize("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getFat("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCholesterol("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSodium("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCarb("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSugar("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            b = Article(title = tempTitle, calories = tempCal, protein = tempProt, count=tempCount, meal=1, servingSize=tempServingSize, diningHall=3, sodium=tempSodium,fat=tempFat,chol=tempChol,carbs=tempCarb,sugar=tempSugar,line=current_menu)
            b.save()
            serializer = ArticleSerializer(b)
            print()
    
    print('\n' + '\n' + "Lunch:")
    backEndData2.append("Lunch: ")
    url2 = lunchLink
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text,"html.parser")
    parse_menu(soup2) #test
    all_items2 = soup2.find_all("div",class_="longmenucoldispname")
    for nutLink in all_items2:
        item = {}
        item['Link'] = nutLink.find("a").attrs["href"]
        invalidCheck("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
        if(invalidVariable == False):
            getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getServingSize("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getFat("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCholesterol("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSodium("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCarb("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSugar("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            b = Article(title = tempTitle, calories = tempCal, protein = tempProt, count=tempCount, meal=2, servingSize=tempServingSize, diningHall=3, sodium=tempSodium,fat=tempFat,chol=tempChol,carbs=tempCarb,sugar=tempSugar,line=current_menu)
            b.save()
            serializer = ArticleSerializer(b)
            print()
    
    print('\n' + '\n' + "Dinner:")
    backEndData2.append("Dinner: ")
    url2 = dinnerLink
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text,"html.parser")
    parse_menu(soup2) #test
    all_items2 = soup2.find_all("div",class_="longmenucoldispname")
    for nutLink in all_items2:
        item = {}
        item['Link'] = nutLink.find("a").attrs["href"]
        invalidCheck("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
        if(invalidVariable == False):
            getTitle("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCal("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getProt("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getServingSize("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getFat("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCholesterol("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSodium("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getCarb("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            getSugar("https://hf-foodpro.austin.utexas.edu/foodpro/" + item['Link'])
            b = Article(title = tempTitle, calories = tempCal, protein = tempProt, count=tempCount, meal=3, servingSize=tempServingSize, diningHall=3, sodium=tempSodium,fat=tempFat,chol=tempChol,carbs=tempCarb,sugar=tempSugar,line=current_menu)
            b.save()
            serializer = ArticleSerializer(b)
            print()
#end of function
    
run_scraping_task()


#SPECIAL CHARACTES:
#&nbsp;-&nbsp;-&nbsp;-
#\xa0-\xa0-\xa0-

# Create your views here.
def printData(request):
    return HttpResponse(backEndData2)

def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    

@csrf_exempt
def article_details(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT': 
        data = JSONParser().parse(request)
        device_identifier = data.get('deviceIdentifier')
        tempCount2 = data.get('tempCount2')
        if device_identifier and tempCount2 is not None:
            if 'count' not in article.__dict__:
                article.count = {}
            article.count[device_identifier] = tempCount2
            article.save()
            serializer = ArticleSerializer(article)
            return JsonResponse(serializer.data, safe=False)
        else:
            serializer = ArticleSerializer(article, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, safe=False)
            return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        article.delete()
        return HttpResponse(status=204)
