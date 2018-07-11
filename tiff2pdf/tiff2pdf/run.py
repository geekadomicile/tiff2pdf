from os import listdir
from os.path import isfile, join
import re
import glob
import subprocess

timestamp = re.compile(".*(\d{8}T\d{6}).*")

incoming_dir = "/home/tiff2pdf/incoming"
active_dir = "/home/tiff2pdf/active"
output_resolution = 150


def timestamp2filename(timestamp):
	return incoming_dir+'/piscan-'+s+'*'

def tiff2ps(timestamp):
	fo = './tmp/'+timestamp+'.ps'
	subprocess.call(['convert',
		#'-colorspace RGB',
		'-density',
		str(output_resolution),
		timestamp2filename(timestamp),
		fo,
		])
	return fo

def ps2pdf(fi, fo):
	subprocess.call([
		'ps2pdf',
		'-sPAPERSIZE=legal',
		fi,
		fo,
		])
	
files = [f for f in listdir(incoming_dir)]

print ([f for f in files])

# Assert that all files from a batch have been transferred
scans = set([timestamp.search(f).group(1) for f in files])
for s in scans:
	count = 0
	for f in glob.glob(timestamp2filename(s)):
		total = int(f[-9:-5])
		count += 1
	if(total == count):
		print("I can start converting "+s)
		ps = tiff2ps(s)
		ps2pdf(ps, active_dir+'/'+s+'.pdf')
	else:
		print("Wrong number of "+s)


#datetime=`date +%Y%m%dT%H%M%S%Z`
#dir_incoming=~/incoming
#dir_active=~/active
#format=tiff
#
#n_pages=$(ls $dir_incoming/* | sort -nr | head -1 | xargs basename | cut -c28-31)
#
#echo $n_pages
#
#logger -t "tiff2pdf: $0" " - converting $format to ps"
##convert -colorspace RGB -density $resolution "$scan_dir/$filename-*.$format" "$scan_dir/$filename.ps"
##logger -t "scanbd: $0" "$SCANBD_ACTION - converting ps to pdf"
##ps2pdf  -sPAPERSIZE=legal "$scan_dir/$filename.ps" "$scan_dir/$filename.pdf"
##logger -t "scanbd: $0" "$SCANBD_ACTION - cleaning up $scan_dir/"
#
##rm -rf $scan_dir/$filename-*.tiff
##rm -rf $scan_dir/$filename.ps
##rm -rf $scan_dir/$filename.pdf
