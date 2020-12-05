from enum import auto
from triple_agent.classes.ordered_enum import OrderedStringifyEnum


class Characters(OrderedStringifyEnum):
    Smallman = auto()
    Duke = auto()
    Salmon = auto()
    Rocker = auto()
    Taft = auto()
    Alice = auto()
    Teal = auto()
    Sikh = auto()
    Carlos = auto()
    Sari = auto()
    Bling = auto()
    Morgan = auto()
    Plain = auto()
    Oprah = auto()
    Queen = auto()
    Boots = auto()
    General = auto()
    Disney = auto()
    Helen = auto()
    Irish = auto()
    Wheels = auto()
    Toby = auto()
    Damon = auto()
    Alphonse = auto()
    Anna = auto()
    Arnold = auto()
    Brimsworth = auto()
    Clarice = auto()
    Cybil = auto()
    DJackson = auto()
    DJenson = auto()
    DJohnson = auto()
    Ether = auto()
    Flawn = auto()
    GenRitzini = auto()
    Girta = auto()
    Jim = auto()
    John = auto()
    Mitchell = auto()
    RBlain = auto()
    Sue = auto()
    Virginia = auto()
    Yvonne = auto()

    def serialize(self):
        return CHARACTERS_TO_STRING[self]

    def stringify(self):
        return CHARACTERS_TO_STRING[self]

    def alpha_sort(self):
        # This is used to provide a default sort based on the
        # character's letter names.  This is the simplest possible
        # metric, but it works so far.  If character names change, this
        # would need to change.  The full string can't be used because Dr.
        # would come before Mr., etc.
        # Because Toby & Damon are not the same format, they can't use
        # the same metric.  This is just a lame hack to make sure they're behind
        # all the letters in the sorting.
        if self == Characters.Damon:
            return "["

        if self == Characters.Toby:
            return "]"

        return CHARACTERS_TO_STRING[self][-1]


CHARACTERS_TO_STRING = {
    Characters.Disney: "Mr. A",
    Characters.Boots: "Ms. B",
    Characters.Taft: "Mr. C",
    Characters.Morgan: "Mr. D",
    Characters.Helen: "Ms. E",
    Characters.Alice: "Ms. F",
    Characters.General: "Mr. G",
    Characters.Oprah: "Ms. H",
    Characters.Wheels: "Mr. I",
    Characters.Queen: "Ms. J",
    Characters.Sikh: "Mr. K",
    Characters.Rocker: "Ms. L",
    Characters.Plain: "Dr. M",
    Characters.Bling: "Dr. N",
    Characters.Irish: "Ms. O",
    Characters.Carlos: "Mr. P",
    Characters.Salmon: "Mr. Q",
    Characters.Teal: "Ms. R",
    Characters.Smallman: "Mr. S",
    Characters.Sari: "Ms. T",
    Characters.Duke: "Mr. U",
    Characters.Toby: "Toby",
    Characters.Damon: "Damon",
    Characters.Alphonse : "Alphonse \"Snaps\" McGee",
    Characters.Anna : "Anna Klàvsky",
    Characters.Arnold : "Arnold Woods-Nicklaus",
    Characters.Brimsworth : "Brimsworth Buckswaggle, III",
    Characters.Clarice : "Clarice Sofia Mortgenstern",
    Characters.Cybil : "Cybil Disobedience",
    Characters.DJackson : "Danger P. Jackson",
    Characters.DJenson : "Danger P. Jenson",
    Characters.DJohnson : "Danger P. Johnson",
    Characters.Ether : "Ether van Trawn",
    Characters.Flawn : "Flawn Tabawt",
    Characters.GenRitzini : "Generalissimo Ritzini",
    Characters.Girta : "Girta Schuhleder",
    Characters.Jim : "Jim Bondo",
    Characters.John : "John Revolta",
    Characters.Mitchell : "Mitchell S. Barney",
    Characters.RBlain : "R. Blain Pembrookeberton",
    Characters.Sue : "Sue Veillance",
    Characters.Virginia : "Virginia Vulpes",
    Characters.Yvonne : "Yvonne Pennyweather",
}

