#! /usr/bin/python

"""
Example:
python get_hist.py -isin DE0002635307 -y 2015 -b 8
-b 		Boersen ID: 8: Fondsgesellschaft; 6: XETRA; 131 Tradegate
"""

__author__ = "Jan Bolmer"
__copyright__ = "Copyright 2017"
__version__ = "1.0"
__maintainer__ = "Jan Bolmer"
__email__ = "jan@bolmer.de"
__status__ = "stable"

import math, time, sys, os, argparse
from bs4 import BeautifulSoup
from urllib import urlopen
import matplotlib.pyplot as plt
import matplotlib.pyplot as pyplot
import matplotlib.dates as mdates
from pylab import *
import urllib, datetime
import datetime
import pandas as pd

#https://www.pantone.com/color-of-the-year-2017
pt_analogous = ["#86af49", "#817397", "#b88bac",
"#d57f70","#dcb967","#ac9897","#ac898d","#f0e1ce",
"#86af49", "#817397","#b88bac", "#d57f70", "#dcb967"]

hk_keys = ["Datum","Erster","Hoch","Tief","Schlusskurs",
			"Stuecke","Volumen"]

today = datetime.datetime.today().strftime('%d.%m.%Y')

def get_data_from_isin(isin, start_year=2010, b_id=8):

	webs = "http://www.ariva.de"
	urlstr = "http://www.ariva.de/"+isin+"/historische_kurse"

	html = urlopen(urlstr).read()    
	soup = BeautifulSoup(html)
	secu = soup.find('input', {'name': 'secu'}).get('value')


	etf_name = soup.title.string.strip("- Historische Kurse - Aktien, Aktienkurse - ARIVA.DE")

	print "getting security code from", urlstr 

	dl_strg = "http://www.ariva.de/quote/historic/historic.csv?secu=" \
		+secu+"&boerse_id="+str(b_id) \
		+"&clean_split=1&clean_payout=1&clean_bezug=1&min_time=01.01."\
		+str(start_year)+"&max_time=" \
		+today+"&trenner=%3B&go=Download"
	
	file = urllib.URLopener()
	file.retrieve(dl_strg, isin+".csv")
	
	isin_df = pd.DataFrame.from_csv(isin+".csv",sep=";",index_col=None)
	
	datum = isin_df["Datum"]
	kurs, kurs_tief, kurs_hoch = [], [], []

	for i in isin_df["Schlusskurs"]:
		if i==" ":
			kurs.append(0.0)
		else:
			kurs.append(float(i.replace(',','.')))

	for i in isin_df["Tief"]:
		if i==" ":
			kurs_tief.append(0.0)
		else:
			kurs_tief.append(float(i.replace(',','.')))

	for i in isin_df["Hoch"]:
		if i==" ":
			kurs_hoch.append(0.0)
		else:
			kurs_hoch.append(float(i.replace(',','.')))

	return datum, kurs, kurs_tief, kurs_hoch, etf_name

def plot_kurs(isin, start_year, etf_name, datum, kurs, kurs_tief, kurs_hoch):

	fig = figure(figsize=(12, 6))
	ax = fig.add_axes([0.08, 0.12, 0.88, 0.80])

	ax.plot_date(datum, kurs, linestyle='solid',marker='o',markersize=2,
		linewidth=0.8, color=pt_analogous[3], label="Aktueller Kurs: "+str(kurs[0]))

	date_format = mdates.DateFormatter("%d/%m/%Y")
	ax.xaxis.set_major_formatter(date_format)
	ax.autoscale_view()
	ax.set_title(etf_name, fontsize=18)
	ax.set_ylabel("Kurs (Eur)",fontsize=18)

	if len(kurs) > 0:
		ax.set_ylim([min(kurs)-2, max(kurs)+2])
		#ax.text(min(datum), max(kurs), "Aktueller Kurs: "+str(kurs[0]))

	ax.grid(True)
	
	lg = ax.legend(numpoints=1, fontsize=16, loc=2)

	for axis in ['top','bottom','left','right']:
	  ax.spines[axis].set_linewidth(2)
	ax.tick_params(which='major',length=8,width=2)
	ax.tick_params(which='minor',length=4,width=1.5)

	for tick in ax.yaxis.get_major_ticks():
		tick.label.set_fontsize(12)

	fig.autofmt_xdate()
	fig.savefig(isin+"_"+str(start_year)+"-"+today+".pdf")
	plt.show()

if __name__ == "__main__":

	start = time.time()

	parser = argparse.ArgumentParser(usage=__doc__)
	parser.add_argument('-isin','--isin',dest="isin",default="LU0496786574",type=str)
	parser.add_argument('-y','--year', dest="year",default=2010,type=int)
	parser.add_argument('-b','--b_id', dest="b_id",default=8,type=int)

	args = parser.parse_args()

	b_id = args.b_id
	isin = args.isin
	start_year = args.year

	datum, kurs, kurs_tief, kurs_hoch, etf_name = get_data_from_isin(isin, start_year, b_id)
	plot_kurs(isin, start_year, etf_name, datum, kurs, kurs_tief, kurs_hoch)




