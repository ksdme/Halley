from halley.core.intents import IntentManager, Intents, Intent
import unittest

class IntentManagerTests(unittest.TestCase):

	def test_simple_binding(self):
		manager = IntentManager(None)

		@manager.subscribe(Intents.SYSTEM_FREE_INTENT)
		def onSystemFree(context, action, *args, **kargs):
			self.assertTrue(True)

		@manager.subscribe(Intents.SYSTEM_FREE_INTENT, (1, 2, 3))
		def freeIntentTwo(context, action, _args):
			self.assertTrue(True)

		manager.emit(Intents.SYSTEM_FREE_INTENT)
