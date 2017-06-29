# @author Kilari Teja

from halley.skills.tdl.utils import PropMap, Constants
from halley.skills.tdl.operator import OPERATOR, OpDescriptor
from halley.skills.tdl.operator import resolveBinaryParameterMagAndDirn, Result

# All the delegations are to turn off the
# parameterized ordering operators
class _OCCOURANCE_ORDER(OPERATOR):
	REVERSE_MAG_SYM = "!"

	def __init__(self, selfToken, *args):
		# Delegated
		# self._mag, self._dirn = resolveBinaryParameterMagAndDirn(
		# 	self.__class__.PARAM_SELECTOR,
		# 	_OCCOURANCE_ORDER.REVERSE_MAG_SYM, selfToken.token)

		super(_OCCOURANCE_ORDER, self).__init__(lambda a, b: None, selfToken, *args)

class PRE_OCCOURANCE(_OCCOURANCE_ORDER):

	PARAM_SELECTOR = r"\<\[([\!]?[0-9]+)\]"
	DESCRIPTOR = [
		# Delegated: OpDescriptor(PARAM_SELECTOR, Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR),
		OpDescriptor(r"\<\=", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR)
	]

	def __init__(self, selfToken, lhs, rhs):
		super(PRE_OCCOURANCE, self).__init__(selfToken, lhs, rhs)

	# Delegated, Supports parameterised
	# def _chopText(self, text, position):
	# 	mag, dirn, chop  = self._mag, self._dirn, None
	# 	mag = 0 if mag is None else mag
	# 	if not dirn:
	# 		chop = (0, position-mag)
	# 	else:
	# 		chop = (position-mag, position)

	# 	return text[chop[0]:chop[1]]

	# Delegated, Supports parameterised
	# def _eval(self, text):
	# 	lhs, rhs = self._args[0].eval(text), self._args[1]
	# 	if lhs.val == -1:
	# 		return lhs

	# 	rhs = rhs.eval(self.chopText(text, lhs.val))

	# 	if rhs.val == -1:
	# 		return rhs
	# 	else:
	# 		if (not self._dirn) or self._mag is None:
	# 			return Result(val=rhs.val, word=rhs.word)
	# 		else:
	# 			return Result(val=rhs.val+(lhs.val-self._mag), word=rhs.word)


	def chopText(self, text, position):
		return text[:position]

	def eval(self, text):
		lhs, rhs = self._args[0].eval(text), self._args[1]
		if lhs.val == -1:
			return lhs

		rhs = rhs.eval(self.chopText(text, lhs.val))
		if rhs.val == -1:
			return rhs
		else:
			return Result(val=rhs.val, word=rhs.word)
	
class POST_OCCOURANCE(_OCCOURANCE_ORDER):

	PARAM_SELECTOR = r"\[([\!]?[0-9]+)\]\>"
	DESCRIPTOR = [
		# Delegated: OpDescriptor(PARAM_SELECTOR, Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR),
		OpDescriptor(r"\=\>", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR)
	]

	def __init__(self, selfToken, lhs, rhs):
		super(POST_OCCOURANCE, self).__init__(selfToken, rhs, lhs)

	# Delegated, Supports parameterised
	# def _chopText(self, text, position, length):

	# 	mag, dirn, chop  = self._mag, self._dirn, None
	# 	mag = 0 if mag is None else mag
	# 	wordTrailingChar = position + length
	# 	if not dirn:
	# 		chop = (wordTrailingChar + mag, None)
	# 	else:
	# 		chop = (wordTrailingChar, wordTrailingChar + mag)

	# 	return text[chop[0]:chop[1]]

	# Delegated, Supports parameterised
	# def _eval(self, text):
	# 	lhs, rhs = self._args[0].eval(text), self._args[1]
	# 	if lhs.val == -1:
	# 		return lhs

	# 	rhs = rhs.eval(self.chopText(text, lhs.val, len(lhs.word.literal)))
	# 	if rhs.val == -1:
	# 		return Result.FALSE()
	# 	else:
	# 		return Result(val=lhs.val+lhs.val+len(lhs.word.literal), word=rhs.word)

	def chopText(self, text, position, leng):
		return text[position+leng:]

	def eval(self, text):
		lhs, rhs = self._args[0].eval(text), self._args[1]
		if lhs.val == -1:
			return lhs

		rhs = rhs.eval(self.chopText(text, lhs.val, len(lhs.word)))
		if rhs.val == -1:
			return Result.FALSE()
		else:
			return Result(val=rhs.val+lhs.val+len(lhs.word.literal), word=rhs.word)
