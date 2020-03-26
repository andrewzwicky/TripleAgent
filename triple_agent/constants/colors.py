from cycler import cycler


class PlotColorsBase:
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.color_1 = None
        self.color_1_light = None
        self.color_2 = None
        self.color_2_light = None
        self.color_3 = None
        self.color_4 = None
        self.color_5 = None

        self.fig_facecolor = None

        self.dark_grey = "xkcd:dark grey"
        self.grey = "xkcd:grey"
        self.light_grey = "xkcd:light grey"
        self.white = "xkcd:white"

        self.cycler = None

    def add_cycler(self):
        self.cycler = cycler(
            color=[
                self.color_1,
                self.color_2,
                self.color_3,
                self.color_4,
                self.color_5,
                self.color_1_light,
                self.color_2_light,
            ]
        )


# based on https://davidmathlogic.com/colorblind/#%23000000-%23E69F00-%2356B4E9-%23009E73-%23F0E442-%230072B2-%23D55E00-%23CC79A7
# Wong
class PlotColorsWong(PlotColorsBase):  # pragma: no cover
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        self.color_1 = "#0072B2"  # blue
        self.color_1_light = "#56B4E9"  # cyan
        self.color_2 = "#D55E00"  # orange
        self.color_2_light = "#E69F00"  # light orange
        self.color_3 = "#009E73"  # green
        self.color_4 = "#F0E442"  # yellow
        self.color_5 = "#CC79A7"  # pink

        self.add_cycler()


# based on https://personal.sron.nl/~pault/ bright qualitative colour scheme
class PlotColorsTolBright(PlotColorsBase):  # pragma: no cover
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        self.color_1 = "#4477AA"  # blue
        self.color_1_light = "#66CCEE"  # cyan
        self.color_2 = "#AA3377"  # purple
        self.color_2_light = "#EE6677"  # red
        self.color_3 = "#228833"  # green
        self.color_4 = "#CCBB44"  # yellow
        self.color_5 = "#BBBBBB"  # grey

        self.fig_facecolor = "white"

        self.add_cycler()


# based on https://personal.sron.nl/~pault/ vibrant qualitative colour scheme
class PlotColorsTolVibrant(PlotColorsBase):  # pragma: no cover
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        self.color_1 = "#0077BB"  # blue
        self.color_1_light = "#33BBEE"  # cyan
        self.color_2 = "#CC3311"  # red
        self.color_2_light = "#EE7733"  # orange
        self.color_3 = "#009988"  # teal
        self.color_4 = "#EE3377"  # magenta
        self.color_5 = "#BBBBBB"  # grey

        self.fig_facecolor = "white"

        self.add_cycler()


# based on https://personal.sron.nl/~pault/ muted qualitative colour scheme
class PlotColorsTolMuted(PlotColorsBase):  # pragma: no cover
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        self.color_1 = "#44AA99"  # teal
        self.color_1_light = "#88CCEE"  # cyan
        self.color_2 = "#AA4499"  # purple
        self.color_2_light = "#CC6677"  # rose
        self.color_3 = "#117733"  # green
        self.color_4 = "#999933"  # olive
        self.color_5 = "#DDCC77"  # sand

        self.fig_facecolor = "white"

        self.add_cycler()


# based on SCL
class PlotColorsSCL(PlotColorsBase):  # pragma: no cover
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        super().__init__()

        self.color_1 = "#F2E5AD"  # tan
        self.color_1_light = "#380A15"  # burgundy
        self.color_2 = "#E1E1E1"  # silver
        self.color_2_light = "#B2122C"  # red
        self.color_3 = "#000000"  # black
        self.color_4 = "#4477AA"  # blue
        self.color_5 = "#88CCEE"  # cyan

        self.fig_facecolor = "white"

        self.add_cycler()


PLOT_COLORS = PlotColorsTolVibrant()
