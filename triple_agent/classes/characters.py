from enum import Enum, auto

# Character names have spaces in them ("Mr. A"), so I'm opting to use
# letters, but single characters violates pylint.
# pylint: disable=invalid-name
class Characters(Enum):
    S = auto()
    U = auto()
    Q = auto()
    L = auto()
    C = auto()
    F = auto()
    R = auto()
    K = auto()
    P = auto()
    T = auto()
    N = auto()
    D = auto()
    M = auto()
    H = auto()
    J = auto()
    B = auto()
    G = auto()
    A = auto()
    E = auto()
    O = auto()
    I = auto()
    Toby = auto()
    Damon = auto()


CHARACTERS_TO_STRING = {
    Characters.A: "Mr. A",
    Characters.B: "Ms. B",
    Characters.C: "Mr. C",
    Characters.D: "Mr. D",
    Characters.E: "Ms. E",
    Characters.F: "Ms. F",
    Characters.G: "Mr. G",
    Characters.H: "Ms. H",
    Characters.I: "Mr. I",
    Characters.J: "Ms. J",
    Characters.K: "Mr. K",
    Characters.L: "Ms. L",
    Characters.M: "Dr. M",
    Characters.N: "Dr. N",
    Characters.O: "Ms. O",
    Characters.P: "Mr. P",
    Characters.Q: "Mr. Q",
    Characters.R: "Ms. R",
    Characters.S: "Mr. S",
    Characters.T: "Ms. T",
    Characters.U: "Mr. U",
}

PORTRAIT_MD5_DICT = {
    "dc1eaaaecfc24b1cbae0e3dd22cb47e4": Characters.S,
    "775985d662ee9c57c376f7ee00d9acbf": Characters.U,
    "8673afcd757ba4a140f50d883036bf5e": Characters.Q,
    "4fa5f5a10cc39b10a3b4662a3f48c75c": Characters.L,
    "f94928e3bdb14b72f4bafb90b6ed3bc7": Characters.C,
    "9bdd8a909687ce01e00b285213289e9e": Characters.F,
    "023d635b5f2039901e748370b1bb9ce0": Characters.R,
    "4b6fafed3acedab526eeb06fe3fd3b18": Characters.K,
    "f5961de554ba93c959b72fb80214687e": Characters.P,
    "e1346b215b3896b5b046d115b001c864": Characters.T,
    "7370c9bef830cdd7f598b5f7c0b33f6f": Characters.N,
    "36cc8b255e5a1243b4b63d299e7327c1": Characters.D,
    "0398fa2aeef203c8915fe9e48ab45fe7": Characters.M,
    "71145e3996b492a6d049c3a288650a92": Characters.H,
    "46bc37721e4e1ce2635bd07b97ac81c2": Characters.J,
    "9827fcb8f14c1fc4d064eb832c3a80be": Characters.B,
    "701d4ca838d51027bfd8717698b4f347": Characters.G,
    "9231e239066dbb6b9c27312637a55e84": Characters.A,
    "9b0a0f240ad9c483d4465784439d9f9d": Characters.E,
    "bc8a99d87995de1dd44ac3edf25d4180": Characters.O,
    "b139c77c346e497b348404fac1a3f2c4": Characters.I,
    "6047239de80c0b6fcf59e3b7bd0bf7a9": Characters.Toby,
    "4bd32c78192c0e08fd09f244a612a59d": Characters.Damon,
    "eba2303dcfce270520163c1a816eeeb6": Characters.U,
    "2e0f38e0557e0f1dac54b0c47b07e5bf": Characters.Toby,
}
