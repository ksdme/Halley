# @author Kilari Teja

from halley.skills.tdl.utils import PropMap, Constants
from halley.skills.tdl.operator import OPERATOR, Descriptor
from halley.skills.tdl.operator import resolveParameterMagAndDirn, Result

""" 
	arg[-1]: dirn: the direction of the passed param distance
				False -> max
				True  -> min

	Supports: => | [x]> | [!x]>
"""
class _OCCOURANCE_ORDER(OPERATOR):
	REVERSE_MAG_SYM = "!"

	def __init__(self, selfToken, *args):
		self._mag, self._dirn = resolveParameterMagAndDirn(
			self.__class__.PARAM_SELECTOR,
			_OCCOURANCE_ORDER.REVERSE_MAG_SYM, selfToken.token)

		super(_OCCOURANCE_ORDER, self).__init__(lambda a, b: None, selfToken, *args)

class PRE_OCCOURANCE(_OCCOURANCE_ORDER):

	PARAM_SELECTOR = r"\<\[([\!]?[0-9]+)\]"
	DESCRIPTOR = [
		Descriptor(PARAM_SELECTOR, Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR),
		Descriptor(r"\<\=",		  Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR)
	]

	def __init__(self, selfToken, lhs, rhs):
		super(PRE_OCCOURANCE, self).__init__(selfToken, lhs, rhs)

	def chopText(self, text, position):
		mag, dirn, chop  = self._mag, self._dirn, None
		mag = 0 if mag is None else mag
		if not dirn:
			chop = (0, position-mag)
		else:
			chop = (position-mag, position)

		return text[chop[0]:chop[1]]

	def eval(self, text):
		lhs, rhs = self._args[0].eval(text), self._args[1]
		if lhs.val == -1:
			return lhs

		rhs = rhs.eval(self.chopText(text, lhs.val))

		if rhs.val == -1:
			return rhs
		else:
			if (not self._dirn) or self._mag is None:
				return Result(val=rhs.val, word=rhs.word)
			else:
				return Result(val=rhs.val+(lhs.val-self._mag), word=rhs.word)

class POST_OCCOURANCE(_OCCOURANCE_ORDER):

	PARAM_SELECTOR = r"\[([\!]?[0-9]+)\]\>"
	DESCRIPTOR = [
		Descriptor(r"\[([\!]?[0-9]+)\]\>", Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR),
		Descriptor(r"\=\>",			     Constants.PRECEDENCE.LOW, Constants.TOKEN_TYPES.OPERATOR)
	]

	def __init__(self, selfToken, lhs, rhs):
		super(POST_OCCOURANCE, self).__init__(selfToken, rhs, lhs)

	def chopText(self, text, position, length):

		mag, dirn, chop  = self._mag, self._dirn, None
		mag = 0 if mag is None else mag
		wordTrailingChar = position + length
		if not dirn:
			chop = (wordTrailingChar + mag, None)
		else:
			chop = (wordTrailingChar, wordTrailingChar + mag)

		return text[chop[0]:chop[1]]

	def eval(self, text):
		lhs, rhs = self._args[0].eval(text), self._args[1]
		if lhs.val == -1:
			return lhs

		rhs = rhs.eval(self.chopText(text, lhs.val, len(lhs.word.literal)))
		if rhs.val == -1:
			return Result.FALSE()
		else:
			return Result(val=lhs.val+lhs.val+len(lhs.word.literal), word=rhs.word)
