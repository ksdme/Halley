# @author Kilari Teja

from halley.skills.tdl.utils import PropMap, Constants
from halley.skills.tdl.operator import OPERATOR, OpDescriptor
from halley.skills.tdl.operator import resolve3WayParameter, Result

class COUNT_OCCOURANCE(OPERATOR):
	PARAM_SELECTOR  = r"\:([\>\<]?[0-9]+)"
	DESCRIPTOR = OpDescriptor(PARAM_SELECTOR, Constants.PRECEDENCE.HIGH, Constants.TOKEN_TYPES.UNARY_OP)

	def __init__(self, selfToken, element):
		super(COUNT_OCCOURANCE, self).__init__(None, selfToken, None)
		self._element = element

		self._validator = resolve3WayParameter(
			COUNT_OCCOURANCE.PARAM_SELECTOR, selfToken.token)

	def eval(self, text):
		evald = self._element.eval(text)
		if evald.val == -1:
			return Result.FALSE()

		flag = self._validator(evald.word.count(text))
		return evald if flag else Result.FALSE()