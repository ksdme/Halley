# Halley's Skill API
# @author Kilari Teja

class Messages:
	BAD_RULE 				= "Bad Rule"
	MISSING_PARTH_CLSE 		= "Missing ')'"
	BAD_COMPOUND_EXPR		= "Bad Compound Expression"
	COMPILATION_ERROR		= "Compilation Issue"
	UNIDENTIFIED_SYM		= "Unidentified Symbol"
	SYNTAX_ERROR			= "Syntax Issue"
	PREPROCESSING_ERROR 	= "Preprocessor Issue"
	PREPROCESSING_KEY_ERROR	= "Spread Map Key Error"

class RuleLanguage(Exception):
	def __init__(self, msg):
		super(RuleLanguage, self).__init__(msg)

class RuleCompilation(Exception):
	def __init__(self, msg):
		super(RuleCompilation, self).__init__(msg)

class RulePreprocessor(Exception):
	def __init__(self, msg):
		super(RulePreprocessor, self).__init__(msg)