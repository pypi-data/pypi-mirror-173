class Formatter:

    def __init__(self, init_param_name=None, base_class=None):
        self.init_param_name = init_param_name or 'json_data'
        self.base_class = base_class or 'general response'

    @staticmethod
    def class_format(string):

        if ' ' in string or '_' in string:
            return string.title().replace(' ', '').replace('_', '')
        else:
            return string[0].upper() + string[1:]

    def CLASS_STATEMENT(self, class_name, parent_name=None):

        parent_name = parent_name or self.base_class

        return 'class {}({}):\n\n'.format(self.class_format(class_name), self.class_format(parent_name))

    def INIT_STATMENT(self):

        return '\tdef __init__(self, {}):\n\n'.format(self.init_param_name)

    @staticmethod
    def ATTRIBUTE_STATEMENT(name, var_type):

        return '\t\tself.{0} = {1}\n\t\t""":type : {1}"""\n'.format(name, var_type)

    @staticmethod
    def ATTRIBUTE_LIST_STATEMENT(name, var_type):

        return '\t\tself.{0} = [{1}]\n\t\t""":type : list[{1}]"""\n'.format(name, var_type)

    def SUPER_STATEMENT(self):

        return '\t\tsuper().__init__({})\n\n\n'.format(self.init_param_name)

    def BASE_CLASS(self):

        return '''class {1}(object):

    def __init__(self, {0}):
        for name, attr_type in self.__dict__.items():
            if attr_type is None:
                pass
            elif isinstance(attr_type, list):
                if issubclass(attr_type[0], GeneralResponse):
                    {0}[name] = [attr_type[0](x) for x in {0}[name]]
            elif issubclass(attr_type, GeneralResponse):
                {0}[name] = attr_type({0}[name])
        if {0}:
            self.__dict__.update({0})\n\n\n'''.format(self.init_param_name, self.class_format(self.base_class))


class JsonToPython:

    def __init__(self, formatter=None):

        self.formatter = formatter or Formatter()

    @classmethod
    def compare_dict_keys(cls, dict1, dict2):
        result = True
        for key in dict1:
            result = result and (key in dict2.keys())
        return result and len(dict1) == len(dict2)

    @classmethod
    def is_in_subclasses(cls, dict1, subclasses):
        if subclasses:
            for entry in subclasses:
                for key in entry:
                    if cls.compare_dict_keys(dict1, entry[key]):
                        return key

    def convert(self, class_name, json_data, parent_name=None):

        def handle_dict(key, value, is_list=False):
            nonlocal result
            formate = self.formatter.ATTRIBUTE_LIST_STATEMENT if is_list else self.formatter.ATTRIBUTE_STATEMENT
            if not value:
                result += formate(key, 'None')
            elif not self.is_in_subclasses(value, subclasses):
                new_class_name = key + ' ' + class_name
                subclasses.append({new_class_name: value})
                result += formate(key, self.formatter.class_format(new_class_name))
            else:
                new_class_name = self.is_in_subclasses(value, subclasses)
                result += formate(key, self.formatter.class_format(new_class_name))

        parent_name = parent_name or self.formatter.base_class
        result = ''
        subclasses = []
        result += self.formatter.CLASS_STATEMENT(class_name, parent_name)
        result += self.formatter.INIT_STATMENT()
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                if value is None:
                    result += self.formatter.ATTRIBUTE_STATEMENT(key, 'None')
                elif isinstance(value, dict):
                    handle_dict(key, value)
                elif isinstance(value, list):
                    if not value:
                        result += self.formatter.ATTRIBUTE_STATEMENT(key, value.__class__.__name__)
                    elif isinstance(value[0], dict):
                        handle_dict(key, value[0], True)
                    else:
                        result += self.formatter.ATTRIBUTE_LIST_STATEMENT(key, value[0].__class__.__name__)

                else:
                    result += self.formatter.ATTRIBUTE_STATEMENT(key, value.__class__.__name__)
        elif isinstance(json_data, list):
            self.convert(class_name, json_data[0], parent_name)
        else:
            raise ValueError('the function only works with parsed json data')

        result += self.formatter.SUPER_STATEMENT()

        result = result.replace('\t', '    ')

        if subclasses:
            for entry in subclasses:
                for key in entry:
                    result += self.convert(class_name=key, parent_name=parent_name, json_data=entry[key])

        return result

    @staticmethod
    def write_file(string, file_name='response_objects', file_path=''):
        with open(file_path + file_name + '.py', 'a') as f:
            f.write(string)
