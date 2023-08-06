class Formatter:
    def binify(self, num_list, length=None):
        if length is None:
            length = len(bin(max(num_list))) - 2
        result = []
        for num in list(map(bin, num_list)):
            leading_zeros = "0" * (length + 2 - len(num))
            num = leading_zeros + num[2:]
            result.append(num)
        return "\n".join(result)
