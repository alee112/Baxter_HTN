

class InputParser:
    def __init__(self):
        pass

    def parse(self, string):
        """
        Commands:                                   Example command:
            -create_block                               "a is a block."
            -create_type                                "blue is a type.
            -instance_type_query                        "is a blue?"
            -type_type_query                            "are all blocks that are magenta red?"
            -set_instance_type                          "a is blue."
            -set_type_implication                       "all blocks that are magenta are red."
            -set_on_set                                 "on(a,B), on(B,fasd)."
            -display_data                               "display data."
            -what_is_on                                 "what is a on?"
            -is_on                                      "is a on b?"

        :param string:
        :return: (string, [string,...,string])
            return[0] is command name
            return[1] is list of argument to the command
        """
        if len(string) >= 11 and string[-11:] == 'is a block.':
            return self.parse_create_block(string)
        elif len(string) >= 10 and string[-10:] == 'is a type.':
            return self.parse_create_type(string)
        elif len(string) >= 7 and string[:7] == 'what is':
            return self.parse_what_is_on(string)
        elif len(string.split(' ')) >= 2 and string.split(' ')[1] == 'is':
            return self.parse_set_instance_type(string)
        elif len(string) >= 19 and string[:27] == 'all current blocks that are':
            return self.parse_set_type_implication(string)
        elif len(string) >= 23 and string[:31] == 'are all current blocks that are':
            return self.parse_type_type_query(string)
        elif len(string) >= 3 and string[:3] == 'on(':
            return self.parse_set_on_set(string)
        elif len(string.split(' ')) == 4 and string.split(' ')[0] == 'is' and string.split(' ')[2] == 'on':
            return self.parse_is_on(string)
        elif len(string) >= 2 and string[:2] == 'is':
            return self.parse_instance_type_query(string)
        elif string == 'display data.':
            return self.parse_display_data(string)
        else:
            return None

    def parse_create_block(self, string):
        """
        For input of the form: a is a block.
        :param string:
        :return:
        """
        command = 'create_block'
        words = string[:-1].split(' ')

        if string[-1] != '.' or len(words) != 4:
            return None

        arguments = [words[0]]

        return command, arguments

    def parse_create_type(self, string):
        """
        For input of the form: blue is a type.
        :param string:
        :return:
        """
        command = 'create_type'
        words = string[:-1].split(' ')

        if string[-1] != '.' or len(words) != 4:
            return None

        arguments = [words[0]]

        return command, arguments

    def parse_set_instance_type(self, string):
        """
        For input of the form: a is blue.
        :param string:
        :return:
        """
        command = 'set_instance_type'
        words = string[:-1].split(' ')

        if string[-1] != '.' or len(words) != 3:
            return None

        arguments = [words[0], words[2]]

        return command, arguments

    def parse_set_type_implication(self, string):
        """
        For input of the form: all current blocks that are blue are horse.
        :param string:
        :return:
        """
        command = 'set_type_implication'
        arguments = []

        words = string[:-1].split(' ')

        if string[-1] != '.' or len(words) != 8:
            return None

        arguments = [words[5], words[7]]

        return command, arguments

    def parse_type_type_query(self, string):
        """
        For input of the form: are all blocks that are mammal horse?
        :param string:
        :return:
        """
        command = 'type_type_query'
        words = string[:-1].split(' ')

        if string[-1] != '?' or len(words) != 8:
            return None

        arguments = [words[6], words[7]]

        return command, arguments

    def parse_set_on_set(self, string):
        """
        For input of the form: on(a,B), on(B,fasd).
        :param string:
        :return:
        """
        command = 'set_on_set'
        words = string[:-1].split(', ')

        if string[-1] != '.':
            return None

        arguments = []

        for word in words:
            word = word.replace('on(','')
            word = word.replace(')','')
            [a,b] = word.split(',')
            arguments.append(a)
            arguments.append(b)

        return command, arguments

    def parse_instance_type_query(self, string):
        """
        For input of the form: is a blue?
        :return:
        """
        command = 'instance_type_query'
        words = string[:-1].split(' ')

        if string[-1] != '?' or len(words) != 3:
            return None

        arguments = [words[1], words[2]]

        return command, arguments

    def parse_display_data(self, string):
        """
        For input of the form: list tables.
        :param string: input
        :return:
        """

        return 'display_data', []

    def parse_what_is_on(self, string):
        """
        For input of the form: what is a on?
        :param string:
        :return:
        """

        command = 'what_is_on'
        words = string[:-1].split(' ')

        if string[-1] != '?' or len(words) != 4:
            return None

        arguments = [words[2]]

        return command, arguments

    def parse_is_on(self, string):
        """
        For input of the form: is a on b?
        :param string:
        :return:
        """

        command = 'is_on'
        words = string[:-1].split(' ')

        if string[-1] != '?' or len(words) != 4:
            return None

        arguments = [words[1], words[3]]

        return command, arguments










































