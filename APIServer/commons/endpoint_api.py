

def get_endpoints(api, app):
    """
    Gets api endpoints, given an api and associated app
    """

    invalid_rules = [
        "/",
        "/swagger.json",
        "/swaggerui/<path:filename>",
        "/static/<path:filename>"
    ]

    def get_rule_method(app, rule):
        """
        Function used to look up the methods for endpoints
        and their related docstrings.
        """
        # Accessing class that defines endpoint
        rule_class = app.view_functions[rule.endpoint].view_class
        # Accessing the methods available to that class/endpoint
        methods = list(app.view_functions[rule.endpoint].methods)
        method_dict = {}

        # Based on available methods, pulls the docstring from the class
        for m in methods:
            if m == 'GET':
                method_dict[m] = rule_class.get.__doc__.strip()
            elif m == 'PUT':
                method_dict[m] = rule_class.put.__doc__.strip()
            elif m == 'POST':
                method_dict[m] = rule_class.post.__doc__.strip()
            elif m == 'DELETE':
                method_dict[m] = rule_class.delete.__doc__.strip()
            else:
                method_dict[m] = 'NO DOC'

        return method_dict

    rules = [rule for rule in api.app.url_map.iter_rules()]
    rules = list(filter(lambda x: x.rule not in invalid_rules, rules))

    endpoints = {rule.rule: get_rule_method(app, rule) for rule in rules}

    return {"Available endpoints": endpoints}
