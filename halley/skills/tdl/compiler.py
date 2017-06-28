# Halley's Skill Plugin API
# @author Kilari Teja

from halley.skills.tdl.utils import *
from halley.skills.exception import *
from halley.skills.tdl.operator import Descriptor

from halley.skills.tdl.operators.word import WORD
from halley.skills.tdl.operators.boolean import NOT, AND, OR
from halley.skills.tdl.operators.count import COUNT_OCCOURANCE
from halley.skills.tdl.operators.ordering import PRE_OCCOURANCE, POST_OCCOURANCE

import re

# Register your operator to this list, 
# Preferably append its descriptor here	
TOKEN_RULES = [
	Descriptor(r"\(", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.PARTH_OPEN),	# (
	Descriptor(r"\)", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.PARTH_CLSE),	# )
]

OR.register(TOKEN_RULES)
NOT.register(TOKEN_RULES)
AND.register(TOKEN_RULES)
WORD.register(TOKEN_RULES)
PRE_OCCOURANCE.register(TOKEN_RULES)
POST_OCCOURANCE.register(TOKEN_RULES)
COUNT_OCCOURANCE.register(TOKEN_RULES)

# Preprocessors
def preprocessRuleText(text):
	return text.lower()

def tokenPreprocessor(token, label):
	return token

def simpleSpaceDelimiter(text):
	return text.split()

def tokeniseRule(rule, tokenProcess=[Constants.TOKEN_TYPES.WORD], tokenProcessor=tokenPreprocessor):
	assert isinstance(tokenProcess, list)

	while rule != "":
		for tokenRule in TOKEN_RULES:
			match = re.match(tokenRule.regex, rule)
			if match is not None:
				matchSpan = match.span()

				token = rule[:matchSpan[1]]
				if tokenRule.label in tokenProcess:
					token = tokenProcessor(token, tokenRule.label)

				yield Token(token, tokenRule)
				rule = rule[matchSpan[1]:]
				break
		else:
			rule = rule[1:]
	else:
		raise StopIteration

# Its a Stack based Expression Parser
def makePostfix(rule):
	assert isinstance(rule, list)

	symbolStack, postfixStack = [], []
	for symbol in rule:
		symbolType = symbol.label

		if symbolType == Constants.TOKEN_TYPES.WORD:
			postfixStack.append(symbol)
		elif symbolType == Constants.TOKEN_TYPES.PARTH_OPEN:
			symbolStack.append(symbol)
		elif symbolType == Constants.TOKEN_TYPES.PARTH_CLSE:
			for _ in xrange(len(symbolStack)):
				symbol = symbolStack.pop(-1)
				if symbol.label == Constants.TOKEN_TYPES.PARTH_OPEN: break
				postfixStack.append(symbol)
			else:
				raise RuleLanguage(Messages.BAD_RULE)

		elif symbolType in [Constants.TOKEN_TYPES.OPERATOR, Constants.TOKEN_TYPES.UNARY_OP]:
			while len(symbolStack) > 0 and symbolStack[-1] != Constants.PARTH_OPEN_SYM:
				if symbolStack[-1].precedence > symbol.precedence:
					postfixStack.append(symbolStack.pop())
				else:
					break

			symbolStack.append(symbol)

	# Count PARTH_OPEN
	for symbol in symbolStack:
		if symbol.label == Constants.TOKEN_TYPES.PARTH_OPEN:
			raise RuleLanguage(Messages.MISSING_PARTH_CLSE)

	postfixStack.extend(reversed(symbolStack))
	return postfixStack

def defaultCompilerFunc(postfixStack, wordDelimiterFunc):
	evaluationStack = []
	while postfixStack != []:
		element = postfixStack.pop(0)
		if element.label in Constants.TOKEN_TYPES.WORD:
			if element.label == Constants.TOKEN_TYPES.WORD:
				element = WORD(wordDelimiterFunc, element.token)

			evaluationStack.append(element)
		
		# Binary Operator
		elif element.label == Constants.TOKEN_TYPES.OPERATOR:
			assert len(evaluationStack) > 1, RuleCompilation(Messages.BAD_COMPOUND_EXPR)

			evaluationStack.append(
				element.clas(element, *(evaluationStack.pop(), evaluationStack.pop())))
		
		# Unary Operator
		elif element.label == Constants.TOKEN_TYPES.UNARY_OP:
			assert len(evaluationStack) > 0, RuleCompilation(Messages.BAD_COMPOUND_EXPR)

			evaluationStack.append(
				element.clas(element, evaluationStack.pop()))
			
	assert len(evaluationStack) == 1, RuleCompilation(Messages.COMPILATION_ERROR)
	return evaluationStack[0]

def ruleCompiler(rule, compiler=defaultCompilerFunc, requiresPostfixExpr=True, defaultDelimiterFunc=simpleSpaceDelimiter):
	if isinstance(rule, str):
		rule = list(tokeniseRule(rule))
	
	if requiresPostfixExpr:
		rule = makePostfix(rule)
	
	return compiler(rule, defaultDelimiterFunc)
