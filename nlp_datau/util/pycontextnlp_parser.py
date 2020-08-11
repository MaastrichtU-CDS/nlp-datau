class ContextParser:

    @staticmethod
    def filter_concept(pycontextnlp_result, filter_target):
        if not pycontextnlp_result:
            return ""
        targets = []
        for result in pycontextnlp_result:
            if filter_target in result['target']['category']:
                targets.append(result)
        return targets

    @staticmethod
    def is_present(filtered_target, modifiers_not_present):
        for result in filtered_target:
            for modifier in result['modifiers']:
                for category in modifier['category']:
                    if category in modifiers_not_present:
                        return False
        return True
