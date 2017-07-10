# @author Kilari Teja
from timeout_decorator import timeout, TimeoutError

class Flag:

	def __init__(self, value):
		self.value = value

# Keep track of threadSafe,
# It needs to be thread safe
class Subscriber(object):
	THREAD_SAFE_FLAG = False
	SUBSCRIBER_TIMEOUT = 3

	FLAG_TIMED_OUT = Flag(-1)

	def __init__(self, tout, func, args, threadSafe):
		assert isinstance(threadSafe, bool)

		self._func = timeout(tout, use_signals=threadSafe)(func)
		self._args = args

	@timeout(SUBSCRIBER_TIMEOUT)
	def onRegister(self, context):
		pass

	def do(self, context, intent, *args, **kargs):
		if self._args != []:
			kargs["_args"] = self._args

		try:
			return self._func(context, intent, *args, **kargs)
		except TimeoutError:
			self.onTimeout(self, context)
			return Subscriber.FLAG_TIMED_OUT

	@timeout(SUBSCRIBER_TIMEOUT)
	def onTimeout(self, context):
		pass
