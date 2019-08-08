from enum import IntEnum, auto


class Characters(IntEnum):
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


CHARACTERS_TO_STRING = {
    Characters.Smallman: "Mr. S",
    Characters.Duke: "Mr. U",
    Characters.Salmon: "Mr. Q",
    Characters.Rocker: "Ms. L",
    Characters.Taft: "Mr. C",
    Characters.Alice: "Ms. F",
    Characters.Teal: "Ms. R",
    Characters.Sikh: "Mr. K",
    Characters.Carlos: "Mr. P",
    Characters.Sari: "Ms. T",
    Characters.Bling: "Dr. N",
    Characters.Morgan: "Mr. D",
    Characters.Plain: "Dr. M",
    Characters.Oprah: "Ms. H",
    Characters.Queen: "Ms. J",
    Characters.Boots: "Ms. B",
    Characters.General: "Mr. G",
    Characters.Disney: "Mr. A",
    Characters.Helen: "Ms. E",
    Characters.Irish: "Ms. O",
    Characters.Wheels: "Mr. I",
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
}