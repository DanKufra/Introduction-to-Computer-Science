#!/usr/bin/env python3


class WordExtractor(object):
	"""
	This class should be used to iterate over words contained in files.
	The class should maintain space complexity of O(1); i.e, regardless
	of the size of the iterated file, the memory requirements ofa class
	instance should be bounded by some constant.
	To comply with the space requirement, the implementation may assume
	that all words and lines in the iterated file are bounded by some
	constant, so it is allowed to read words or lines from the
	iterated file (but not all of them at once).
	"""
	def __init__(self, filename):
		"""
		Initiate a new WordExtractor instance whose *source file* is
		indicated by filename.
		:param filename: A string representing the path to the instance's
		*source file*
		"""
		# our position in the file, starts at the start
		self.last_pos = 0
		# save our filename
		self.file = filename
		# list that holds the content of the line
		self.content = []
		# instances that hold our list length and counter
		self.list_length = len(self.content)
		self.counter = 0

	def __iter__(self):
		"""
		Returns an iterator which iterates over the words in the
		*source file* (i.e - self)
		:return: An iterator which iterates over the words in the
		*source file*
		"""
		return self

	def _open_close_file(self):
		"""
		Method that opens , reads our line, saves our place and closes our
		file
		:return: None
		"""
		# set the file to be the current open file
		file = open(self.file, 'r')
		file.seek(self.last_pos)
		# save self.content as the next line in the file
		self.content = file.readline()
		# save our last position in the file
		self.last_pos = file.tell()
		# close the file
		file.close()

	def _next_line(self):
		"""
		Method that recognizes when to proceed to the next line, calls our
		open_close method and then splits the line into a list. Also
		recognizes when the file has been read and raises StopIteration()
		:return: None
		"""
		self._open_close_file()
		# if the next line was the end of the file, raise the StopIteration()
		if self.content == "":
			# set our position to the beginning of the file if we'd like to
			# use it again
			self.last_pos = 0
			raise StopIteration()
		# if the line is an empty line but not the end of the file, move on
		# to the next line
		while self.content.isspace():
			self._open_close_file()
		# split the line into a list of words
		self.content = self.content.split()
		# save the length of the list
		self.list_length = len(self.content)

	def __next__(self):
		"""
		Make a single word iteration over the source file.
		:return: A word from the file.
		"""
		EMPTY = 0
		#check if the length of our list is 0, if it is proceed to next line
		if self.list_length == EMPTY:
			self._next_line()
		# if there are still unread words in the list, add one to the
		# counter and return the index of the next word in the list
		if self.counter < self.list_length:
			self.counter += 1
			return self.content[self.counter - 1]
		# reset our counter and list length to 0
		self.counter = EMPTY
		self.list_length = EMPTY
		# recall our __next__() method
		return self.__next__()






