# import our classes and os
from WordTracker import *
from WordExtractor import *
import os


class PathIterator:
	"""
	An iterator which iterates over all the directories and files
	in a given path (note - in the path only, not in the
	full depth). There is no importance to the order of iteration.
	"""

	def __init__(self, path):
		# set our instances for the path, the directories and files inside
		# it and the empty list of full paths
		self.path = path
		self.content = os.listdir(path)
		self.list_paths = []


	def __iter__(self):
		"""
		An iter method that creates our list of full paths.
		"""
		for item in self.content:
			self.list_paths.append(os.path.join(self.path, item))
		return self

	def __next__(self):
		"""
		Next method that returns the first index of our list of full paths.
		If the list is empty returns a StopIteration
		"""
		if len(self.list_paths) == 0:
			raise StopIteration
		return self.list_paths.pop()


def path_iterator(path):
	"""
	Returns an iterator to the current path's filed and directories.
	Note - the iterator class is not outlined in the original
	version of this file - but rather is should be designed
	and implemented by you.
	:param path: A (relative or an absolute) path to a directory.
	It can be assumed that the path is valid and that indeed it
	leads to a directory (and not to a file).
	:return: An iterator which returns all the files and directories
	in the *current* path (but not in the *full depth* of the path).
	"""
	# create an object using the PathIterator class, this object is an
	# iterator containing the list of items in the given directory
	file_path = PathIterator(path)
	#return the object
	return file_path


def print_tree_helper(path, first_path, sep):
	'''
	Helper function for our print_tree function that allows us to save the
	first path given. And using it, prints a tree of the absolute path
	recursively.
	:param path: The path we want to explore
	:param first_path: The first path which we want to save and use for spacing
	:param sep: the separator between branches in our tree
	:return: None
	'''
	# set a variable to the iterator in our previous function that holds all
	#  the paths inside the directory
	recur_index = 1
	list_directories = path_iterator(path)
	# for every path in that iterator, split it into a list of paths without
	#  the "/" character
	for directory in list_directories:
		split_directory = directory.split('/')
		# set place to equal the length of the full path minus the first
		# path we got - 1. This gives us the proper spacing for our tree.
		place = len(split_directory) - len(first_path.split('/')) - recur_index
		# if the path given leads to a directory, print the directory and
		# then explore it recursively by calling our function again.
		if os.path.isdir(directory):
			print((place * sep) + split_directory[-1])
			print_tree_helper(directory, first_path, sep)
		# if it isn't a directory, just print it
		else:
			print((place * sep) + split_directory[-1])


def print_tree(path, sep='  '):
	"""
	Print the full hierarchical tree of the given path.
	Recursively print the full depth of the given path such that
	only the files and directory names should be printed (and not
	their full path), each in its own line preceded by a number
	of separators (indicated by the sep parameter) that correlates
	to the hierarchical depth relative to the given path parameter.
	:param path: A (relative or an absolute) path to a directory.
	It can be assumed that the path is valid and that indeed it
	leads to a directory (and not to a file).
	:param sep: A string separator which indicates the depth of
	current hierarchy.
	"""
	# call our helper function that allows us to save the first path
	return print_tree_helper(path, path, sep)


def file_with_all_words(path, word_list):
	"""
	Find a file in the full depth of the given path which contains
	all the words in word_list.
	Recursively go over  the files in the full depth of the given
	path. For each, check whether it contains all the words in
	word_list and if so return it.
	:param path: A (relative or an absolute) path to a directory.
	In the full path of this directory the search should take place.
	It can be assumed that the path is valid and that indeed it
	leads to a directory (and not to a file).
	:param word_list: A list of words (of strings). The search is for
	a file which contains this list of words.
	:return: The path to a single file which contains all the
	words in word_list if such exists, and None otherwise.
	If there exists more than one file which contains all the
	words in word_list in the full depth of the given path, just one
	of theses should be returned (does not matter which).
	"""
	# save the iterator object from our previous function as a variable
	list_path = path_iterator(path)
	# set our default found_file to None, this will change if we find a file
	found_file = None
	# run over the files in our path
	for item in list_path:
		# if the item is a directory, recall our function recursively and
		# explore the inner directory
		if os.path.isdir(item):
			found_file = file_with_all_words(item, word_list)
		# if it's a file, search the file for the words in our list
		else:
			# create an object which holds our list of words using WordTracker
			our_words = WordTracker(word_list)
			# create an object that holds our file using WordExtractor.py
			file = WordExtractor(item)
			# for that loops over the iterator we created and returns a word
			# each time
			for word in file:
				# use our encounter() method from WordTracker on our word
				our_words.encounter(word)
				# check if after using the =method all our words were found,
				# if they were return the file name
				if our_words.encountered_all():
					return item
	# return the found file, if none was found it'll return None
	return found_file


