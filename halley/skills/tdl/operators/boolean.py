# @author Kilari Teja

from halley.skills.tdl.utils import PropMap, Constants, Token
from halley.skills.tdl.operator import OPERATOR, Descriptor
from halley.skills.tdl.operator import resolveParameterMagAndDirn, Result

class AND(OPERATOR):

	DESCRIPTOR = [
		Descriptor(r"\&", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR),
		Descriptor(r"\,", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR)
	]

	def __init__(self, selfToken, *args):
		lamda = lambda a, b: a if a.val < b.val else b
		super(AND, self).__init__(lamda, selfToken, *args)

class OR(OPERATOR):

	DESCRIPTOR = Descriptor(r"\|", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR)

	def __init__(self, selfToken, *args):
		lamda = lambda a, b: a if a.val > b.val else b
		super(OR, self).__init__(lamda, selfToken, *args)

class NOT(OPERATOR):

	DESCRIPTOR = Descriptor(r"\!", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.UNARY_OP)

	def __init__(self, selfToken, arg):
		super(NOT, self).__init__(lambda a, b: None, selfToken, arg)
		self.label = Constants.TOKEN_TYPES.COMPOUND_EXPR

	def eval(self, text):
		val = self._args[0].eval(text).val
		return Result.FALSE() if val > -1 else Result(0, None)
