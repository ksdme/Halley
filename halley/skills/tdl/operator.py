# @author Kilari Teja

from halley.skills.tdl.utils import PropMap, Constants
import re

class OPERATOR(object):

	DESCRIPTOR = None

	@classmethod
	def register(clas, tokenStore):
		OPERATOR.registerStatic(clas, tokenStore)		

	@staticmethod
	def registerStatic(clas, tokenStore):
		if isinstance(clas.DESCRIPTOR, list):
			map(lambda d: d.setClass(clas), clas.DESCRIPTOR)
			tokenStore += clas.DESCRIPTOR
		else:
			clas.DESCRIPTOR.setClass(clas)
			tokenStore.append(clas.DESCRIPTOR)

	def __init__(self, action, selfToken, *args):
		assert len(args) > 0
		
		self._args  = args
		self._actn  = action
		self.label  = Constants.TOKEN_TYPES.COMPOUND_EXPR

	def bool(self, text):
		return self.eval(text).val >= 0

	def eval(self, text):
		return reduce(self._actn, map(lambda arg: arg.eval(text), self._args))

class Descriptor(PropMap):

	def __init__(self, regex, precedence, label):
		super(Descriptor, self).__init__(
			clas=None,
			regex=regex,
			label=label,
			precedence=precedence
		)

	def setClass(self, clas):
		self.clas = clas

class Result(PropMap):

	_FALSE = None

	def __init__(self, val, word):
		super(Result, self).__init__(val=val, word=word)

	@staticmethod
	def FALSE():
		if Result._FALSE is None:
			Result._FALSE = Result(-1, None)

		return Result._FALSE

def resolveParameterMagAndDirn(selector, reverseMagSym, paramText):

	mag, dirn = re.match(selector, paramText), False
	if mag is None:
		return (None, dirn)

	mag  = mag.groups()[0]
	dirn = not mag.startswith(reverseMagSym)
	mag  = int(mag[1:] if not dirn else mag)

	return (mag, dirn)