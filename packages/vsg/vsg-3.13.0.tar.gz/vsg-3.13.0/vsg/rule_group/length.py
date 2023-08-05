
from vsg import rule
from vsg import severity


class Rule(rule.Rule):
    '''
    Class for assigning rules to the length group.

    Parameters
    ----------

    name : string
       The group the rule belongs to.

    identifier : string
       unique identifier.  Usually in the form of 00N.
    '''

    def __init__(self, name, identifier):
        rule.Rule.__init__(self, name=name, identifier=identifier)
        self.phase = 7
        self.fixable = False
        self.groups.append('length')
        self.severity = severity.warning('Warning')
        self.configuration.append('length')
