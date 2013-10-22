"""
In this file we create the objects for the rules
"""

import types


class Statement:
    """Holds one premise, goal condition or calculated condition"""
    def __init__(self, lopperand, relation, ropperand):
        self.lopperand = lopperand
        self.relation = relation
        self.ropperand = ropperand

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "{}{}{}".format(self.lopperand, self.relation, self.ropperand)

    def __repr__(self):
        return self.__unicode__()

    def __contains__(self, value):
        return value in (self.lopperand, self.ropperand)

    def __eq__(self, other):
        return self.lopperand == other.lopperand and self.relation == other.relation and self.ropperand == other.ropperand

    def invert(self):
        '''Invert the given statement.'''
        return Statement(self.ropperand, self.relation, self.lopperand)


class Rule:
    """Generic rule template for a rule that can be applied on statements"""
    def __init__(self, name, validation, result):
        self.name = name
        self.validation = types.MethodType(validation, self)
        self.result_int = types.MethodType(result, self)

    def __str__(self):
        return "{}".format(self.name)

    def result(self, *args):
        '''Validate that the rule is applicable and return the resulting statement'''
        if self.validation(*args):
            return self.result_int(*args)


class Relation:
    """Representation of a relation with its counterpart.
    Not really exploited but used in several occasions"""
    def __init__(self, rel, negrel):
        self.rel = rel
        self.negrel = negrel

    def __eq__(self, other):
        return (self.rel == other) or (self.rel == other.rel)

    def __neq__(self, other):
        return not (self == other)

    def __contains__(self, value):
        return value in [self.rel, self.negrel]

    def __str__(self):
        return "<Relation {}>".format(self.rel)

"""The relations"""

rellr = Relation("l", "r")
relfb = Relation("f", "b")

relations = (rellr, relfb)

"""The rules used"""
"""All rules must be appended to this list else they will be ignored"""

rules = []

"""Transitivity"""


def t_valid(self, *args):
    s0 = args[0]
    s1 = args[1]
    return (s0.relation == s1.relation and s0.ropperand == s1.lopperand)


def t_result(self, *args):
    s0 = args[0]
    s1 = args[1]
    return Statement(s0.lopperand, s0.relation, s1.ropperand)

transitivity = Rule('Transitivity', t_valid, t_result)


def test_transitivity():
    """ Test if transitive statements are actually correctly transformed """
    s0 = Statement('a', Relation('l', 'r'), 'b')
    s1 = Statement('b', 'l', 'c')
    print(transitivity.result(s0, s1))

rules.append(transitivity)
""" Front Transitivities """


def tf_validl(self, s0, s1):
    return (s0.relation == "l") and (s1.relation == "f") and (s0.lopperand == s1.ropperand)


def tf_validr(self, s0, s1):
    return (s0.relation == "l") and (s1.relation == "f") and (s0.ropperand == s1.ropperand)


def tf_resultl(self, s0, s1):
    return Statement(s1.lopperand, s0.relation, s0.ropperand)


def tf_resultr(self, s0, s1):
    return Statement(s0.ropperand, s0.relation, s1.lopperand)


fronttransitivityl = Rule('Fronttransitivityl', tf_validl, tf_resultl)
fronttransitivityr = Rule('Fronttransitivityr', tf_validr, tf_resultr)
rules.append(fronttransitivityl)
rules.append(fronttransitivityr)


def test_fronttransitivity():
    s0 = Statement('a', Relation('l', 'r'), 'b')
    s1 = Statement('c', 'f', 'b')
    print(fronttransitivityl.result(s0, s1))
    print(fronttransitivityr.result(s0, s1))

""" If they are independent """


def ind_valid(self, s0, s1):
    return (s0.lopperand != s1.lopperand) and (s0.ropperand != s1.lopperand) and (s0.ropperand != s1.ropperand) and (s0.lopperand != s1.ropperand)


def ind_resultl(self, s0, s1):
    return Statement(s0.ropperand, 'l', s1.lopperand)


def ind_resultr(self, s0, s1):
    return Statement(s1.ropperand, 'l', s0.lopperand)

independentl = Rule('Independentl', ind_valid, ind_resultl)
independentr = Rule('Independentr', ind_valid, ind_resultr)

rules.append(independentl)
#rules.append(independentr)

""" Turn around r relations """


def turn_valid(self, s0, s1):
    return (s0.relation == 'r')


def turn_result(self, s0, s1):
    return Statement(s0.ropperand, 'l', s0.lopperand)

turn = Rule('Turn', turn_valid, turn_result)

#rules.append(turn)
