class Colors:
    def __init__(self, color_theme = "DTU") -> None:
        self.color_theme = color_theme

        if self.color_theme == "DTU":
            self.set_dtu_colors()

    def set_dtu_colors(self):
        self.cred = "#990000"
        self.blue = "#2F3EEA"
        self.brightgreen = "#1FD082"
        self.navyblue = "#030F4F"
        self.yellow = "#F6D04D"
        self.orange = "#FC7634"
        self.pink = "#F7BBB1"
        self.grey = "#DADADA"
        self.red = "#E83F48"
        self.green = "#008835"
        self.purple = "#79238E"
