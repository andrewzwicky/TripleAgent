from cycler import cycler


class PlotColorsBase:
    def __init__(self):
        self.DarkGrey = "xkcd:dark grey"
        self.Grey = "xkcd:grey"
        self.LightGrey = "xkcd:light grey"
        self.White = "xkcd:white"

        self.cycler = cycler(
            color=[
                self.Color1,
                self.Color2,
                self.Color3,
                self.Color4,
                self.Color5,
                self.Color1Light,
                self.Color2Light,
            ]
        )


# based on https://davidmathlogic.com/colorblind/#%23000000-%23E69F00-%2356B4E9-%23009E73-%23F0E442-%230072B2-%23D55E00-%23CC79A7
# Wong
class PlotColorsWong(PlotColorsBase):
    def __init__(self):
        self.Color1 = "#0072B2"  # blue
        self.Color1Light = "#56B4E9"  # cyan
        self.Color2 = "#D55E00"  # orange
        self.Color2Light = "#E69F00"  # light orange
        self.Color3 = "#009E73"  # green
        self.Color4 = "#F0E442"  # yellow
        self.Color5 = "#CC79A7"  # pink

        super().__init__()


# based on https://personal.sron.nl/~pault/ bright qualitative colour scheme
class PlotColorsTolBright(PlotColorsBase):
    def __init__(self):
        self.Color1 = "#4477AA"  # blue
        self.Color1Light = "#66CCEE"  # cyan
        self.Color2 = "#AA3377"  # purple
        self.Color2Light = "#EE6677"  # red
        self.Color3 = "#228833"  # green
        self.Color4 = "#CCBB44"  # yellow
        self.Color5 = "#BBBBBB"  # grey

        super().__init__()


# based on https://personal.sron.nl/~pault/ vibrant qualitative colour scheme
class PlotColorsTolVibrant(PlotColorsBase):
    def __init__(self):
        self.Color1 = "#0077BB"  # blue
        self.Color1Light = "#33BBEE"  # cyan
        self.Color2 = "#CC3311"  # red
        self.Color2Light = "#EE7733"  # orange
        self.Color3 = "#009988"  # teal
        self.Color4 = "#EE3377"  # magenta
        self.Color5 = "#BBBBBB"  # grey

        super().__init__()


# based on https://personal.sron.nl/~pault/ muted qualitative colour scheme
class PlotColorsTolMuted(PlotColorsBase):
    def __init__(self):
        self.Color1 = "#44AA99"  # teal
        self.Color1Light = "#88CCEE"  # cyan
        self.Color2 = "#AA4499"  # purple
        self.Color2Light = "#CC6677"  # rose
        self.Color3 = "#117733"  # green
        self.Color4 = "#999933"  # olive
        self.Color5 = "#DDCC77"  # sand

        super().__init__()


# based on SCL
class PlotColorsSCL(PlotColorsBase):
    def __init__(self):
        self.Color1 = "#F2E5AD"  # tan
        self.Color1Light = "#380A15"  # burgundy
        self.Color2 = "#E1E1E1"  # silver
        self.Color2Light = "#B2122C"  # red
        self.Color3 = "#000000"  # black
        self.Color4 = "#4477AA"  # blue
        self.Color5 = "#88CCEE"  # cyan

        super().__init__()


PlotColors = PlotColorsTolVibrant()
