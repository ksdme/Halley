from halley.skills.tdl.preprocessor import Preprocessor, PrepDescriptor
from halley.skills.exception import Messages, RulePreprocessor
import re

class SPREAD(Preprocessor):
	DESCRIPTOR = PrepDescriptor(Preprocessor.CONSUMES_RAW)
	
	SYMBOLS = {
		"AND": "&",
		"OR" : "|",
		"NOT": "!"
	}

	REGEX = r"\[([\{AND}\{OR}\{NOT}]?[a-zA-Z_]+)\]".format(
			AND=SYMBOLS["AND"],
			OR=SYMBOLS["OR"],
			NOT=SYMBOLS["NOT"])

	@staticmethod
	def act(data, flatMap):
		allHits = re.findall(SPREAD.REGEX, data)
		for hit in allHits:
			hitSymbol = hit[0]

			try:
				replaceStr, listTo = "", map(lambda l: '"{}"'.format(l), flatMap[hit[1:]])
			except KeyError:
				raise RulePreprocessor(Messages.PREPROCESSING_KEY_ERROR)

			if hitSymbol == SPREAD.SYMBOLS["AND"]:
				replaceStr = "({})".format(SPREAD.SYMBOLS["AND"].join(listTo))

			elif hitSymbol == SPREAD.SYMBOLS["OR"]:
				replaceStr = "({})".format(SPREAD.SYMBOLS["OR"].join(listTo))

			elif hitSymbol == SPREAD.SYMBOLS["NOT"]:
				listTo = map(lambda l: "!{}".format(l), listTo)
				replaceStr = "({})".format(SPREAD.SYMBOLS["AND"].join(listTo))

			if replaceStr != "":
				data.replace("[{}]".format(hit), replaceStr)
			else:
				raise RulePreprocessor(Messages.PREPROCESSING_ERROR)
