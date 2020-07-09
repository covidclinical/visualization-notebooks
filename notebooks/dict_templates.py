import re
from functools import reduce
from jsonpath_rw import parse as jsonpath_parse

# Python port of json-templates
# Reference: https://github.com/datavis-tech/json-templates

# Constructs a template function.
class Template:
    def __init__(self, fn, parameters):
        self.fn = fn
        self.parameters = parameters


# Constructs a parameter object from a match result.
# e.g. "['{{foo}}']" --> { key: "foo" }
# e.g. "['{{foo:bar}}']" --> { key: "foo", defaultValue: "bar" }
class Parameter:
    def __init__(self, match):
        match_value = match[2:len(match)-2].strip()
        key = match_value
        default_value = None
        
        if ":" in match_value:
            i = match_value.index(":")
            key = match_value[:i]
            default_value = match_value[i+1:]
        
        self.key = key
        self.default_value = default_value


# This regular expression detects instances of the
# template parameter syntax such as {{foo}} or {{foo:someDefault}}.
str_regex = r"({{(\w|:|[\s\-+.,@/\//()?=*_])+}})"

# Parses leaf nodes of the template object that are strings.
# Also used for parsing keys that contain templates.
def parse_str(value):
    print("parse_str")
    parameters = []
    template_fn = (lambda context: value)

    if re.search(str_regex, value):
        matches = [ g[0] for g in re.findall(str_regex, value) ]
        parameters = [ Parameter(match) for match in matches ]

        def template_fn(context):

            def accumulator(a, h):
                i = h[0]
                match = h[1]
                parameter = parameters[i]
                parameter_key_expr = jsonpath_parse(parameter.key)
                try:
                    fill_value = parameter_key_expr.find(context)[0].value
                except:
                    fill_value = parameter.default_value

                if type(fill_value) == dict:
                    return fill_value

                if fill_value == None:
                    return None

                if len(match) == len(value):
                    return fill_value
                return value.replace(match, fill_value)
            return reduce(accumulator, enumerate(matches), value)
    return Template(template_fn, parameters)


def parse_dict(value):
    print("parse_dict")
    children = [
        {
            "key_template": parse_str(k),
            "value_template": parse(v)
            
        }
        for k, v in value.items()
    ]
    def accumulator(a, h):
        # Concatenate all of the .parameters arrays together
        return a + h["value_template"].parameters + h["key_template"].parameters

    template_parameters = reduce(accumulator, children, [])

    def template_fn(context):
        def accumulator(a, h):
            a[h["key_template"].fn(context)] = h["value_template"].fn(context)
            return a
        return reduce(accumulator, children, {})

    return Template(template_fn, template_parameters)


def parse_list(value):
    print("parse_list")
    templates = list(map(parse, value))

    def accumulator(a, h):
        return a + h.parameters

    template_parameters = reduce(accumulator, templates, [])

    def template_fn(context):
        return list(map((lambda template: template(context)), templates))

    return Template(template_fn, template_parameters)


def parse(value):
    print("parse")
    if type(value) == str:
        return parse_str(value)
    elif type(value) == dict:
        return parse_dict(value)
    elif type(value) == list:
        return parse_list(value)
    else:
        return Template((lambda context: value), [])

