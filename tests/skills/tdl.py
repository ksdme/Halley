import unittest
from halley.skills.tdl.compiler import ruleCompiler

class TDLTestCase(unittest.TestCase):

	TEST_INPUT_0_0 = ("ab",			"ab ba",		True)
	TEST_INPUT_0_1 = ("?a",			"ab",		False)
	TEST_INPUT_0_2 = ("?a",			"a bb",		True)
	TEST_INPUT_0_3 = ("'hey man'",	"hey man",	True)	
	
	TEST_INPUT_1_0 = ("a & b",		"ab",	 	True)
	TEST_INPUT_1_4 = ("a, b",		"ab",	 	True)
	TEST_INPUT_1_1 = ("a | b", 		"a", 		True)
	TEST_INPUT_1_2 = ("!a", 			"a", 		False)
	TEST_INPUT_1_3 = ("!a", 			"b", 		True)
	
	TEST_INPUT_2_0 = ("a => b",		"abb",		True)
	TEST_INPUT_2_1 = ("a => b",		"bab",		True)
	TEST_INPUT_2_2 = ("a => b => c",	"abc",		True)
	TEST_INPUT_2_3 = ("a => b => c",	"acb",		False)
	TEST_INPUT_2_4 = ("a [!2]> b",	"a  b",		True)
	TEST_INPUT_2_5 = ("a [2]> b",		"a  b",		False)
	TEST_INPUT_2_6 = ("a => b [2]> c",	"a b a b c",	True)

	TEST_INPUT_4_0 = ("a & (b | c)", 	"ac", 		True)
	TEST_INPUT_4_1 = ("(a | b) | c", 	"abc", 		True)
	TEST_INPUT_4_2 = ("(a | b) & !b", 	"b", 		False)

	def ruleTest(self, testInput):

		rule = ruleCompiler(testInput[0])
		self.assertEqual(rule.bool(testInput[1]), testInput[2])

	def runAlongInputs(self, case):
		case, lndex = "TEST_INPUT_{0}_{1}".format(case, "{}"), 0

		while True:
			try:
				self.ruleTest(getattr(self, case.format(lndex)))
				lndex += 1
			except AttributeError:
				break

	def test_simple_words(self):
		self.runAlongInputs(0)

	def test_simple_boolean(self):
		self.runAlongInputs(1)

	def test_simple_ordering_operators(self):
		self.runAlongInputs(2)

	def test_simple_compound_expressions(self):
		self.runAlongInputs(4)
