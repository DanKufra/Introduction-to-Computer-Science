#!/usr/bin/env python3
import random


def quicksort(lst):
	'''
	quicksort function that calls our helper function.
	:param lst:
	:return:lst
	'''
	quick_sort_helper(lst, 0, len(lst) - 1)
	return lst


def quick_sort_helper(lst, start, end):
	'''

	:param lst: our list
	:param start: starting index
	:param end: end index
	:return: our list
	'''
	# if the difference between the last and first index is larger than 0, sort
	if end - start > 0:
		# set our pivot to a random index between start and end
		pivot = lst[random.randint(start, end)]
		# set new variable names for start and end we can change
		left = start
		right = end
		# while the right index is bigger than the left
		while left < right:
			# while the word in the left index is smaller than our pivot
			# move the left index by 1
			while lst[left] < pivot:
				left += 1
			# while the word in the right index is larger than our pivot
			# move the right index by 1
			while lst[right] > pivot:
				right -= 1
			# if the left index is smaller  or equal to the right, swap them
			#  and move by 1
			if left <= right:
				lst[left], lst[right] = lst[right], lst[left]
				left += 1
				right -= 1
		# recursively call the helper function again with the list split
		# into two parts.
		quick_sort_helper(lst, start, right)
		quick_sort_helper(lst, left, end)
	# once the difference between the start and end is lower than 0, return lst
	return lst

class WordTracker(object):
	"""
	This class is used to track occurrences of words.
	The class uses a fixed list of words as its dictionary
	(note - 'dictionary' in this context is just a name and does
	not refer to the pythonic concept of dictionaries).
	The class maintains the occurrences of words in its
	dictionary as to be able to report if all dictionary's words
	were encountered.
	"""

	def __init__(self, word_list):
		"""
		Initiates a new WordTracker instance.
		:param word_list: The instance's dictionary.
		"""
		# copy our dictionary to to another list
		self.dictionary = word_list[:]
		# set our sorted dictionary and list of found words to empty lists
		self.sorted_dictionary = []
		self.found_words = []


	def __contains__(self, word):
		"""
		Check if the input word in contained within dictionary.
		For a dictionary with n entries, this method guarantees a
		worst-case running time of O(n) by implementing a
		binary-search.
		:param word: The word to be examined if contained in the
		dictionary.
		:return: True if word is contained in the dictionary,
		False otherwise.
		"""
		# if the sorted dictionary is empty, then sort it using our
		# quicksort functions
		if not self.sorted_dictionary:
			new_lst = self.dictionary
			self.sorted_dictionary = quicksort(new_lst)
		# save our sorted dictionary into a variable and set our start and
		# end values
		lst = self.sorted_dictionary
		start = 0
		end = len(lst) - 1
		# use a binary search to find if a word is in our sorted list
		while start <= end:
			# find the middle index of our list, if the word in the index is
			# equal to the word we are searching for return True
			middle_indx = (start + end) // 2
			if word == lst[middle_indx]:
				return True
			# if the word in the index is larger than the word we are
			# searching for, move the middle index left by 1
			elif lst[middle_indx] > word:
				end = middle_indx - 1
			# otherwise it must be bigger, so move it right by 1
			else:
				start = middle_indx + 1
		# if our loop ended without finding it, return False
		return False

	def encounter(self, word):
		"""
		A "report" that the give word was encountered.
		The implementation changes the internal state of the object as
		to "remember" this encounter.
		:param word: The encountered word.
		:return: True if the given word is contained in the dictionary,
		False otherwise.
		"""
		# checks whether the dictionary contains a word.
		if self.__contains__(word):
			# if it does, and the words isn't in our list of encountered
			# words, add it
			if word not in self.found_words:
				self.found_words.append(word)
			# return True regardless
			return True
		# if it isn't in the dictionary, return False
		return False


	def encountered_all(self):
		"""
		Checks whether all the words in the dictionary were
		already "encountered".
		:return: True if for each word in the dictionary,
		the encounter function was called with this word;
		False otherwise.
		"""
		# since our list of found words has no duplicate words, we can just
		# make sure the lengths  of the dictionary and it are equal (and
		# above 0)
		if len(self.found_words) == len(self.sorted_dictionary) and (len(
				self.sorted_dictionary) > 0):
			# if they are we return True
			return True
		# otherwise we return False
		return False


	def reset(self):
		"""
		Changes the internal representation of the instance such
		that it "forget" all past encounters. One implication of
		such forgetfulness is that for encountered_all function
		to return True, all the dictionaries' entries should be
		called with the encounter function (regardless of whether
		they were previously encountered ot not).
		"""
		# we set our found words list to be an empty list
		self.found_words = []
