import rules_registry_hop1
class RuleEngine:
    _rules = {
        'default_criteria': lambda ctx: rules_registry_hop1.execute(ctx)
    }
    @staticmethod
    def evaluate(rule_name, context):
        return RuleEngine._rules[rule_name](context)
