
from vsg import parser


class label(parser.label):
    '''
    unique_id = wait_statement : label
    '''

    def __init__(self, sString):
        parser.label.__init__(self, sString)


class label_colon(parser.label_colon):
    '''
    unique_id = wait_statement : label_colon
    '''

    def __init__(self):
        parser.label_colon.__init__(self)


class wait_keyword(parser.keyword):
    '''
    unique_id = wait_statement : wait_keyword
    '''

    def __init__(self, sString):
        parser.keyword.__init__(self, sString)


class semicolon(parser.semicolon):
    '''
    unique_id = wait_statement : semicolon
    '''

    def __init__(self, sString=';'):
        parser.semicolon.__init__(self)
