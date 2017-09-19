"""
	@author ksdme
	provides a basic preprocessor
	for rules and tokens
"""
import re

class Preprocessor(object):
	"""
		provides default set of
		rule preprocessors
	"""

	def rule(self, ruleText):
		"""
			responsible for preprocessing
			a given rule before it is tokenised

			:param ruleText: the raw rule as string
			:return: returns the processed rule text
			:rtype: string
		"""

		return ruleText.lower().strip()

	def token(self, token, label):
		"""
			token units preprocessor
			
			:param token: token unit
			:return: processed token
			:rtype: string
		"""

		return token

	def delimiter(self, ruleText):
		"""
			delimits a multi word
			sentence
		"""

		# default delim
		if ruleText is None:
			return [" "]

		return ruleText.split()

	def acceptable(self, char):
		"""
			checks for if a giveb char
			is acceptable and is not a
			special character
		"""

		return char in [" ", "\t", "\n"]