PORTRAIT_MD5_DICT = {
    "dc1eaaaecfc24b1cbae0e3dd22cb47e4": Characters.Smallman,
    "775985d662ee9c57c376f7ee00d9acbf": Characters.Duke,
    "8673afcd757ba4a140f50d883036bf5e": Characters.Salmon,
    "4fa5f5a10cc39b10a3b4662a3f48c75c": Characters.Rocker,
    "f94928e3bdb14b72f4bafb90b6ed3bc7": Characters.Taft,
    "9bdd8a909687ce01e00b285213289e9e": Characters.Alice,
    "023d635b5f2039901e748370b1bb9ce0": Characters.Teal,
    "4b6fafed3acedab526eeb06fe3fd3b18": Characters.Sikh,
    "f5961de554ba93c959b72fb80214687e": Characters.Carlos,
    "e1346b215b3896b5b046d115b001c864": Characters.Sari,
    "7370c9bef830cdd7f598b5f7c0b33f6f": Characters.Bling,
    "36cc8b255e5a1243b4b63d299e7327c1": Characters.Morgan,
    "0398fa2aeef203c8915fe9e48ab45fe7": Characters.Plain,
    "71145e3996b492a6d049c3a288650a92": Characters.Oprah,
    "46bc37721e4e1ce2635bd07b97ac81c2": Characters.Queen,
    "9827fcb8f14c1fc4d064eb832c3a80be": Characters.Boots,
    "701d4ca838d51027bfd8717698b4f347": Characters.General,
    "9231e239066dbb6b9c27312637a55e84": Characters.Disney,
    "9b0a0f240ad9c483d4465784439d9f9d": Characters.Helen,
    "bc8a99d87995de1dd44ac3edf25d4180": Characters.Irish,
    "b139c77c346e497b348404fac1a3f2c4": Characters.Wheels,
    "6047239de80c0b6fcf59e3b7bd0bf7a9": Characters.Toby,
    "4bd32c78192c0e08fd09f244a612a59d": Characters.Damon,
    "eba2303dcfce270520163c1a816eeeb6": Characters.Duke,
    "2e0f38e0557e0f1dac54b0c47b07e5bf": Characters.Toby,
    "1ad437a9fe239ae75d9704944611740c": Characters.Alphonse,
    "e303c3e9c027c8d3318c3f7204ac24ff": Characters.Anna,
    "eac1f2687bdfa36c1116c485ea65fcfa": Characters.Arnold,
    "2e8c47cb24be51da297bd4f79794e01a": Characters.Brimsworth,
    "6211521e80ef976448b8642397fb3f6d": Characters.Clarice,
    "a9479476c35ad7adf399fdc261617148": Characters.Cybil,
    "47f88c36518d063e6f5489b3c5a6d2db": Characters.DJackson,
    "db688d509d0ed29adc7e3b93bb27541e": Characters.DJenson,
    "b72a9571b92cfe78f3252fe61eac55fa": Characters.DJohnson,
    "7b20926d74d3cfe07de3e72a4d746254": Characters.Ether,
    "fbbc04b490406078c045c6e6fe1debf1": Characters.Flawn,
    "30ee639e1f0d9766cd7a800c9a832575": Characters.GenRitzini,
    "d54bc31ec89d3cb9a1298217ddf7d619": Characters.Girta,
    "02481d141a7bc82a75559861de671976": Characters.Jim,
    "d14392d6783880ee736478cc63effe74": Characters.John,
    "dbdbf1b202c925bcd21e5727e21f8556": Characters.Mitchell,
    "ef2c92121a6a3c8ad6eb1125ad55054f": Characters.RBlain,
    "dbd14dec0ac780fcb79f2c1a80cea668": Characters.Sue,
    "421ef4d1c150a35f12fb0bed49908dad": Characters.Virginia,
    "a1965df8eb47d0ac2a1893ef7fce6729": Characters.Yvonne,

}
