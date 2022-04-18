import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from datetime import datetime, timedelta

# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
    
    name: str
    date: datetime
    
    def __str__ (self):
        # String output
        # Holiday output when printed.
        return f"{self.name} ({self.date})"
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:

    def __init__(self):
       self.innerHolidays = []

    #print entire list as string
    def __str__ (self):
        outlist = []
        for hd in self.innerHolidays:
            outlist.append(str(hd))
        return str(outlist)
   
    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday

        if type(holidayObj) != Holiday:
            print("Not a valid holiday object")
            return
        # accept 2 date input formats, with or without hours, minutes sec
        try:
            newDate = datetime.strptime(str(holidayObj.date), '%Y-%m-%d %H:%M:%S')
        except:
            newDate = datetime.strptime(str(holidayObj.date), '%Y-%m-%d')

        self.innerHolidays.append(Holiday(holidayObj.name, newDate))
        print(f"{str(holidayObj)} added")

    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday

        for hd in self.innerHolidays:
            if hd.name == HolidayName and hd.date == Date:
                return hd

    def removeHoliday(self, HolidayName):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

        for hd in self.innerHolidays:
            #apparently example doens't check for date
            if hd.name == HolidayName: # and hd.date == Date:
                self.innerHolidays.remove(hd)
                print(f"{str(hd)} removed")
                return
        print(f"{HolidayName} not found")

    def read_json(self, filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

        with open(filelocation, "r") as f:
            data = json.load(f)
            for obj in data["holidays"]:
                self.addHoliday(Holiday(obj["name"], datetime.strptime(obj["date"], '%Y-%m-%d')))
                #self.addHoliday(Holiday(obj["name"], datetime.strptime(obj["date"], '%Y-%m-%d %H:%M:%S.%f')))

    def save_to_json(self, filelocation):
        # Write out json file to selected file.

        # convert list to formattable dict first and then json, dumps for convert to str, dump for write to file
        outHoli = []
        for holi in self.innerHolidays:
            outHoli.append({"name": holi.name, "date": str(holi.date)})
        outHoli2 = {"holidays": outHoli}
        #convert formatted dict to json
        niceHolidays = json.dumps(outHoli2)
        jsonHolidays = json.loads(niceHolidays)
        with open(filelocation, "w") as f:
            json.dump(jsonHolidays, f, indent = 4)

    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.    

        #easier than getting year from current datetime and add/subtract
        years = [2020,2021,2022,2023,2024] 
        # scrape site based on year, parse with bs4, then get table headers and anchor texts and convert to useable formats
        for year in years:
            try:
                hdsite = requests.get("https://www.timeanddate.com/holidays/us/"+str(year)).text
                soup = BeautifulSoup(hdsite,'html.parser')
                table = soup.find('table',attrs = {'id':'holidays-table'})
                tbody = table.find("tbody")
                # i as limit of things to not query too much from site
                #i = 0
                for row in tbody.find_all('tr'):
                    #datecell = row.find_all("th")
                    #print(datecell)
                    days = {}
                    if row.th != None and row.a != None:
                        dateVal = datetime.strptime(f"{row.th.string} {str(year)}", '%b %d %Y').date()
                        hd = Holiday(row.a.string, dateVal)
                        if hd not in self.innerHolidays:
                            self.addHoliday(hd)
                    '''i += 1
                    
                    if i > 50:
                        print("-----------------------------")
                        break'''
            except:
                print(f"Something went wrong scraping the holidays site for year: {year}")

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return (len(self.innerHolidays))
    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

        yearhd = list(filter(lambda hd: hd.date.year == year, self.innerHolidays))
        # have to convert datetime.date back into datetime.datetime to get isocalender
        weekhd = list(filter(lambda hd: datetime(hd.date.year, hd.date.month,hd.date.day).isocalendar().week == week_number, yearhd))
        return weekhd

    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

        # always used around filter, ie call is displayHolidaysInWeek(filter_holidays_by_week(self, year, week_number))
        # feel like this is a weird way of calling it but w/e
        for hd in holidayList:
            print(str(hd))

    def getWeather(self):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

        #only called from viewcurrentweek so got rid of weeknum
        #doesn't say where the weather is for so used san francisco since that was in the site example
        #no mention of using multiple apis in rubric, also used recommended api has data limitations and I couldn't find a better
        # one so this will only have weather for the next 5 days until the end of the week based on matching dates
        # also for some reason api may only be returning 3 days? can't really do anything about this

        #basically just copied from https://rapidapi.com/community/api/open-weather-map
        
        url = "https://community-open-weather-map.p.rapidapi.com/forecast"
        querystring = {"q":"san francisco,us"}
        headers = {
            "X-RapidAPI-Host": "community-open-weather-map.p.rapidapi.com",
            "X-RapidAPI-Key": "ec46b6accfmshcf7496c87fa6df6p105b29jsnb7c4987224f8"
        }
        response = ""
        try:    
            response = requests.request("GET", url, headers=headers, params=querystring)  
        except:
            print("Something went wrong getting the weather API")

        #print(response.json()["list"])

        #copied from https://www.pythonprogramming.in/how-to-get-start-and-end-of-week-data-from-a-given-date.html
        # timedelta is just modifying a datetime.date by a certain number of days, in the first case it's the number 
        # associated with the current day where monday is 0 and sunday is 6
        today = datetime.today().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday

        dayWeathers = {}
        for row in response.json()["list"]:
            dayNum = datetime.strptime(row["dt_txt"], '%Y-%m-%d %H:%M:%S').date().day
            if  dayNum >= start_of_week.day and dayNum <= end_of_week.day:
                #replaces keys for each day so ends up with weather being last day in entry
                #considered doing certain num of iterations to get noon but data not even number of entries per day
                for i in range(start_of_week.day, end_of_week.day+1):
                    if dayNum == i:
                        dayWeathers[i] = row["weather"][0]["description"].capitalize()

        return dayWeathers
                    
    def viewCurrentWeek(self, withWeather):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

        #displaying then asking defeats purpose of weather per day, new param for if include weather
        curWeek = datetime.today().isocalendar().week
        weekhd = self.filter_holidays_by_week(2022,curWeek)
        weekWeather = self.getWeather()

        if withWeather:
            for hd in weekhd:
                for key, value in weekWeather.items():
                    if hd.date.day == key:
                        print(f"{str(hd)} - {value}")
        else:
            self.displayHolidaysInWeek(self.filter_holidays_by_week(datetime.today().year, curWeek))

def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 
    runMenu = True
    unSavedChanges = False
    hl = HolidayList()
    hl.read_json("holidays.json")
    hl.scrapeHolidays()

    print(f"Holiday Management\n===================\nThere are {hl.numHolidays()} holidays stored in the system.")
    #not in requirements to have external txt files
    while runMenu:
        print("Holiday Menu\n================\n1. Add a Holiday\n2. Remove a Holiday\n3. Save Holiday List\n4. View Holidays\n5. Exit")
        menuItem = -1
        while menuItem <= 0 or menuItem > 5:
            try: 
                menuItem = int(input(""))
                if menuItem <= 0 or menuItem > 5:
                    print("Not a valid number")
            except: 
                print("Must be an integer")

        if menuItem == 1:
            name = str(input("Add a Holiday\n=============\nHoliday: "))
            date = ""
            needDate = True
            while needDate:
                try: 
                    date = datetime.strptime(input(F"Date (YYYY-MM-DD): "), '%Y-%m-%d')
                    needDate = False
                except: 
                    print("Incorrect format. Try again")
            hl.addHoliday(Holiday(name,date))
            unSavedChanges = True
        elif menuItem == 2:
            name = str(input("Remove a Holiday\n================\nHoliday Name: "))
            # func does print, if not found exit anyway so no softlock
            hl.removeHoliday(name)
        elif menuItem == 3:
            conf = str(input("Saving Holiday List\n====================\nEnter 'y' to save your changes, anything else otherwise:"))
            if conf.lower() == "y":
                hl.save_to_json("all_holidays.json")
                print("Your changes have been saved")
            else:
                print("Not saved")
            unSavedChanges = False
        #getting too annoying checking all valid input
        elif menuItem == 4:
            print("View Holidays\n=================")
            year = 0
            while year < 2020 or year > 2024:
                try: 
                    year = int(input(F"Select Year(2020-2024): "))
                    if year < 2020 or year > 2024:
                        print("Year out of range")
                except: 
                    print("Must be an integer")
            week = 0
            curWeek = False
            while week < 1 or week > 52:
                try: 
                    week = input(F"Select week #[1-52, Leave blank for the current week, overrides year]: ")
                    if week == "":
                        curWeek = True
                        break
                    week = int(week)
                    if week < 1 or week > 52:
                        print("Week out of range")
                except: 
                    print("Must be an integer")
            if not curWeek:
                hl.displayHolidaysInWeek(hl.filter_holidays_by_week(year, week))
            else:
                conf = str(input("Enter 'y' to see weather, anything else otherwise:"))
                if conf.lower() == "y":
                    hl.viewCurrentWeek(True)
                else: 
                    hl.viewCurrentWeek(False)
        elif menuItem == 5:
            #had a thing to track unsaved changes but this just makes more sense
            conf = str(input("Exit\n=====\nAre you sure you want to exit? (enter 'y' if so)\nAny unsaved changes will be lost.\n"))
            if conf.lower() == "y":
                runMenu = False
                print("Goodbye")

if __name__ == "__main__":
    main()


#other random testing comments below, moved down for conciseness




    #print(hl.filter_holidays_by_week(2021,2))
    
    #for i in str(hl):
       # print(type(i))
    #hl.scrapeHolidays()
    #hl.displayHolidaysInWeek(hl.filter_holidays_by_week(2022,1) )
    #hl.save_to_json("scrapedOUT.json")   
    #hl.getWeather() 
   # hl.viewCurrentWeek(False)
        



# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.





