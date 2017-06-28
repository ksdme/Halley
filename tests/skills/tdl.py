import unittest
from halley.skills.tdl.compiler import ruleCompiler

class TDLTestCase(unittest.TestCase):

	TEST_INPUT_0_0 = ("ab",			"ab ba",	True)
	TEST_INPUT_0_1 = ("?a",			"ab",	False)
	TEST_INPUT_0_2 = ("?a",			"a bb",	True)
	TEST_INPUT_0_3 = ("'hey man'",	"hey man",True)	
	
	TEST_INPUT_1_0 = ("a & b",		"ab",	True)
	TEST_INPUT_1_4 = ("a, b",		"ab",	True)
	TEST_INPUT_1_1 = ("a | b", 		"a", 	True)
	TEST_INPUT_1_2 = ("!a", 			"a", 	False)
	TEST_INPUT_1_3 = ("!a", 			"b", 	True)
	
	TEST_INPUT_2_0 = ("a => b",		"ab", 	True)
	TEST_INPUT_2_1 = ("a <= b",		"ab", 	True)
	TEST_INPUT_2_2 = ("a => b => c",	"abc", 	True)
	TEST_INPUT_2_3 = ("a <= b <= c",	"abc", 	True)
	TEST_INPUT_2_4 = ("a => (l|m)",	"al", 	True)
	TEST_INPUT_2_5 = ("(l|m) => a",	"la", 	True)
	TEST_INPUT_2_6 = ("a => b => ?c",	"ab c", 	True)
	TEST_INPUT_2_7 = ("a => b => ?c",	"abc", 	False)
	TEST_INPUT_2_8 = ("a <= b => a",	"ab", 	False)
	TEST_INPUT_2_9 = ("a <= b => a",	"aba", 	True)
	TEST_INPUT_2_10 = ("a => b:2",		"bab", 	False)
	TEST_INPUT_2_11 = ("a => b:2",		"abb", 	False)

	TEST_INPUT_4_0 = ("a & (b | c)", 	"ac", 	True)
	TEST_INPUT_4_1 = ("(a | b) | c", 	"abc", 	True)
	TEST_INPUT_4_2 = ("(a | b) & !b", 	"b", 	False)

	TEST_INPUT_5_0 = ("a:1",			"a",		True)
	TEST_INPUT_5_1 = ("a:2",			"a a",	True)
	TEST_INPUT_5_2 = ("?a:1",		"a",		True)
	TEST_INPUT_5_3 = ("?a:2",		"a a",	True)
	TEST_INPUT_5_4 = ("?a:1",		"a",		True)
	TEST_INPUT_5_5 = ("?a:>2",		"a a a",	True)
	TEST_INPUT_5_6 = ("?a:<2",		"a",		True)
	TEST_INPUT_5_7 = ("(a|b|c):2",	"bb",	True)
	TEST_INPUT_5_8 = ("(a|b|c):2",	"kk",	False)
	TEST_INPUT_5_9 = ("(?a|?b|?c):2",	"a a",	True)
	TEST_INPUT_5_10 = ("(a|b|c):2",	"",		False)
	TEST_INPUT_5_11 = ("(a|!b|?c):2",	"b",		False)
	TEST_INPUT_5_12 = ("(a|!b|c):2",	"baa",	True)

	def ruleTest(self, testInput, message=""):

		rule = ruleCompiler(testInput[0])
		self.assertEqual(rule.bool(testInput[1]), testInput[2], message)

	def runAlongInputs(self, case):
		case, lndex = "TEST_INPUT_{0}_{1}".format(case, "{}"), 0

		while True:
			try:
				currentCase = case.format(lndex)
				self.ruleTest(getattr(self, currentCase), "[-] Failed {}".format(currentCase))
				lndex += 1
			except AttributeError:
				break
		else:
			return lndex

	def test_simple_words(self):
		self.runAlongInputs(0)

	def test_simple_boolean(self):
		self.runAlongInputs(1)

	def test_simple_ordering_operators(self):
		self.runAlongInputs(2)

	def test_simple_compound_expressions(self):
		self.runAlongInputs(4)

	def test_simple_count_unary_operator(self):
		self.runAlongInputs(5)
