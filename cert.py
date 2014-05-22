#!/usr/bin/env python

# expect parameters as arguments
# parameters:
#   1 $$name$$
#   2 $$title$$
#   3 $$date$$
#   4 $$location$$
#   5 $$trainer$$

import sys, os
from subprocess import call

is_cgi = False
#check if this is a cgi request
if 'REQUEST_METHOD' in os.environ :
	# Import modules for CGI handling 
	import cgi, cgitb 
	cgitb.enable()
	# Create instance of FieldStorage 
	#form = cgi.FieldStorage() 
	is_cgi = True

def usage():
	print """

#   1 $$name$$
#   2 $$title$$
#   3 $$date$$
#   4 $$location$$
#   5 $$trainer$$
"""

inkscape_bin = "/usr/bin/inkscape"
arg = ["exe", "name", "title", "date", "location", "trainer"]

def main(argv=None):
	#print "Content-type: text/plain\n\n"
	#print argv
	#print 1
	#sys.exit(0)
	
	if argv is None:
		argv = sys.argv
	
	#print "Content-type: text/plain\n\n"
	#print "Hello %s" % argv[0]
	#sys.exit(0)
	
	if (len(argv) < 6):
		print("Argument error %d\n") % len(sys.argv)
		print argv
		usage()
		sys.exit(1)
	
	# debug
	#print("name: %s\ntitle: %s\ndate: %s\nlocation: %s\ntrainer: %s\n") % \
	#	(argv[1], argv[2], argv[3], argv[4], argv[5])
	
	# load svg template
	template = "./cert_cd_1_template.svg"
	try:
		fp = open(template, "r")
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		fp.close()
		sys.exit(1)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		fp.close()
		sys.exit(1)
	
	buffer = fp.read();
	fp.close()
	
	# subsitute values in svg
	for (i, keyword) in enumerate(arg):
		#sys.stdout.write("[%d] %s: %s\n " % (i, keyword, argv[i]))
		repl = '$$' + keyword + '$$'
		#sys.stdout.write("%s %s\n" % (repl, argv[i]))
		buffer = buffer.replace(repl, argv[i])
	
	# write temp svg file
	pid = os.getpid()
	
	# TODO: figure out absolute path
	file_base = "./tmp/out-%d" % (pid)
	file_svg = file_base + ".svg"
	
	#sys.stdout.write("%s\n" % file_svg)
	#print buffer;
	try:
		fp = open(file_svg, "wb+")
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		fp.close()
		sys.exit(1)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		fp.close()
		sys.exit(1)
	
	fp.write(buffer)
	fp.close()
	
	# convert svg to pdf
	# /usr/bin/inkscape --export-pdf=FILENAME
	file_pdf = file_base + ".pdf"
	call([inkscape_bin, "--export-pdf="+file_pdf, file_svg])
	
	statinfo = os.stat(file_pdf)
	#print "Content-type: text/plain\n\n"
	#print "aaa"
	#sys.stdout.write("Content-length: %d\n\n" % statinfo.st_size)
	#sys.exit(0)
	
	# stream pdf result
	sys.stdout.write("Content-type: application/pdf\n")
	#print file_pdf# + " - %d\n" % statinfo.st_size
	sys.stdout.write("Content-length: %d\n" % statinfo.st_size)
	sys.stdout.write("Content-disposition: inline; filename='CD_certifcate.pdf'\n\n")
	
	try:
		fp = open(file_pdf, "r")
	except IOError as e:
		print "I/O error({0}): {1}".format(e.errno, e.strerror)
		fp.close()
		sys.exit(1)
	except:
		print "Unexpected error:", sys.exc_info()[0]
		fp.close()
		sys.exit(1)
	print fp.read()
	fp.close()
	
	# remove files
	os.remove(file_svg)
	os.remove(file_pdf)
	
if __name__ == "__main__":
	a = None
	if (is_cgi):
		form = cgi.FieldStorage() 
		
		a = ["cgi", "", "", "", "", ""]
		#a.append(form.getValue(args[1]))
		
		#print "Content-type: text/html\n\n"
		#print args.index("name")
		for i in form.keys():
			#print i
			ix = arg.index(i)
			#print ix
			#print i + " %d" % ix
			#print form[i].value + " <br/>"
			a[ix] = form[i].value
			#print i + " " + form[i].value +"\n"
			
		#print 1
		#print a[0]
		#print a[1]
		#print a[2]
		#print a[3]
		#print a[4]
		#print a[5]
		#sys.exit(0)
		#a.append(form.getValue(arg[1]))
		#a.append(form.getValue(arg[2]))
		#a.append(form.getValue(arg[3]))
		#a.append(form.getValue(arg[4]))
		#a.append(form.getValue(arg[5]))
		
	sys.exit(main(a))
