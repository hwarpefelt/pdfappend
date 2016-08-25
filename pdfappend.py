# Copyright (c) 2016 Henrik Warpefelt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
'''
	File name: pdfappend.py
	Author: Henrik Warpefelt
	Date created: 2016-08-25
	Date last modified: 2016-08-25
	Python Version: 2.7.9
'''
from PyPDF2 import PdfFileMerger
import argparse

class PDFAppend:
	"""
	PDFAppend does the gruntwork. Basically wraps PyPDF2.
	"""
	def __init__(self, L, o, v=False):
		"""
		Construct a new 'PDFAppend' object. 

		:param L: A list of strings describing PDF file names
		:param o: A string describing the output file name
		:param v: A boolean toggle for verbose mode (optional)
		:return: returns nothing
		"""
		self.pdfs = L
		self.outname = o
		self.verbose = v
		self.merger = PdfFileMerger()
		if self.verbose:
			print "+++ PDFAppend set up to create " + str(self.outname) + " from :" + str(self.pdfs)

	def process(self):
		"""
		Processes the input files. 

		:return: True if successful, False if not. 
		"""
		if self.verbose:
			print "+++ Processing initiated"
		if (len(self.pdfs) > 0 and len(self.outname) > 0):
			if self.verbose:
				print "+++ Data valid. Continuing..."
			for pdf in self.pdfs:
				try:
					if self.verbose:
						print "+++ Appending " + str(pdf)
					f = open(pdf, "rb")
					self.merger.append(f)
				except IOError:
					print "!!! I/O Error: Cannot open file " + str(pdf)
					return False
			if self.verbose:
				print "+++ All files appended. Proceeding to write file " + str(self.outname)
			try:
				fout = open(self.outname, "wb")
				self.merger.write(fout)
				if self.verbose:
					print "+++ File " + str(self.outname) + " written."
			except IOError:
				print "!!! I/O Error: Cannot write to file " + str(self.outname)
				return False
			return True
		else:
			if self.verbose:
				print "!!! Failed to create PDF file."
				if len(self.pdfs <= 0):
					print "!!! No files to add"
				if len(self.outname <= 0):
					print "!!! Output name not specified"
			return False

	def set_verbose(self):
		"""
		Sets the PDFAppend object to verbose mode.
		"""
		self.verbose = True

def main():
	"""
	Main class. Processes command line arguments and sets up a PDFAppend object. 
	"""
	parser = argparse.ArgumentParser(description="pdfappend is a utility for appending PDF files.")
	parser.add_argument('-o', metavar='output', type=str, default='output.pdf', help='The name of the output file')
	parser.add_argument('-v', action='store_const', const=True, help='Produce verbose input')
	parser.add_argument('pdf', metavar="pdf", type=str, nargs='+', help='A PDF file to be appended')
	args = parser.parse_args()
	p = PDFAppend(args.pdf, args.o)
	if (args.v):
		verbose = True
		print "+++ Setting verbose mode"
		p.set_verbose()
	if not p.process():
		print "!!! Failed to append PDF files"

if __name__ == "__main__": main()
