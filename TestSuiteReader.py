import os
import csv

#  This program browses through a test suite for a combination of keywords by making a subset of the cases that match with the the combination of keywords.
#  The program goes through all the '.csv' files in a given folder.

def wordReader(row, keywrd, new_reader):
    for key in row:
        print
        # The keyword search is done in these columns only.
        if key in ["Title", "PreRequisites","Test Steps", "Test Steps (Expected Result)","Test Steps (Step)"]:
            words = row[key].split()
            # Converts everything to lower case to make the search case insensitive.
            wordsLower=map(lambda x: x.lower(), words)

            if keywrd.lower() in wordsLower:
                new_reader.append(row)
                break
    return new_reader

# This function recursively looks for next keyword in the reduced dictionary after completing one search
def recursive_Subset(keywrd, csv_row_reader, new_Reader): # keywrd: List of keword to look for in the suite, csv_row_reader: The cursor element that point to the next row/line when called
    for row in csv_row_reader:
        if len(keywrd)==0:  # This condition is given so that the Last subset after all the keywords have been matched, is printed.
            print("\n Suite: {} \t Folder: {} \t ID: {} \t Title: {}".format(row["Suite"],row["Section"],row['\ufeff"ID"'],row["Title"]),end="\n")
            # This condition is gven so that the recursion of this function comes to an end only after printing the last element of the Final subset.
            if csv_row_reader.index(row) >= len(csv_row_reader)-1:
                return
        else:
            result = wordReader(row, keywrd[0], new_Reader) # if there are more keywords to search, This code is executed
    new_Reader = []
    if len(result)==0:  # The code under this block is executed if subset is empty, i.e. If none of the cases have a combination of these keywords.
        print("\nNo Test case found with this combination of keywords in {} suite".format(csv_row_reader[0]["Suite"]))
    else:  # The code under this block is executed if the subset is not empty and searches for the next keyword in the subset.
        recursive_Subset(keywrd[1:], result, new_Reader)

print(""""
***This program allows you to  search through an exported version of the testrail for keywords and returns the Test case details (Suite, Folder and Test case ID)
for you to identify the test case easily.

***Make sure to export all the latest Test Suites of all the Components necessary from the Testrail to the same local folder having this TestSuiteKeyWordSearch.py file.

Enter the Key words below. After typing a keyword hit enter to type the next key word.
Type Done and hit Enter to start the search once you are done giving the keyword
""")
keyword=[] # Keywords are collected and stored in an array. Every element of the array is a keyword.
while True:
    isKeyWord=input("Enter the keyword / Done: \n").strip()
    if isKeyWord.lower()=="done":
        break
    elif isKeyWord=="":
        print("Keyword Cannot be empty")
    else:
        keyword= keyword + isKeyWord.split()  # This is done so that if more than one word is given in one entry, each word is taken as a keyword.


dir_list = os.listdir()
for file in dir_list:   #This Loop iterates through every CSV file in the folder. Each CSV file in the folder is an exported suite.
    new_Subset = []
    if ".csv" in file:
        with open(file,"r") as FileRHandle:
            csv_reader = csv.DictReader(FileRHandle) # This method from the CSV module helps convert the CSV file to a Dictionary. So the values of a cell of row can be pulled by the calling the 'key'
            csv_row_reader=list(csv_reader)   # I convert the Dictionary to a List so that I can iterate through it with the cursor pointing at the next list element after every call.
            recursive_Subset(keyword, csv_row_reader, new_Subset)