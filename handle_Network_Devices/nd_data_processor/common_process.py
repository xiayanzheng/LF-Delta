import re

from lfcomlib.Jessica import DaPr

DaPr = DaPr.Core()


class CommonDataProcess:

    def findall_single_line_data(self, *args):
        regex_rule, data = args[0], args[1]
        data = re.findall(regex_rule, data)
        new_data = []
        for line in data:
            multi_space_to_one = re.sub("-+", " ", line)
            multi_space_to_one = re.sub("\\s+", "  ", multi_space_to_one)
            new_data.append(multi_space_to_one)
        return new_data

    def findall_multiline_data(self, *args):
        regex_rule, data = args[0], args[1]
        single_line_data = DaPr.convert_multiline_to_single_line(data, "|", " ", "")
        return self.findall_single_line_data(regex_rule, single_line_data)

    def bypass(self, *args):
        regex_rule, data = args[0], args[1]
        return data
