from cycler import cycler

# based on https://davidmathlogic.com/colorblind/#%23000000-%23E69F00-%2356B4E9-%23009E73-%23F0E442-%230072B2-%23D55E00-%23CC79A7
# Wong
class PlotColorsWong:
    Color1 = "#0072B2"  # blue
    Color1Light = "#56B4E9"  # cyan
    Color2 = "#D55E00"  # orange
    Color2Light = "#E69F00"  # light orange
    Color3 = "#009E73"  # green
    Color4 = "#F0E442"  # yellow
    Color5 = "#CC79A7"  # pink

    DarkGrey = "xkcd:dark grey"
    Grey = "xkcd:grey"
    LightGrey = "xkcd:light grey"
    White = "xkcd:white"


# based on https://personal.sron.nl/~pault/ bright qualitative colour scheme
class PlotColorsTolBright:
    Color1 = "#4477AA"  # blue
    Color1Light = "#66CCEE"  # cyan
    Color2 = "#AA3377"  # purple
    Color2Light = "#EE6677"  # red
    Color3 = "#228833"  # green
    Color4 = "#CCBB44"  # yellow
    Color5 = "#BBBBBB"  # grey

    DarkGrey = "xkcd:dark grey"
    Grey = "xkcd:grey"
    LightGrey = "xkcd:light grey"
    White = "xkcd:white"


# based on https://personal.sron.nl/~pault/ vibrant qualitative colour scheme
class PlotColorsTolVibrant:
    Color1 = "#0077BB"  # blue
    Color1Light = "#33BBEE"  # cyan
    Color2 = "#CC3311"  # red
    Color2Light = "#EE7733"  # orange
    Color3 = "#009988"  # teal
    Color4 = "#EE3377"  # magenta
    Color5 = "#BBBBBB"  # grey

    DarkGrey = "xkcd:dark grey"
    Grey = "xkcd:grey"
    LightGrey = "xkcd:light grey"
    White = "xkcd:white"


# based on https://personal.sron.nl/~pault/ muted qualitative colour scheme
class PlotColorsTolMuted:
    Color1 = "#44AA99"  # teal
    Color1Light = "#88CCEE"  # cyan
    Color2 = "#AA4499"  # purple
    Color2Light = "#CC6677"  # rose
    Color3 = "#117733"  # green
    Color4 = "#999933"  # olive
    Color5 = "#DDCC77"  # sand

    DarkGrey = "xkcd:dark grey"
    Grey = "xkcd:grey"
    LightGrey = "xkcd:light grey"
    White = "xkcd:white"


# based on SCL
class PlotColorsSCL:
    Color1 = "#F2E5AD"  # tan
    Color1Light = "#380A15"  # burgundy
    Color2 = "#E1E1E1"  # silver
    Color2Light = "#B2122C"  # red
    Color3 = "#000000"  # black
    Color4 = "#4477AA"  # blue
    Color5 = "#88CCEE"  # cyan

    DarkGrey = "xkcd:dark grey"
    Grey = "xkcd:grey"
    LightGrey = "xkcd:light grey"
    White = "xkcd:white"


PlotColors = PlotColorsTolVibrant

DEFAULT_COLOR_CYCLE = cycler(
    color=[
        PlotColors.Color1,
        PlotColors.Color2,
        PlotColors.Color3,
        PlotColors.Color4,
        PlotColors.Color5,
        PlotColors.Color1Light,
        PlotColors.Color2Light,
    ]
)
