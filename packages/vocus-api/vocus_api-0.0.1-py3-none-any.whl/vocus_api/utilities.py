
class Utilities():
    def camel_case_convert (camel_input):
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', camel_input.strip())
        word = '_'.join(map(str.lower, words))
        if word in ('class', 'def'):
            return word + "_"
        return word