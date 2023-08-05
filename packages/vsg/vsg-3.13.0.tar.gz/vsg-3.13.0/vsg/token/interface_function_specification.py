
from vsg import parser


class pure_keyword(parser.keyword):
    '''
    unique_id = interface_function_specification : pure_keyword
    '''

    def __init__(self, sString):
        parser.keyword.__init__(self, sString)


class impure_keyword(parser.keyword):
    '''
    unique_id = interface_function_specification : impure_keyword
    '''

    def __init__(self, sString):
        parser.keyword.__init__(self, sString)


class function_keyword(parser.keyword):
    '''
    unique_id = interface_function_specification : function_keyword
    '''

    def __init__(self, sString):
        parser.keyword.__init__(self, sString)


class parameter_keyword(parser.identifier):
    '''
    unique_id = interface_function_specification : parameter_keyword
    '''

    def __init__(self, sString):
        parser.identifier.__init__(self, sString)


class designator(parser.designator):
    '''
    unique_id = interface_function_specification : designator
    '''

    def __init__(self, sString):
        parser.designator.__init__(self, sString)


class open_parenthesis(parser.open_parenthesis):
    '''
    unique_id = interface_function_specification : open_parenthesis
    '''

    def __init__(self, sString='('):
        parser.open_parenthesis.__init__(self)


class close_parenthesis(parser.close_parenthesis):
    '''
    unique_id = interface_function_specification : close_parenthesis
    '''

    def __init__(self, sString=')'):
        parser.close_parenthesis.__init__(self)


class return_keyword(parser.identifier):
    '''
    unique_id = interface_function_specification : return_keyword
    '''

    def __init__(self, sString):
        parser.identifier.__init__(self, sString)
