#!/usr/bin/env python

#CreateE-book.py - Combines GenMetadata.py and GenEpub.py into one easy script.

#GenMetadata.py - Generates the content.opf and toc.ncx files from the metadata.json file.

#opf = "OEBPS/content.opf"
#ncx = "OEBPS/toc.ncx"

#JSON extraction magic

import os
import json
from collections import OrderedDict

with open("metadata.json") as json_file:
    data = json.load((json_file), object_pairs_hook=OrderedDict) #For some reason the order is randomised, this preserves the order.

#Create a compatible content.opf from scratch.
def GenOPF():

    opf = open(data["containerFolder"] + os.sep + "content.opf", "w")
    opf.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?><package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="2.0">\n')

    #Metadata tags
    opf.write('\t<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\n')
    opf.write('\t\t<dc:title>' + data["title"] + '</dc:title>\n')
    opf.write('\t\t<dc:creator>' + data["creator"] + '</dc:creator>\n')
    opf.write('\t\t<dc:subject>' + data["subject"] + '</dc:subject>\n')
    opf.write('\t\t<dc:publisher>' + data["publisher"] + '</dc:publisher>\n')
    opf.write('\t\t<dc:identifier id="bookid">' + data["ISBN"] + '</dc:identifier>\n')
    opf.write('\t\t<dc:language>' + data["language"] + '</dc:language>\n')
    opf.write('\t\t<dc:rights>' + data["rights"] + '</dc:rights>\n')
    opf.write('\t\t<meta content="main_cover_image" name="cover"/>\n')

    #Fixed (non-reflowable) support
    if data["textPresentation"] == "Reflowable" or "reflowable":
        print('e-book type: Reflowable')
        
    elif data["textPresentation"] == "Fixed layout" or "Fixed Layout" or "fixed layout" or "fixed":
        opf.write('\t\t<meta name="fixed-layout" content="true"/>\n')
        print('e-book type: Fixed layout')
    
    opf.write('\t</metadata>\n')

    #Manifest tags
    opf.write('\t<manifest>\n')

    #Write out the CSS files
    cssindex = 0

    for subdir, dirs, files in os.walk(data["containerFolder"] + os.sep + data["cssFolder"]):
        for file in files:
            filepath = subdir + os.sep + file
            correctfilepath = filepath.replace(data["containerFolder"] + os.sep, "") #removes the redudant OEBPS

            if filepath.endswith(".css"):
                opf.write('\t\t<item href="' + correctfilepath + '" id="css' + str(cssindex) + '" media-type="text/css"/>\n')
                print (filepath)
                cssindex += 1           

    #Write out the NCX and cover image files
    opf.write('\t\t<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\n')
    #opf.write('\t\t<item href="'+ data["imagesFolder"] + '/' + data["epubCover"] +'" id="main_cover_image" media-type="image/jpeg"/>\n') #Removes duplicate output, leaving commented as I might it later for the Kindle covers.

    #Write out the images

    imageindex = 0

    for subdir, dirs, files in os.walk(data["containerFolder"] + os.sep + data["imagesFolder"]):
        for file in files:
            filepath = subdir + os.sep + file
            correctfilepath = filepath.replace(data["containerFolder"] + os.sep, "") #removes the redudant OEBPS

            if filepath.endswith(".jpg") or filepath.endswith(".jpeg") or filepath.endswith(".jpe"):
                opf.write('\t\t<item href="' + correctfilepath + '" id="image' + str(imageindex) + '" media-type="image/jpeg"/>\n')
                print (filepath)
                imageindex += 1

            elif filepath.endswith(".png"):
                opf.write('\t\t<item href="' + correctfilepath + '" id="image' + str(imageindex) + '" media-type="image/png"/>\n')
                print (filepath)
                imageindex += 1

            elif filepath.endswith(".gif"):
                opf.write('\t\t<item href="' + correctfilepath + '" id="image' + str(imageindex) + '" media-type="image/gif"/>\n')
                print (filepath)
                imageindex += 1

            elif filepath.endswith(".svg"):
                opf.write('\t\t<item href="' + correctfilepath + '" id="image' + str(imageindex) + '" media-type="image/svg+xml"/>\n')
                print (filepath)
                imageindex += 1

    #Write out all the pages in the book.
    #Count all the instances within the pages block.

    currentpage = 0
    totalpages = len(data["pages"]) #Number of pages
    
    while currentpage != totalpages: #Write out all the xhtml files as declared in the JSON.
        pageid = str.lower(data["pages"][currentpage]["pageName"]) #remove capital letters and spaces from the id attribute (works with Unicode)
        correctpageid = pageid.replace(" ","_")
        
        opf.write('\t\t<item href="' + data["pages"][currentpage]["fileName"] + '" id="' + correctpageid + '" media-type="application/xhtml+xml"/>\n')
        currentpage += 1
        
    #Write out all the custom fonts in the book.

    fontindex = 0

    for subdir, dirs, files in os.walk(data["containerFolder"] + os.sep + data["fontsFolder"]):
        for file in files:
            filepath = subdir + os.sep + file
            correctfilepath = filepath.replace(data["containerFolder"] + os.sep, "") #removes the redudant OEBPS

            if filepath.endswith(".ttf"):
                opf.write('\t\t<item href="' + correctfilepath + '" id="font' + str(fontindex) + '" media-type="font/truetype"/>\n')
                print (filepath)
                imageindex += 1

            elif filepath.endswith(".otf"):
                opf.write('\t\t<item href="' + correctfilepath + '" id="font' + str(fontindex) + '" media-type="font/opentype"/>\n')
                print (filepath)
                imageindex += 1

    opf.write('\t</manifest>\n')

    #Spine tags
    opf.write('\t<spine toc="ncx">\n')

    #Write out all the filenames in order again as declared in the JSON.

    currentpage = 0
    totalpages = len(data["pages"]) #Number of pages
    
    while currentpage != totalpages: #Write out all the xhtml files as declared in the JSON.
        pageid = str.lower(data["pages"][currentpage]["pageName"]) #remove capital letters and spaces from the id attribute (works with Unicode)
        correctpageid = pageid.replace(" ","_")
        
        opf.write('\t\t<itemref idref="' + correctpageid + '"/>\n')
        currentpage += 1

    opf.write('\t</spine>\n')

    #End of file
    opf.write('</package>')

    opf.close() #Eventually save directly to the OEBPS folder

