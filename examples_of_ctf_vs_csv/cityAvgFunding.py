import csv 
# a program that reads in a csv file with data on venture capital funding and computes
# the average amount of a funding each american city has then prints it
# this program is equivalent to the SQL query 
# SELECT sum(capital) FROM techcrucnch GROUP BY city


with open("TechCrunchcontinentalUSA.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    

    cities = {} #dictionary with key as city and two values as count and total amount of funding

    for row in reader:
        if(row["city"] in cities):
            cities[row["city"]][0] += 1
            cities[row["city"]][1] += int(row["raisedAmt"])
        else:
            cities[row["city"]] = [1, int(row["raisedAmt"])] 


    for key in cities:
        avgFund = cities[key][1] / cities[key][0]

        print(key + ": " + str(avgFund)) 


