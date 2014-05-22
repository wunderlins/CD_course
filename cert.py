#!/usr/bin/env python

# expect parameters as arguments
# parameters:
#   1 $$name$$
#   2 $$title$$
#   3 $$date$$
#   4 $$location$$
#   5 $$trainer$$

import sys

def usage():
	print """

#   1 $$name$$
#   2 $$title$$
#   3 $$date$$
#   4 $$location$$
#   5 $$trainer$$
"""

def main(argv=None):
	
	args = ["exe", "name", "title", "date", "location", "trainer"]
	
	if argv is None:
		argv = sys.argv
	
	if (len(sys.argv) < 6):
		print("Argument error\n")
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
	except:
		print "Unexpected error:", sys.exc_info()[0]
		fp.close()
		sys.exit(1)
	
	buffer = fp.read();
	fp.close()
	
	# subsitute values in svg
	for (i, keyword) in enumerate(args):
		#sys.stdout.write("[%d] %s: %s\n " % (i, keyword, argv[i]))
		repl = '$$' + keyword + '$$'
		#sys.stdout.write("%s %s\n" % (repl, argv[i]))
		buffer = buffer.replace(repl, argv[i])
	
	print buffer;
	
	# convert svg to pdf
	
	# stream pdf result
	
	

if __name__ == "__main__":
	sys.exit(main())
