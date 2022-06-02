import os
import csv
dir_list = os.listdir()


# This function converts the data to dictionaries with the column heads as keys and the list of all the data under the column as value.

def wordReader(line, keywrd,new_reader):
    for key in line:
        print
        if key in ["Title", "PreRequisites","Test Steps", "Test Steps (Expected Result)","Test Steps (Step)"]:
            words = line[key].split()
            wordsComp=map(lambda x: x.lower(), words)

            if keywrd.lower() in wordsComp:
                new_reader.append(line)
                break
    return new_reader

# This function recursively looks for next keyword in the reduced dictionary after completing one search
def kewRecurs(keywrd, csv_read, new_Reader):
    for line in csv_read:
        if len(keywrd)==0:
            print("\n Suite: {} \t Folder: {} \t ID: {} \t Title: {}".format(line["Suite"],line["Section"],line['\ufeff"ID"'],line["Title"]),end="\n")
            if csv_read.index(line) >= len(csv_read)-1:
                return
        else:
            result = wordReader(line, keywrd[0], new_Reader)
    new_Reader = []
    if len(result)==0:
        print("\nNo Test case found with this combination of keywords in {} suite".format(csv_read[0]["Suite"]))
    else:
        kewRecurs(keywrd[1:], result, new_Reader)

print(""""
***This program allows you to  search through an exported version of the testrail for keywords and returns the Test case details (Suite, Folder and Test case ID)
for you to identify the test case easily.

***Make sure to export all the latest Test Suites of all the Components necessary from the Testrail to the same local folder having this TestSuiteKeyWordSearch.py file.

Enter the Key words below. After typing a keyword hit enter to type the next key word.
Type Done and hit Enter to start the search once you are done giving the keyword
""")
keyword=[]
while True:
    isKeyWord=input("Enter the keyword / Done: \n").strip()
    if isKeyWord.lower()=="done":
        break
    elif isKeyWord=="":
        print("Keyword Cannot be empty")
    else:
        keyword= keyword + isKeyWord.split()



for file in dir_list:
    new_reader = []
    if ".csv" in file:
        with open(file,"r") as FileRHandle:
            csv_reader = csv.DictReader(FileRHandle)
            csv_read=list(csv_reader)
            kewRecurs(keyword,csv_read,new_reader)