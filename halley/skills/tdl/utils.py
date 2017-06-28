# @author Kilari Teja
import re

class PropMap(object):

	def __init__(self, **kargs):
		self._kargs = kargs
		for key in kargs:
			setattr(self, key, kargs[key])

	def __str__(self):
		return str(self._kargs)

class Constants:

	TOKEN_TYPES = PropMap(
		COMPOUND_EXPR 	=	"COMPOUND_EXPR",
		PARTH_OPEN	=	"PARTH_OPEN",
		PARTH_CLSE 	=	"PARTH_CLSE",
		OPERATOR 		=	"OPERATOR",
		UNARY_OP		=	"UNARY_OP",
		WORD 		=	"WORD"
	)

	PRECEDENCE = PropMap(
		HIGH		= 3,
		MEDIUM	= 2,
		LOW		= 1
	)

	PARTH_OPEN_SYM, PARTH_CLSE_SYM   	= "(", ")" 
	AND_SYM, OR_SYM, NOT_SYM     	 	= "&", "|", "!" 
	PRE_OCCOURANCE_NON_PARAM_SYM		= "<=" 
	POST_OCCOURANCE_NON_PARAM_SYM		= "=>"
	DELIMITED_WORD_STARTS_WITH 		= "?"

class Token(PropMap):

	def __init__(self, token, tokenRule):
		super(Token, self).__init__(
			clas=tokenRule.clas,
			token=token,
			label=tokenRule.label,
			precedence=tokenRule.precedence
		)

def 