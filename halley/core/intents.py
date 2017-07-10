# @author Kilari Teja
import time
from exception import *
from subscriber import *

class Intent(object):

	@staticmethod
	def vaidateIntentAction(action):
		return isinstance(action, str) and len(action) > 0

	def __init__(self, action, timestamp=None):
		assert Intent.vaidateIntentAction(action), Messages.IntentActionValidation

		self._action = action
		self._timestamp = time.time() if timestamp is None else timestamp

	action = property(lambda self: self._action)
	timestamp = property(lambda self: self._timestamp)

class Intents:
	
	SYSTEM_FREE_INTENT = Intent("system.free")

# IntentManager needs to be on the main thread
# Or the Subscriber's flag should be set appropriately
class IntentManager(object):
	HISTORY_CACHE_SIZE = 30	

	def __init__(self, context):
		self._context = context
		self.reInit()

	def reInit(self):
		self._intentsStore = {}
		self._history = []

	def resolveIntentTargets(self, action):
		try:
			return self.intentStore[action]
		except:
			return []

	def resolveIntent(self, action, *args, **kargs):
		if not isinstance(action, str):
			action = action.action

		for subscriber in self.resolveIntentTargets(action):
			subscriber.do(self.context, action, *args, **kargs)

		self.addToHistory(action)

	def addToHistory(self, intent):
		self._history.append((intent, time.time()))
		self._history = self._history[-IntentManager.HISTORY_CACHE_SIZE:]

	# Intent func: func(intent, *args)
	def addIntent(self, action, subscriber):
		try:
			self.intentStore[action]
		except:
			self.intentStore[action] = []

		self.intentStore[action].append(subscriber)

	def emit(self, action, *args, **kargs):
		if isinstance(action, str) or isinstance(action, Intent):
			self.resolveIntent(action, *args, **kargs)
			return True

		else:
			raise EmitTypeIssue()

	def subscribe(self, action, args=[]):
		if not isinstance(action, str):
			action = action.action

		def _(func):
			l = Subscriber(Subscriber.SUBSCRIBER_TIMEOUT,
					func, args, Subscriber.THREAD_SAFE_FLAG)

			self.addIntent(action, l)
			l.onRegister(self.context)

			return func

		return _

	intentStore = property(lambda self: self._intentsStore)
	history = property(lambda self: self._history)
	context = property(lambda self: self._context)
