#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Razor version 1.0

Copyright (C)2008 Petr Nohejl, jestrab.net

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

This program comes with ABSOLUTELY NO WARRANTY!

This program require graphic library PIL (http://www.pythonware.com/products/pil/).
Tested od PIL 1.1.6.
"""

### IMPORT A KONSTANTY #########################################################

import Image	# graficka knihovna PIL http://www.pythonware.com/products/pil/

import types	# datove typy
import string	# prace s retezci
import sys		# argv
import glob		# ziskani nazvu souboru dle * konvence
import os		# prace se soubory a adresari



CONST_EXTENSION = (".jpg", ".jpeg", ".png", ".gif", ".bmp")	# seznam koncovek souboru
CONST_SIGN = "_razor_images"								# nazev vystupniho adresare
CONST_ALIGN = 4												# zarovnani cisel ve stats
CONST_OFFSET = 5											# pocet mezer mezi udaji ve stats



### POMOCNE FCE ################################################################

# je prvek n-tice?
def IsTuple(obj):
	return type(obj)==types.TupleType
	
	
	
# vypocet sedi
def Greyscale(col):
	if(IsTuple(col)):
		res = (col[0] + col[1] + col[2]) / 3
	else:
		res = col
	return res



### LIMITS #####################################################################

# vraci meze obrazku pro orezani
def Limits(image, cropGrey, tolerance):

	# zjisteni velikosti
	xsize, ysize = image.size
	
	# inicializace mezi
	crop = [xsize, None, 0, ysize]
	
	# pruchod framebufferem
	for y in range(ysize):
		for x in range(xsize):
			color = image.getpixel((x, y))
			grey = Greyscale(color)

			if (not(grey > cropGrey-tolerance and grey < cropGrey+tolerance)): # kontrola stupne sedi s toleranci
				# leva mez
				if(x < crop[0]):
					crop[0] = x
					
				# prava mez
				if(x > crop[2]):
					crop[2] = x
					
				# horni mez
				if(crop[1] == None):
					crop[1] = y
				
				# dolni mez
				crop[3] = y+1
	
	crop[2] = crop[2] + 1
	
	# osetreni mezi pokud nemaji okraje	
	if(crop[0] == xsize):
		crop[0] = 0
	if(crop[1] == None):
		crop[1] = 0
	if(crop[2] == 0):
		crop[2] = xsize
		
	# osetreni preteceni framebufferu
	if(crop[0] < 0):
		crop[0] = 0
	if(crop[1] < 0):
		crop[1] = 0
	if(crop[2] > xsize):
		crop[2] = xsize
	if(crop[3] > ysize):
		crop[3] = ysize
			
	return crop



### GETFILES ###################################################################

# nacte seznam obrazku
def GetFiles(files, actDir):
	
	os.chdir(actDir)			# nastaveni aktualniho adresare
	dirs = []					# seznam adresaru
	elements = glob.glob("*")	# seznam souboru a adresaru
	
	# ziskani adresaru
	for x in range(len(elements)):
		if(os.path.isdir(elements[x])):
			dirs.append(elements[x])

	# ziskani a ulozeni souboru
	for x in range(len(CONST_EXTENSION)):
		type = glob.glob("*" + CONST_EXTENSION[x])
		# pridani absolutni cesty
		for x in range(len(type)):
			type[x] = os.path.join(actDir, type[x])
		files += type
		 
	# vnoreni do dalsiho podadresare
	if(dirs != []):
		for x in range(len(dirs)):
			GetFiles(files, os.path.join(actDir, dirs[x]))
	
	return files
	
	
	
### MAKEDIRS ###################################################################

# vytvori adresarovou strukturu
def MakeDirs(actDir, input, output):
	
	os.chdir(actDir)								# nastaveni aktualniho adresare
	dirs = []										# seznam adresaru do kterych se dale budu vnorovat
	elements = glob.glob("*")						# seznam souboru a adresaru
	outDir = string.replace(actDir, input, output)	# kopie aktualniho adresare
	
	# vytvoreni adresaru
	for x in range(len(elements)):
		if(os.path.isdir(elements[x])):
			new = os.path.join(outDir, elements[x])
			act = os.path.join(actDir, elements[x])
			if(os.path.isdir(new) == False):
				os.mkdir(new)
			dirs.append(act)
	
	# vnoreni do dalsiho podadresare
	if(dirs != []):
		for x in range(len(dirs)):
			MakeDirs(dirs[x], input, output)



### PRINT STATS ################################################################

def PrintStats(file, sizeImg, sizeReg):
	
	# potrebny pocet mezer
	spaceImg = []
	spaceReg = []
	spaceImg.append(CONST_ALIGN - len(str(sizeImg[0])))
	spaceImg.append(CONST_ALIGN - len(str(sizeImg[1])))
	spaceReg.append(CONST_ALIGN - len(str(sizeReg[0])))
	spaceReg.append(CONST_ALIGN - len(str(sizeReg[1])))
	
	# rozmery obrazku
	strImg = spaceImg[0] * " " + str(sizeImg[0]) + " x " + spaceImg[1] * " " + str(sizeImg[1])
	strReg = spaceReg[0] * " " + str(sizeReg[0]) + " x " + spaceReg[1] * " " + str(sizeReg[1])
	
	# vypis statistik
	print strImg + CONST_OFFSET * " " + strReg + CONST_OFFSET * " " + file



### ERROR A HELP ###############################################################

def ErrorArg():
	print "ERROR: Incorrect arguments!\nTo show help, run program with parameter -h."
	return
	
def ErrorDir(dir):
	print "ERROR: Directory " + dir + " doesn't exist!"
	return
	
def ErrorOpen(file):
	print "ERROR: Cannot open image file: " + file
	return
	
def ErrorSave(file):
	print "ERROR: Cannot save image file: " + file
	return
	
def Help():
	print "Razor version 1.0"
	print ""
	print "Copyright (C)2008 Petr Nohejl, jestrab.net"
	print ""
	print "Program cut off the excrescent margins in images and create new directory with new images."
	print "You must set absolute path where, you have your images,"
	print "color in greyscale (0-255, 255 is white color) and tolerance (0-255, 0 is no tolerance)."
	print ""
	print "Usage: razor path color tolerance"
	print "       razor -h"
	print ""
	print "Example: python razor.py D:\images 255 10"
	return



### RAZOR ######################################################################

# oreze prebytecne okraje obrazku
def Razor():

	# osetreni parametru prikazove radky
	if(len(sys.argv) == 4):
		input = sys.argv[1]
		try:
			cropGrey = int(sys.argv[2])
			tolerance = int(sys.argv[3])
		except:
			ErrorArg()
			return
		
		# overeni existence adresare
		if(os.path.isdir(input) == False):
			ErrorDir(input)
			return
		
		# overeni spravnost cisel
		if((cropGrey < 0 or cropGrey > 255) or (tolerance < 0 or tolerance > 255)):
			ErrorArg()
			return
			
	elif(len(sys.argv) == 2 and sys.argv[1] == "-h"):
		Help()
		return
	else:
		ErrorArg()
		return


	# vytvoreni vystupniho adresare a jeho podadresaru
	output = input + CONST_SIGN
	if(os.path.isdir(output) == False):
		os.mkdir(output)
	MakeDirs(input, input, output)

	# seznam souboru
	files = GetFiles([], input)
	
	
	# orezani obrazku
	for i in range(len(files)):
		
		# nacteni obrazku
		try:
			image = Image.open(files[i])
		except:
			ErrorOpen(files[i])
			continue
		
		# prevod do modu RGB
		imageRgb = image.convert("RGB")
		
		# zjisteni mezi
		crop = Limits(imageRgb, cropGrey, tolerance)
		
		# vystupni soubor
		save = string.replace(files[i], input, output)
		
		# orezani a ulozeni obrazku
		region = image.crop((crop[0], crop[1], crop[2], crop[3]))
		region.load()
		try:
			region.save(save)
		except:
			ErrorSave(files[i])
			continue
		
		# report
		PrintStats(files[i], image.size, region.size)



### MAIN #######################################################################

if (__name__=="__main__"):
	Razor()
