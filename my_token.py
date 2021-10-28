class Token:
    coord: [2]
    type: str
    src: str
    value: str

    def __init__(self, coord, type, src, val):
        self.type = type
        self.coord = coord
        self.src = src
        self.value = val

    def print_token(self):
        print(self.coord, self.type, self.src, self.value)

    def get_str(self):
        return [self.coord, self.type.value, self.src, self.value]

    def get_type(self):
        return self.type

    def get_src(self):
        return self.src

    def get_coord(self):
        return self.coord

    def get_value(self):
        return self.value
