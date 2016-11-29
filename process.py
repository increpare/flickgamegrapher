#!/usr/bin/python

import json
from subprocess import call
from os import listdir
from os.path import isfile, join
import os

def inc(s):
	return str(int(s)+1)

images = []

def processFile(filename):
	path = "lib/"+filename
	print(path)
	with (open(path)) as data_file:
		data = json.load(data_file)

	canvascolors = []
	for page in range(0,16):		
		canvaspage_colors = list(set(data["canvasses"][page][1::2]))
		canvaspage_colors_int = []
		for x in canvaspage_colors:
			canvaspage_colors_int.append(int("0x"+x,16))
		canvaspage_colors_int.sort()
		canvascolors.append(canvaspage_colors_int)

	hyperlinks = []
	for page in range(0,16):
		canvaspage_hyperlinks = data["hyperlinks"][page]
		canvaspage_hyperlinks_int = []
		for x in canvaspage_hyperlinks:
			canvaspage_hyperlinks_int.append(int(x))
		hyperlinks.append(canvaspage_hyperlinks_int)

	lines = []
	for page in range (0,16):
		for page2 in range(0,16):
			if page2 in canvascolors[page]:
				target = hyperlinks[page][page2]-1

				if target >=0:
					arrow = str(page)+","+str(target)
					if arrow not in lines:	
						lines.append(arrow)

	reachablepages = ["0"]
	addedpage = True 
	while addedpage:
		addedpage = False
		for l in lines:
			pair = l.split(",")
			if pair[0] in reachablepages and pair[1] not in reachablepages:
				addedpage = True
				reachablepages.append(pair[1])

	print("canvascolors = " +str(canvascolors))
	print("hyperlinks = " +str(hyperlinks))
	print("lines = " +str(lines))
	print ("reachablepages = " +str(reachablepages))
	graphstr = 'digraph {\n\tsplines=true;\n\tnode [margin=0 fontcolor=black fontsize=32 shape="point" width=0.1 label="" ]\n\t1 [shape="circle"]\n'
	for l in lines:
		pair = l.split(",")
		if (pair[0] in reachablepages) and (pair[0] != pair[1]):
			graphstr = graphstr + "\t"+inc(pair[0])+" -> " + inc(pair[1])+"\n"

	graphstr = graphstr + "}"

	textfile = open("viz/"+filename+".viz","w")
	textfile.write(graphstr);
	textfile.close()
	
	os.system ("neato -Tsvg viz/"+filename+".viz"+ " > svg/" + filename+".svg")

if not os.path.exists("viz"):
    os.makedirs("viz")
if not os.path.exists("svg"):
    os.makedirs("svg")

#processFile ("2476f4a312479277b044.txt")

htmlfile="<html><head><style>img{max-width:100%;}div{text-align:center;border:1px solid black;width:600px;}</style></head><body><center><div>this page graphs the structures of various games made with <a href='http://www.flickgame.org'>flickgame</a> that've appeared on <a href='http://flickgamegallery.tumblr.com/'>flickgamegallery.tumblr.com</a>.</div><p>\n"

onlyfiles = [f for f in listdir("lib") if isfile(join("lib", f))]
for fn in onlyfiles:
	if fn[0]==".":
		continue

	print(fn)

	processFile(fn)
	fnraw = fn.split('.')[0]
	htmlfile = htmlfile + '<div><img src="svg/'+fn+'.svg"><p><a href="http://www.flickgame.org/play.html?p='+fnraw+'">'+fnraw+"</a></div><p>"

htmlfile = htmlfile+"<p><div><a href='https://github.com/increpare/flickgamegrapher'>source code</a></div></center></body></html>"

textfile = open("index.html","w")
textfile.write(htmlfile);
textfile.close()