#Create a compatible toc.ncx from scratch.
def GenNCX():
   
    ncx = open(data["containerFolder"] + os.sep + "toc.ncx", "w")
    
    ncx.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    ncx.write('<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd"><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n')

    #Head tags
    ncx.write('<head>\n')
    ncx.write('\t<meta name="dtb:uid" content="' + data["ISBN"] + '" />\n') #Has to be the same as dc:identifier.

    #Declare the maximum amount of indentation from 1 to 4.
    
    indentations = [] #Assemble a Python list (array) with all the indentations and take the largest number.
    currentpage = 0
    totalpages = len(data["pages"]) #Number of pages
    
    while currentpage != totalpages: 
        indentations.append(data["pages"][currentpage]["indentation"])
        maxdepth = max(indentations)
        currentpage += 1
    
    ncx.write('\t<meta name="dtb:depth" content="' + str(maxdepth) + '" />\n')
    ncx.write('\t<meta name="dtb:totalPageCount" content="0" />\n')
    ncx.write('\t<meta name="dtb:maxPageNumber" content="0" />\n')
    ncx.write('</head>\n')

    #Doctitle tags
    ncx.write('<docTitle>\n')
    ncx.write('\t<text>' + data["titleShort"] + '</text>\n')
    ncx.write('</docTitle>\n')

    #Write out the NavMap tags (and their children)
    ncx.write('<navMap>\n')

    currentpage = 0
    index = 1
    totalpages = len(data["pages"]) #Number of pages

    while currentpage != totalpages: #Write out all the xhtml files as declared in the JSON, indendation currently unsupported (data["pages"][currentpage]["indentation"]. 
    
        ncx.write('\t<navPoint id="navpoint-' + str(currentpage) + '" playOrder="' + str(index) + '">\n') #id=001 class=h1 playOrder=1
        ncx.write('\t\t<navLabel>\n')
        ncx.write('\t\t\t<text>' + data["pages"][currentpage]["pageName"] + '</text>\n')
        ncx.write('\t\t</navLabel>\n')
        ncx.write('\t\t<content src="'+ data["pages"][currentpage]["fileName"] +'" />\n')
        ncx.write('\t</navPoint>\n')

        currentpage += 1
        index += 1
    
    ncx.write('</navMap>\n')
    
    #End of file
    ncx.write('</ncx>')

def GenEpub():
#GenEpub.py - Generates an .epub file from the data provided.
#Ideally with no errors or warnings from epubcheck (needs to be implemented, maybe with the Python wrapper).

    import os
    import json
    import zipfile
    
    with open('metadata.json') as json_file:
        data = json.load(json_file)

    #The ePub standard requires deflated compression and a compression order.
    zf = zipfile.ZipFile(data["fileName"] + '.epub', mode='w', compression=zipfile.ZIP_STORED)

    zf.write('mimetype')

    for dirname, subdirs, files in os.walk('META-INF'):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
            print('dirname:' + dirname)
            print('filename:' + filename)

    for dirname, subdirs, files in os.walk('OEBPS'):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
            print('dirname:' + dirname)
            print('filename:' + filename)

    zf.close()

    #zipfile has a built-in validator for debugging
    with open(data["fileName"] + '.epub', 'r') as f:
        if zipfile.is_zipfile(f) is True:
            print("ZIP file is valid.")

#Extra debugging information
#print(getinfo.compress_type(zf))
#print(getinfo.compress_size(zf))
#print(getinfo.file_size(zf))

GenOPF()
GenNCX()
GenEpub()
