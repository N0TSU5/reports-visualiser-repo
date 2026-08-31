
class RuleEngine:
    _rules = {
        'default_criteria': lambda ctx: ctx['flag'] or ctx['dpd'] >= ctx['threshold']
    }
    @staticmethod
    def evaluate(rule_name, context):
        return RuleEngine._rules[rule_name](context)
