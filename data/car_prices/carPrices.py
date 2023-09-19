#/usr/bin/python3
import csv
import pprint

# ********
# MetaData
# 
#  Data scraped from https://www.ccarprice.com/us/ on Sep 12th.
#  Collected from each brand name's page (on the right side) eg https://www.ccarprice.com/us/honda-car-prices-in-USA-1
#  Scraping was done manually by copying and pasting - this is the reason for the duplicate lines of car names on each line, the picture title. 
#  This data showed all models announced in 2023, not just 2023 model years, so anything not marked as 2023 was filtered out
#  The US in the title appears to only be the currency, so there are most definitely makes and models of vehicle not available in North America. 
#  
# ********

# ********
# Variables 
# ********
pp = pprint.PrettyPrinter(indent=4)


allRows = {} #all rows to clean up
cars = {} #cars to keep

namesList = ['Honda',
    'BMW',
    'Lexus',
    'Hyundai',
    'Toyota',
    'KIA',
    'Nissan',
    'Audi',
    'Chevrolet',
    'Ford',
    'Mercedes',
    'Porsche',
    'Infiniti',
    'Jaguar',
    'Cadillac',
    'Land Rover',
    'Jeep',
    'Volkswagen',
    'Maserati',
    'Subaru',
    'Dodge',
    'Mazda',
    'Chrysler',
    'Aston Martin',
    'Ferrari',
    'Lamborghini',
    'Bugatti',
    'Bentley',
    'Rolls Royce',
    'Mclaren',
    'Lincoln',
    'Alfa Romeo',
    'Volvo',
    'MINI',
    'Fiat',
    'Acura',
    'Genesis',
    'Buick',
    'GMC',
    'Tesla'
]


# ********
# Pull in Data 
# ********

def getCars():
    with open('cars.csv', mode='r', encoding='utf8') as cars:
    # with open('carstest.csv', mode='r', encoding='utf8') as cars:
        cars_reader = csv.DictReader(cars) 

        index=1000
        allRows[999] = ''
        for row in cars_reader:
            if(allRows[index-1] == row['car']):
                continue
            allRows[index] = row['car']
            index = index+1
        allRows.pop(999)

# ********
# Do stuff with Data 
# ********

# Find each car
def findAndCreateCars():

    carsIndex = 0

    # keeps track of current make to remove from name and add to cars dict
    currentMake = "" 

    for k, v in allRows.items():                

        # if row is ***, next row is first word of next row is make for next section
        if v == "***":
            currentMake = getCurrentMake(k)
            continue

        # skip if price (as I already got it last step)
        if('$' in v[0]):
            continue

        # skip if year is not 2023
        year = getYear(k)

        if(year != '2023'):
            continue

        # gets model and trim
        model = getModel(v, currentMake)

        # gets price (or 'No price available')
        price = getPrice(k)    

        # start new car
        cars[carsIndex] = {}
        cars[carsIndex]['year'] = year
        cars[carsIndex]['make'] = currentMake
        cars[carsIndex]['model'] = model
        # make nice string 
        # cars[carsIndex]['string'] = year + " " + currentMake + " " + model.strip()
        cars[carsIndex]['price'] = price
        carsIndex = carsIndex + 1

def getYear(k):
    return allRows[k][-4:]

def getPrice(k):
    priceRow = allRows[k+1]
    if(priceRow == "Coming soon"):
        return "No price available"
    return priceRow.replace("$","").replace(",","").strip()
    
def getModel(v, currentMake):

    # removes make from title ie  Tesla Model S Plaid 2022  -> Model S Plaid 2022    
    withoutMake = v.lstrip(currentMake).strip()

    # returns without make or year
    return withoutMake[:-5]

def getCurrentMake(k):
    entryList = allRows[k+1].split()
    # for the single word names
    if(entryList[0] in namesList):
        return entryList[0]
    
    # for the 2 word names
    if(entryList[0] + " " + entryList[1] in namesList):
        return entryList[0] + " " + entryList[1]

# ********
# makeCSV
# ********

def makeCSV():
    headerList = ['year', 'make','model','price']
    file = 'carPriceList.csv'
    try:
        with open(file, 'w', newline='') as f: 
            writer = csv.writer(f, delimiter=',')   
            writer.writerow(headerList)     
            
            for key, value in cars.items():

                writer.writerow(value.values())

            print("File " + file + " created successfully")

    except IOError:
        print("I/O error - Close the file Dumbass")  

# ********
# Run Methods
# ********    

getCars()
findAndCreateCars()

makeCSV()
