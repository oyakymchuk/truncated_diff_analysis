class S_box:

    def __init__(self, bits, name=None, s_box=None):
        if s_box and len(s_box) == 2 ** bits:
            self.bits = bits
            self.s_box = s_box
            
        else:
            if bits == 2:
                self.bits = 2
                self.s_box = [2, 1, 3, 0]
            
            if bits == 3:
                self.bits = 3
                self.s_box = [1, 6, 5, 4, 0, 7, 3, 2]

            if bits == 4:
                self.bits = 4
                self.s_box = [7, 9, 4, 13, 0, 2, 12, 11, 10, 8, 1, 6, 14, 5, 15, 3]

        self.name = name

    def calculate_result(self, input_number):
        '''
            input must be a positive integer
        '''
        if input_number.bit_length() > self.bits:
            raise Exception('Input bit length > S_box bit length!')
        else:
            return self.s_box[input_number]