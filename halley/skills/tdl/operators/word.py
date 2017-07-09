# @author Kilari Teja

from halley.skills.tdl.utils import PropMap, Constants
from halley.skills.tdl.operator import OPERATOR, OpDescriptor, Result

# ?WORD is a simple delimited word,
# '?' here isn't a operator
class WORD:

	NON_DELIMITED_WORD_STARTS_WITH = "?"
	DESCRIPTOR = [
		OpDescriptor(r"[\?]?\'[0-9A-Za-z ]+\'", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.WORD),
		OpDescriptor(r'[\?]?\"[0-9A-Za-z ]+\"', Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.WORD),
		OpDescriptor(r"[\?]?[0-9A-Za-z_]+",	Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.WORD)
	]

	@classmethod
	def register(clas, tokenStore):
		OPERATOR.registerStatic(clas, tokenStore)

	def __init__(self, wordDelimiterFunc, word):
		self.label = Constants.TOKEN_TYPES.WORD
		self._word = word

		self._delimited = not self._word.startswith(WORD.NON_DELIMITED_WORD_STARTS_WITH)
		self._delimiter = wordDelimiterFunc

		if not self._delimited:
			self._word = self._word[1:]

		self._word = self.sanitise(self._word)

		# If the _word contains a space, Its automatically delimited
		if any(map(lambda l: self._word.find(l) != -1, wordDelimiterFunc(None))):
			self._delimited = False

	def count(self, text):
		text = self._delimiter(text) if self._delimited else text
		return text.count(self._word)

	def bool(self, text):
		return self.eval(text).val != -1

	def eval(self, text):
		originalText, text = text, self._delimiter(text) if self._delimited else text
		if self._delimited:
			try:
				baseString, baseIndex = "".join(text[:text.index(self._word)+1]), 0

				while len(baseString) != 0:
					if baseString[0] == originalText[0]:
						baseString = baseString[1:]

					originalText = originalText[1:]
					baseIndex += 1

				return Result(baseIndex - len(self._word), self)
			except:
				return Result.FALSE()
		else:
			return Result(text.find(self._word), self)

	def sanitise(self, token):
		return token[1:-1] if token.startswith("'") or token.startswith('"') else token

	literal = property(lambda self: self._word)
