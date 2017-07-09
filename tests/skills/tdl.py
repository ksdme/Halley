import unittest
from halley.skills.tdl.compiler import ruleCompiler

class TDLTestCase(unittest.TestCase):

	TEST_INPUT_0_0 = ("ab",			"ab ba",	True)
	TEST_INPUT_0_1 = ("?a",			"ab",	True)
	TEST_INPUT_0_2 = ("?a",			"a bb",	True)
	TEST_INPUT_0_3 = ("'hey man'",	"hey man",True)	
	
	TEST_INPUT_1_0 = ("a & b",		"a b",	True) 
	TEST_INPUT_1_4 = ("a, b",		"a b",	True)
	TEST_INPUT_1_1 = ("a | b", 		"a", 	True)
	TEST_INPUT_1_2 = ("!a", 			"a", 	False)
	TEST_INPUT_1_3 = ("!a", 			"b", 	True)
	
	TEST_INPUT_2_0 = ("a => b",		"a b", 	True)
	TEST_INPUT_2_1 = ("a <= b",		"a b", 	True)
	TEST_INPUT_2_2 = ("a => b => c",	"a b c", 	True)
	TEST_INPUT_2_3 = ("a <= b <= c",	"a b c", 	True)
	TEST_INPUT_2_4 = ("a => (l|m)",	"a l", 	True)
	TEST_INPUT_2_5 = ("(l|m) => a",	"l a", 	True)
	TEST_INPUT_2_6 = ("a => b => ?c",	"a bc", 	True)
	TEST_INPUT_2_7 = ("a => b => ?c",	"a b c", 	False)
	TEST_INPUT_2_8 = ("a <= b => a",	"a b", 	False)
	TEST_INPUT_2_9 = ("a <= b => a",	"a b a", 	True)
	TEST_INPUT_2_10 = ("a => b:2",	"b a b", 	False)
	TEST_INPUT_2_11 = ("a => b:2",	"a b b", 	False)

	TEST_INPUT_4_0 = ("a & (b | c)", 	"a c", 	True)
	TEST_INPUT_4_1 = ("(a | b) | c", 	"a b c", 	True)
	TEST_INPUT_4_2 = ("(a | b) & !b", 	"b", 	False)

	TEST_INPUT_5_0 = ("a:1",			"a",		True)
	TEST_INPUT_5_1 = ("a:2",			"a a",	True)
	TEST_INPUT_5_2 = ("?a:1",		"a",		True)
	TEST_INPUT_5_3 = ("?a:2",		"aa",	True)
	TEST_INPUT_5_4 = ("?a:1",		"a",		True)
	TEST_INPUT_5_5 = ("?a:>2",		"aaa",	True)
	TEST_INPUT_5_6 = ("?a:<2",		"a",		True)
	TEST_INPUT_5_7 = ("(a|b|c):2",	"b b",	True)
	TEST_INPUT_5_8 = ("(a|b|c):2",	"k k",	False)
	TEST_INPUT_5_9 = ("(?a|?b|?c):2",	"aa",	True)
	TEST_INPUT_5_10 = ("(a|b|c):2",	"",		False)
	TEST_INPUT_5_11 = ("(a|!b|?c):2",	"b",		False)
	TEST_INPUT_5_12 = ("(a|!b|c):2",	"b a a",	True)

	# Spread Preprocessor
	TEST_INPUT_6_0 = ("[&TEST]",	"abc",	True, { "spreadMap": { "TEST": ["a", "b", "c"] } })

	def ruleTest(self, testInput, hasPreprocessorArgs=False, message=""):

		rule = ruleCompiler(testInput[0], **(testInput[3] if hasPreprocessorArgs else {}))
		self.assertEqual(rule.bool(testInput[1]), testInput[2], message)

	def runAlongInputs(self, case, hasPreprocessorArgs=False):
		case, lndex = "TEST_INPUT_{0}_{1}".format(case, "{}"), 0

		while True:
			try:
				currentCase = case.format(lndex)
				self.ruleTest(getattr(self, currentCase), hasPreprocessorArgs, "[-] Failed {}".format(currentCase))
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

	# def test_preprocessor_spread(self):
	# 	self.runAlongInputs(6)
