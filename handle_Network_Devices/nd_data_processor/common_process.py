import re
from lfcomlib.Jessica import DaPrCore as DaPr


class CommonDataProcess(DaPr.Core):

    def findall_single_line_data(self, regex_rule, data):
        data = re.findall(regex_rule, data)
        new_data = []
        for line in data:
            multi_space_to_one = re.sub("-+", " ", line)
            multi_space_to_one = re.sub("\\s+","  ",multi_space_to_one)
            new_data.append(multi_space_to_one)
        return new_data


    def findall_multiline_data(self, regex_rule, data):
        single_line_data = self.convert_multiline_to_single_line(data, " ", "")
        return self.findall_single_line_data(regex_rule, single_line_data)