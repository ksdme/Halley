from halley.skills.tdl.utils import Pipeline, PropMap

class Preprocessor(object):
	CONSUMES_RAW 			= 3
	CONSUMES_TOKEN_STREAM 	= 4

	DESCRIPTOR = None

	@classmethod
	def register(clas, pipeline, argslambda):
		pipeline.add(clas, clas.DESCRIPTOR.consumesType, argslambda)

	@staticmethod
	def registerStatic(clas, pipeline, argslambda):
		clas.register(clas, pipeline, argslambda)

	@staticmethod
	def act(data):
		raise NotImplementedError()

class PrepDescriptor(PropMap):

	def __init__(self, consumesType):
		super(PrepDescriptor, self).__init__(
			consumesType=consumesType)

class PreprocessorPipeline:

	def __init__(self, tokeniser):
		self._when_raw_code = Pipeline()
		self._post_tokenise = Pipeline()

		self._post_tokenise.addAction(tokeniser)

	def __call__(self, data):
		return self.do(data)

	def do(self, data):
		return self._post_tokenise.do(self._when_raw_code.do(data))

	def add(self, clas, consumesType, argslambda):
		lamda = (lambda data, args: clas.act(data, args), argslambda)
		
		if consumesType == Preprocessor.CONSUMES_RAW:
			self._when_raw_code.addAction(lamda)
		elif consumesType == Preprocessor.CONSUMES_TOKEN_STREAM:
			self._post_tokenise.addAction(lamda)
