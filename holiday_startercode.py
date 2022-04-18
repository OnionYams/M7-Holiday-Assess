import datetime
import json
from math import ceil
from tkinter.messagebox import NO
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from datetime import datetime

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
#@dataclass
class HolidayList:

    #innerHolidays: list

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
        self.innerHolidays.append(holidayObj)
        print(f"{str(holidayObj)} added")

    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday

        for hd in self.innerHolidays:
            if hd.name == HolidayName and hd.date == Date:
                return hd

    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

        for hd in self.innerHolidays:
            if hd.name == HolidayName and hd.date == Date:
                self.innerHolidays.remove(hd)
                print(f"{str(hd)} removed")
                break

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

        # convert list to formattable json first, dumps for convert to str, dump for write to file
        outHoli = []
        for holi in self.innerHolidays:
            outHoli.append({"name": holi.name, "date": str(holi.date)

                })
        outHoli2 = {"holidays": outHoli}
        #convert dict to json
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
        for year in years:
            try:
                hdsite = requests.get("https://www.timeanddate.com/holidays/us/"+str(year)).text
                soup = BeautifulSoup(hdsite,'html.parser')
                table = soup.find('table',attrs = {'id':'holidays-table'})
                tbody = table.find("tbody")
                i = 0
                for row in tbody.find_all('tr'):
                    #datecell = row.find_all("th")
                    #print(datecell)
                    days = {}
                    if row.th != None and row.a != None:
                        dateVal = datetime.strptime(f"{row.th.string} {str(year)}", '%b %d %Y').date()
                        hd = Holiday(row.a.string, dateVal)
                        if hd not in self.innerHolidays:
                            self.addHoliday(hd)
                    i += 1
                    
                    if i > 50:
                        print("-----------------------------")
                        break
            except:
                print("Something went wrong scraping the holidays site")



    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return (len(self.innerHolidays))
    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays
        '''
        for hd in self.innerHolidays:
            if hd.name == "New Year's Day":
                print(hd, datetime(hd.date.year, hd.date.month,hd.date.day).isocalendar().week)

        for hd in self.innerHolidays:
            print(datetime(hd.date.year, hd.date.month,hd.date.day).isocalendar().week)
            break
        return'''

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

    def getWeather(self, weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.
        a=1

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        a = 1


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
    print("bal")
    hl = HolidayList()
    hl.scrapeHolidays()
    hl.displayHolidaysInWeek(hl.filter_holidays_by_week(2022,1) )
    #hl.save_to_json("scrapedOUT.json")    
    print("end")
        
if __name__ == "__main__":
    main()


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





