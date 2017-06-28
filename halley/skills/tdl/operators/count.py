# @author Kilari Teja

from halley.skills.tdl.utils import PropMap, Constants
from halley.skills.tdl.operator import OPERATOR, Descriptor
from halley.skills.tdl.operator import resolveParameterMagAndDirn, Result

class COUNT_OCCOURANCE(OPERATOR):
	PARAM_SELECTOR  = r"\:([\!]?[0-9]+)"
	REVERSE_MAG_SYM = "!"
	DESCRIPTOR = Descriptor(PARAM_SELECTOR, Constants.PRECEDENCE.HIGH, Constants.TOKEN_TYPES.UNARY_OP)

	def __init__(self, selfToken, element):
		super(COUNT_OCCOURANCE, self).__init__(None, selfToken, None)
		self._element = element

		self._mag, self._dirn = resolveParameterMagAndDirn(
			COUNT_OCCOURANCE.PARAM_SELECTOR,
			COUNT_OCCOURANCE.REVERSE_MAG_SYM, selfToken.token)

	def eval(self, text):
		evald = self._element.eval(text)
		if evald.val == -1:
			return Result.FALSE()

		cunt = evald.word.count(text)
		flag = (self._dirn and cunt >= self._mag)
		flag = flag or ((not self._dirn) and cunt <= self._mag)

		return evald if flag else Result.FALSE()