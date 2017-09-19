# Halley's Skill Plugin API
# @author Kilari Teja
from halley.skills.tdl.utils import *
from halley.skills.exception import *
from halley.skills.tdl.operators.word import WORD
from halley.skills.tdl.operator import OpDescriptor
from halley.skills.tdl.preprocessor import Preprocessor

class RuleCompiler(object):
	"""
		the default rule compiler class
		glues together many processes
	"""

	def init(self):

		self.token_rules = [
			OpDescriptor(r"\(", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.PARTH_OPEN), # (
			OpDescriptor(r"\)", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.PARTH_CLSE), # )
		]

	def __init__(self, ops=[], preprocessor=None):
		
		# init self
		self.init()

		# list of ops to reg
		self.registerOps(ops)

		# resolve the preopr
		if preprocessor is None:
			self.preprocessor = Preprocessor()
		else:
			assert isinstance(preprocessor, Preprocessor)
			self.preprocessor = preprocessor

	def registerOp(self, op):
		op.register(self.token_rules)

	def registerOps(self, ops):
		for op in ops: self.registerOp(op)

	def rawTokenStream(self, rule):
		"""
			transforms a given rule text into
			a stream of tokens, refernces self
			.token_stream to extract patterns

			:param rule: rule as a string
			:return: token generator
		"""

		while rule != "":
			for tokenRule in self.token_rules:
				match = re.match(tokenRule.regex, rule)
				if match is not None:
					matchSpan = match.span()

					token = rule[:matchSpan[1]]
					token = self.preprocessor.token(token, tokenRule.label)

					yield Token(token, tokenRule)
					rule = rule[matchSpan[1]:]
					break
			else:
				if self.preprocessor.acceptable(rule[0]):
					rule = rule[1:]
				else:
					raise RuleCompilation(Messages.UNIDENTIFIED_SYM)
		else:
			raise StopIteration

	def tokeniseRule(self, rule):
		"""
			transforms a text rule into
			a list of tokens as opposed
			to a stream of tokens

			:param rule: rule as a string
			:return: list of tokens
			:rtype: list
		"""

		return list(self.rawTokenStream(rule))

	def makePostfix(self, rule):
		"""
			transforms a token rule
			(list) into a postfix stack

			:param rule: tokd rule
			:return: postfix stack
			:rtype: list
		"""

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

		for symbol in symbolStack:
			if symbol.label == Constants.TOKEN_TYPES.PARTH_OPEN:
				raise RuleLanguage(Messages.MISSING_PARTH_CLSE)

		postfixStack.extend(reversed(symbolStack))
		return postfixStack

	def defaultCompiler(self, postfixStack):
		"""
			the default compiler method,
			transforms a postfix stack
			into nested operator wrappers

			:param postfixStack: rule as a postfix stack
			:return: nested operator object
			:rtype: OPERATOR
		"""

		evaluationStack = []
		while postfixStack != []:
			element = postfixStack.pop(0)
			if element.label in Constants.TOKEN_TYPES.WORD:
				if element.label == Constants.TOKEN_TYPES.WORD:
					element = WORD(self.preprocessor.delimiter, element.token)

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

	def compile(self, rule):
		"""
			basically this just wraps intermediate
			transformation of rule to postfixStack
			and then to a compiled object

			:param rule: rule as text
			:return: OPERATOR object
			:rtype: OPERATOR
		"""
		assert isinstance(rule, str)
		
		rule = self.makePostfix(self.tokeniseRule(rule))
		return self.defaultCompiler(rule)

class DefaultRuleCompiler(RuleCompiler):
	"""
		a special RuleCompiler that has
		basic operator support built in
		though it can always be expanded
		usng registerOp()
	"""

	def __init__(self, *args, **kargs):

		# get all default ops
		from halley.skills.tdl.operators.boolean import NOT, AND, OR
		from halley.skills.tdl.operators.count import COUNT_OCCOURANCE
		from halley.skills.tdl.operators.ordering import PRE_OCCOURANCE, POST_OCCOURANCE

		ops = [
			WORD, NOT, AND, OR, COUNT_OCCOURANCE,
			PRE_OCCOURANCE, POST_OCCOURANCE
		]

		super(DefaultRuleCompiler, self).__init__(*args, ops=ops, **kargs)
