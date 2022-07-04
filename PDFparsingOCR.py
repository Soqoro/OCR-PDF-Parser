import enum
from lib2to3.pytree import convert
import pytesseract
from pdf2image import convert_from_path
import glob
import tkinter as tk

#GUI
window = tk.Tk()

#Search through all pdf files in one command
#pdfs = glob.glob(r"C:\Users\qiron\source\e2iprojects\*.pdf")

#If need to parse through every page of every pdf files
#for pdf_paths in pdfs:
#    pages = convert_from_path(pdf_paths,dpi = 500,userpw="Snp2020")
    
#    for pageNum,imgBlob in enumerate(pages):
#        text = pytesseract.image_to_string(imgBlob,lang="eng")

#        with open(f"{pdf_paths[:-4]}_page_{pageNum}.txt",'w') as the_file:
#            the_file.write(text)

ACRA = glob.glob(r"C:\Users\qiron\source\e2iprojects\ACRA.pdf")
APP = glob.glob(r"C:\Users\qiron\source\e2iprojects\APPLICATION.pdf")
FINAL = glob.glob(r"C:\Users\qiron\source\e2iprojects\FINAL.pdf")

#ACRA
#For first page of every pdf files
for pdf_paths in ACRA:
    pages = convert_from_path(pdf_paths,dpi = 500,userpw="Snp2020",single_file=True)
    for pageNum,imgBlob in enumerate(pages):
        text = pytesseract.image_to_string(imgBlob,lang="eng")

        with open(f"{pdf_paths[:-4]}_page_{pageNum}.txt",'w') as the_file:
            the_file.write(text)


#Filtering for UEN & SSIC
with open(r'C:\Users\qiron\source\e2iprojects\ACRA_page_0.txt', 'r') as f:
    count = 0
    for line in f.readlines():
        for str in line.split():
            if len(str) == 9 or len(str) == 10:
                if str[0].isdigit() and str[-1].isalpha():
                    UENtext = tk.Label(text="UEN: "+str)
                    UENtext.pack()
                    print("UEN: "+str)
            
            if len(str) == 7:
                if str[1:6].isdigit():
                    if count == 0:
                        count+=1
                        SSICtext = tk.Label(text="SSIC: "+str)
                        SSICtext.pack()
                        print("SSIC: "+str)

#FINAL
for pdf_paths in FINAL:
    pages = convert_from_path(pdf_paths,dpi = 500,first_page=3,last_page=3,userpw="Snp2020")
    for pageNum,imgBlob in enumerate(pages):
            text = pytesseract.image_to_string(imgBlob,lang="eng")

            with open(f"{pdf_paths[:-4]}_page_{pageNum+3}.txt",'w') as the_file:
                the_file.write(text)

#Filtering Through LOO
with open(r'C:\Users\qiron\source\e2iprojects\FINAL_page_3.txt', 'r') as f:
    linecount = 0
    count = 0
    startdate = ""
    enddate = ""
    claimdate = ""
    for line in f.readlines():
        linecount+=1
        if linecount == 6:
            reftext = tk.Label(text=line.rstrip())
            reftext.pack()
            print(line.rstrip())
            continue
        if linecount == 8:
            startdate = line
            continue
        if linecount == 10:
            Nametext = tk.Label(text="Name: "+line.rstrip())
            Nametext.pack()
            print("Name: "+line.rstrip())
            continue
        if linecount == 12:
            for str in line.split():
                Positiontext = tk.Label(text="Position: "+str)
                Positiontext.pack()
                print("Position: "+ str)
                break
        if linecount == 13 or linecount == 14:
            Addresstext = tk.Label(text="Address: "+line.rstrip())
            Addresstext.pack()
            print("Address: "+line.rstrip())
            continue
        if linecount == 33:
            for str in line.split():
                if str[0] == '$':
                    Granttext = tk.Label(text="Grant Amount: "+str)
                    Granttext.pack()
                    print("Grant Amount: "+str)
        if linecount == 35:
            tester = False
            count = 0
            for str in line.split():
                if str[0].isdigit():
                    tester = True
                    enddate += str
                    enddate += " "
                    if count == 1:
                        tester = False
                elif tester:
                    enddate += str
                    enddate += " "
                    count += 1
                    if count == 2:
                        tester = False
        if linecount == 38:
            tester = False
            count = 0
            for str in line.split():
                if str[0].isdigit():
                    tester = True
                    claimdate += str
                    claimdate += " "
                    if count == 1:
                        tester = False
                elif tester:
                    claimdate += str
                    claimdate += " "
                    count += 1
                    if count == 2:
                        tester = False
    startdatetext = tk.Label(text="Start Date: "+startdate.rstrip())
    enddatetext = tk.Label(text="End Date: "+enddate)
    Claimdatetext = tk.Label(text="Claim Date: "+claimdate)
    startdatetext.pack()
    enddatetext.pack()
    Claimdatetext.pack()
    print("Start Date: "+startdate.rstrip())
    print("End Date: "+enddate)
    print("Claim Date: "+claimdate)
    window.mainloop()



