# @author Kilari Teja
import re

class PropMap(object):

	def __init__(self, **kargs):
		self._kargs = kargs
		for key in kargs:
			setattr(self, key, kargs[key])

	def __str__(self):
		return str(self._kargs)

class Constants:

	TOKEN_TYPES = PropMap(
		COMPOUND_EXPR 	=	"COMPOUND_EXPR",
		PARTH_OPEN	=	"PARTH_OPEN",
		PARTH_CLSE 	=	"PARTH_CLSE",
		OPERATOR 		=	"OPERATOR",
		UNARY_OP		=	"UNARY_OP",
		WORD 		=	"WORD"
	)

	PRECEDENCE = PropMap(
		HIGH		= 3,
		MEDIUM	= 2,
		LOW		= 1
	)

	PARTH_OPEN_SYM, PARTH_CLSE_SYM   	= "(", ")" 
	AND_SYM, OR_SYM, NOT_SYM     	 	= "&", "|", "!" 
	PRE_OCCOURANCE_NON_PARAM_SYM		= "<=" 
	POST_OCCOURANCE_NON_PARAM_SYM		= "=>"
	DELIMITED_WORD_STARTS_WITH 		= "?"

class Token(PropMap):

	def __init__(self, token, tokenRule):
		super(Token, self).__init__(
			clas=tokenRule.clas,
			token=token,
			label=tokenRule.label,
			precedence=tokenRule.precedence
		)

class StatsCollector(PropMap):
	
	def __init__(self):
		self._words, self._trues = 0, 0

	def inc(self, by=1):
		self._words += 1

	def wordInc(self, by=1):
		self._trues += 1

	def getRating(self):
		return self._trues/float(self._words)

	words = property(lambda self: self._words)
	trues = property(lambda self: self._trues)

class Pipeline(object):

	def __init__(self, actions=[]):
		self.init()
		self.setUpActions(actions)

	def __call__(self, data):
		return self.do(data)

	def init(self):
		self._actions = []

	def setUpActions(self, actions):
		assert isinstance(actions, list)

		self.init()
		for action in actions:
			self.addAction(action)

	def addAction(self, action):
		if isinstance(action, tuple):
			self._actions.append(action)
		else:
			self._actions.append((action, lambda *args: []))

	def do(self, data):
		for action in self._actions:
			data = action[0](data, action[1]())

		return data

	actions = property(lambda self: self._action)
