# @author Kilari Teja
from timeout_decorator import timeout

# Keep track of threadSafe,
# It needs to be thread safe
class Subscriber(object):
	THREAD_SAFE_FLAG = False
	SUBSCRIBER_TIMEOUT = 10

	def __init__(self, tout, func, args, threadSafe):
		assert isinstance(threadSafe, bool)

		self._func = timeout(tout, use_signals=threadSafe)(func)
		self._args = args

	@timeout(SUBSCRIBER_TIMEOUT)
	def onRegister(self, context):
		return None

	def do(self, context, intent, *args, **kargs):
		if self._args != []:
			kargs["_args"] = self._args

		self._func(context, intent, *args, **kargs)
