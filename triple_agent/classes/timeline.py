# pylint: disable=too-many-lines
from collections.abc import Sequence
from datetime import datetime
from enum import auto, Flag
from typing import Optional, List, Tuple
from dataclasses import dataclass, field

from triple_agent.classes.action_tests import ActionTest
from triple_agent.classes.books import Books
from triple_agent.classes.characters import Characters, CHARACTERS_TO_STRING
from triple_agent.classes.missions import Missions
from triple_agent.classes.roles import Roles
from triple_agent.classes.ordered_enum import ReverseOrderedFlag


class TimelineCoherency(Flag):
    Coherent = 0
    NoTimeline = auto()
    TimeRewind = auto()
    BookMissingColor = auto()
    NoGameStart = auto()
    NoGameEnding = auto()
    StartClockMismatch = auto()
    PickedMissionsMismatch = auto()
    CompletedMissionsMismatch = auto()
    SelectedMissionsMismatch = auto()
    GuestCountMismatch = auto()
    SpyNotCastInBeginning = auto()
    CharacterNotAssignedRole = auto()
    RoleWithNoCharacter = auto()
    ElapsedTimeMissing = auto()


# using ReverseOrderedFlag gives a deterministic sort to
# TimelineCategory, even if it doesn't make sense to sort these
# things.
class TimelineCategory(ReverseOrderedFlag):
    NoCategory = 0
    ActionTest = auto()
    ActionTriggered = auto()
    MissionPartial = auto()
    SniperLights = auto()
    MissionComplete = auto()
    MissionCountdown = auto()
    GameEnd = auto()
    GameStart = auto()
    TimeAdd = auto()
    Cast = auto()
    # selected means that the sniper can see it as a possible mission
    MissionSelected = auto()
    # enabled means that the spy can complete it, this will be smaller than
    # selected in pick modes.
    MissionEnabled = auto()
    SniperShot = auto()

    # Modifiers
    BananaBread = auto()

    # FP Objects
    Briefcase = auto()
    Statues = auto()
    Books = auto()
    Drinks = auto()

    # Modifiers cont.
    Conversation = auto()
    Watch = auto()

    Overtime = auto()

    def serialize(self):
        return [cat.name for cat in TimelineCategory if cat & self]


EVENT_IMAGE_HASH_DICT = {
    "b38d6b3162ecee914e68191eba678139": "got cupcake from waiter.",
    "5a109148b0321fa0458133f8a1ab3ab3": "waiter stopped offering drink.",
    "7817b66ae1b7e67f096667f3919a135a": "waiter stopped offering cupcake.",
    "5b399a954b788c11678efb89e55587fd": "spy leaves conversation.",
    "0ad1e5c65ab347f5908224802c504270": "spy enters conversation.",
    "3230377406adffef4544607df49fb432": "spy joined conversation with double agent.",
    "0faaca34326fffbbfde957989958fd7d": "marked book.",
    "62e3e62b1c77944948dfdda56666446a": "guest list purloined.",
    "1a8cdd526ca2256c8444c42aee40ece3": "action triggered: contact double agent",
    "3a5271e6847abcd01e7eee30b9f232cb": "real banana bread started.",
    "2d8b1b30edb6d62a27f953e0c79dded9": "action test red: contact double agent",
    "649e5e3e7ad3f714d74410361f3ff50e": "banana bread uttered.",
    "226a718a5e231ffa2c133531639b4439": "double agent contacted.",
    "23f4c27de9985f4bd254e5aee4caba1e": "45 seconds added to match.",
    "d26a40c458fca862d893e3ce71c6ec1b": "spy left conversation with double agent.",
    "1570134cb95670f10dd4a1570c6aed8a": "spy picks up briefcase.",
    "e5341af159fc7288343a5a937c8fccce": "picked up fingerprintable briefcase.",
    "d26597036c74e800f5e4f39cff214492": "action triggered: fingerprint ambassador",
    "b053b28d82e5ff6228658ee890605166": "started fingerprinting briefcase.",
    "909a216af5765cb4dfd217fb04860ed2": "fingerprinted briefcase.",
    "aec62ede9621d7bd65d2a5a23eabf532": "spy returns briefcase.",
    "ed3cddc39e5fac4372d65d0b2f3303fd": "game started.",
    "7a1416528959d1213aca828389ca462f": "marked less suspicious.",
    "32a02ddef19e9a5ec01aba6eacb054b6": "spy player takes control from ai.",
    "161e6be1904781e7b946643d2e310365": "action triggered: bug ambassador",
    "d8d68ffabbba7320ec394917bcefa51c": "begin planting bug while walking.",
    "b3dcc24ab5bb9fdfefda54cf90270600": "failed planting bug while walking.",
    "c9b69e088afdbd9b359ca79996c27aa4": "marked suspicious.",
    "67baba0bdce2ed478ef21b6f768c9a17": "action test green: contact double agent",
    "3ee230a7c3f1590ae5515270b80a38ba": "marked neutral suspicion.",
    "6faa9813756ee4a7f81cd379f84a5dad": "took last sip of drink.",
    "ed06251db400b4e711b57ac6a80780e2": "picked up statue.",
    "309d30bad509119670bb028f3e14463d": "action triggered: inspect statues",
    "3d2afd3ab54d4c31e6205f0d17950f1d": "action test white: inspect statues",
    "00e630506955a56d637b4a1de65771e5": "left statue inspected.",
    "951a4c5cc056b74f7cf85cbfee3b8acc": "spy cast.",
    "1f794e2c8a778a54748c4855941ad096": "ambassador cast.",
    "3faf4b9c22f75b93f4261c36a5e5ca94": "double agent cast.",
    "db3d6fe633fccf6f965a7de7cdb3b945": "suspected double agent cast.",
    "1d0c3a6a016d31b8e5e8df0325129844": "seduction target cast.",
    "fe4657cedf546b464cc46c3a21f59ab3": "left statue inspection cancelled.",
    "e1c3bfe9177f6ae2441ee84d6790ec9a": "right statue inspection cancelled.",
    "80d549213a0a5a64eb5fd5c1e9b03c9d": "left statue inspection interrupted.",
    "be3cda5592a1a916846e7196fbaa5e95": "statue inspection interrupted.",
    "5840248148cd6b0cea38d2ad58474535": "right statue inspection interrupted.",
    "5626495338f84019f99d6956a4ed02a5": "civilian cast.",
    "579670a2f2248b94e0e77daac2f62bf6": "bug ambassador selected.",
    "7c524e5a4be7dfb182dbccd671b9d881": "contact double agent selected.",
    "8e084c3d6391c6373d3c608382da1fdb": "transfer microfilm selected.",
    "9c0faeee1aa19ebf7b1dcc836f57310e": "swap statue selected.",
    "6c4824628cc971e5c735680d131626b5": "inspect 3 statues selected.",
    "3de9dc934fded6e28638ae579e601338": "seduce target selected.",
    "e512eb60cb8f40af55558f54a43865c1": "purloin guest list selected.",
    "82774a310f33d24a4242b6413719223e": "fingerprint ambassador selected.",
    "eb9751e75f502c69d13b8d290053cf6c": "bug ambassador enabled.",
    "d93491adf3331ca5160e8a970449b6f2": "contact double agent enabled.",
    "5b73571ec9cc0dec0fce8876ff772876": "transfer microfilm enabled.",
    "5975a54affafd2db3fe55c881170a7a2": "swap statue enabled.",
    "bb66cc6ca9c6f74a67c616a720c0a677": "inspect 3 statues enabled.",
    "521503717667e4825207996a4932656c": "seduce target enabled.",
    "2681afe7f005b1a374bf06beb5f5c0af": "purloin guest list enabled.",
    "0b43fbf44919051ad8f98cceca3b236e": "fingerprint ambassador enabled.",
    "d20d62e6307b4a0f25d503037cec0a30": "get book from bookcase.",
    "5a0e1b02ebe0269b60f3ef0911aba2db": "action triggered: transfer microfilm",
    "c8e97c2b128707e66b2a4a2105e04cbf": "action test white: transfer microfilm",
    "a60d7f6b936ce3d95bc03346704b709c": "remove microfilm from book.",
    "8069b4cc9125c5e564e33b1ad6431959": "action test green: transfer microfilm",
    "0d5a71d5447c4bc2348e5927f8ddb6be": "hide microfilm in book.",
    "6954ce09e91c6d69a80618db1e96fdc2": "put book in bookcase.",
    "8d4f2df56952c641d700766603b9f4b5": "transferred microfilm.",
    "5b59b4f3cab30a2f3e03f4056f1b38c4": "request drink from waiter.",
    "323b91fcf1a9da56c28fe81b4dd1877c": "picked up fingerprintable briefcase (difficult).",
    "bf24d6a70eb44615a2395a61d0019f41": "action test red: fingerprint ambassador",
    "34a781cf07abac08e110cfa9539489da": "fingerprinting failed.",
    "236090881b10fd68589e5b4d7a05fc09": "begin planting bug while standing.",
    "536509cfac1fba12e632f7b3bf0026ca": "bugged ambassador while standing.",
    "b09a162d3cb74796dfbfa152a77ccdd0": "spy puts down briefcase.",
    "fd2f4abf24058cc36b4472b294f70624": "missions reset.",
    "0202f0c6b885b60ffcdd9144e6225b37": "held statue inspected.",
    "b50d53e2c3cf20ead52832ccf1a8595f": "all statues inspected.",
    "dc8719e17cde5f7428da1799321f2e91": "put back statue.",
    "c0d169a807b1704ca503e2c1293ed876": "marked spy suspicious.",
    "12d041286098ee6c213abcc44d662b27": "action triggered: seduce target",
    "70c9710c4dc5adbb3e2de4045c4c8040": "begin flirtation with seduction target.",
    "e97828c37d813d423c65a40161b77ac0": "action test green: seduce target",
    "e46964ac0ea006ade7add17e114c8f6d": "flirt with seduction target: 51%",
    "39fd4381f226270075665d11f1b51360": "stopped talking.",
    "c640b53fec92bc1be46447e0ef1b3c90": "waiter offered drink.",
    "72759a3476e816057472567a63d1febd": "action triggered: purloin guest list",
    "371891839d73f956745c1438ca4da47a": "action test white: purloin guest list",
    "620e7ebe2fc3e5d805d1b6688d1eb307": "got drink from waiter.",
    "5b5c8345245a87d6e050ae4794504602": "sipped drink.",
    "5f0832dec6f670d263c68d65f7801bfb": "bit cupcake.",
    "d0bd47210b12ac6d2b62214cad7bbd5d": "flirtation cooldown expired.",
    "5784c6cdd823ff417b562567cf0c46bc": "gulped drink.",
    "a8b8c5ba7649dbebd31db6dd44dd40ed": "chomped cupcake.",
    "0c00f6ba136e8633041eab53ba8b218a": "bartender offered cupcake.",
    "bc913c68f90054fb95f53a8a1d4f42c4": "waiter offered cupcake.",
    "b2d269c794d079e0653d409d5536a6db": "waiter gave up.",
    "489d536dabec41f643ea9de811ee688e": "purloin guest list aborted.",
    "ce317bb385b4f8231b5888e1d1850de8": "action test green: inspect statues",
    "f0ad7ef2bd2d2bcdf950bb97d60ee4a9": "action triggered: swap statue",
    "8bdce8a2dd6fd66cca261892dbfa66f3": "action test white: swap statue",
    "9f9eba5d7ef5d94718f4c291a7f8415f": "statue swapped.",
    "fd34d424047339fc13e7b7dd5e1600f2": "missions completed. 10 second countdown.",
    "d5c8686d37e1f1f7bb98fb1efd696186": "ambassador's personal space violated.",
    "2ece32018f973bb00aef7c9105d1cb77": "rejected drink from waiter.",
    "ccfa5907d7b6f28ef8c22fec72687403": "picked up fingerprintable statue (difficult).",
    "329757ba419e524dc7198c7e5fa7bd17": "started fingerprinting statue.",
    "24bda9d67dfda798ba137e3cda969893": "action test green: fingerprint ambassador",
    "c4fd5b425ac587af10b56910f87389ef": "fingerprinted statue.",
    "128b75c0a0a13988f4560621a5a5ac9b": "action test green: swap statue",
    "f58915975f4fc169d8fc14873342d744": "statue swap pending.",
    "28e077700c5ee0d5fc4792e76bcfb098": "character picked up pending statue.",
    "7dccf8237bfe794727b060d8ba89dd96": "action test green: purloin guest list",
    "d91f89f90080a33b1e6bd222c574a191": "guest list purloin pending.",
    "ce77fd8d3d86f48174fbb6b477db81f1": "flirt with seduction target: 100%",
    "a82426e62385f9a189bad9ded2fef016": "target seduced.",
    "df37dbbb795a37ae7ab461fc3f864e77": "missions completed successfully.",
    "8e248ff240ba72a33ed2752a8e89f546": "inspect 2 statues selected.",
    "3767785942cb613f40586ec045fe7a85": "inspect 2 statues enabled.",
    "0f0cbe5ce306d857323d3c7842db6659": "action test white: contact double agent",
    "895902a2f65b2af298ce2fb77b192835": "flirt with seduction target: 94%",
    "e904df6aa47d6684f0e50de6e21ad9c2": "right statue inspected.",
    "ade41b6279ad9a98c3e6a96b9ad41025": "took shot.",
    "b2b98f845cc3d02c34c9a0ff3c980a08": "sniper shot civilian.",
    "7367356bfef3a56eea270a9acbd80776": "double agent left conversation with spy.",
    "115e1b6c144d18ac729e0ea7225db27c": "action test white: seduce target",
    "0bf2418405cd6e0733d60b6914266852": "flirt with seduction target: 68%",
    "c1d2ae516933eccf018d208a768102f4": "action test ignored: seduce target",
    "c89b2d7400e4702393a610042db50f59": "flirt with seduction target: 85%",
    "f13a4c11f29b2a800e941fcb907f390c": "overtime!",
    "426fbe1a317e86986dcba9d8e8d5d0f4": "delegated purloin timer expired.",
    "1d449ca29e070eecd4481d9d79bfbd1e": "picked up fingerprintable statue.",
    "a682c48dc256d52c7ed06f0f1d54db71": "action triggered: check watch",
    "882d5890f602fa469ed90a4cd4310e6d": "watch checked to add time.",
    "1c4a6f8bffcbcd01b524d851df179940": "action test green: check watch",
    "890a04a48d8f318c9cb49f9e8515f255": "delegated purloin to ms. o.",
    "008abd07ef76e22b0970394c43d95478": "flirt with seduction target: 69%",
    "0130bdee457add93dd4e24249903b170": "delegated purloin to ms. l.",
    "02f4960217f6b685ffcbb58ffff14a00": "flirt with seduction target: 33%",
    "0ca3cb9c9a0b28522390c7f2ee380e7f": "flirt with seduction target: 75%",
    "0d0cc1e5d137ad86292e3cc47c6e9c86": "flirt with seduction target: 47%",
    "0eb79ab25238e4d05f2f547201f836d0": "flirt with seduction target: 27%",
    "0fb9e9bcb97904da6874dc9b29f4928e": "action test ignored: inspect statues",
    "11446c98c0b8f4987562e3b38bad4ffd": "action test red: transfer microfilm",
    "132b29dc8813572dcb41c82a0559f8a6": "flirt with seduction target: 97%",
    "14304c57b4232b2559f4b668a5a4b807": "flirt with seduction target: 22%",
    "168ee1e7b870d92522aaeb07b1451a82": "flirt with seduction target: 39%",
    "178d3ac1b90f3f4161df72e742d742a8": "flirt with seduction target: 65%",
    "1863ed6523d63c66010d16538608116c": "flirt with seduction target: 19%",
    "1be6585aed858a0246d055744143eed3": "flirt with seduction target: 38%",
    "1c960a4197ed2ceaedb5e1b12f53d7cf": "flirt with seduction target: 30%",
    "1e064e90ef4af023e7a6080fbd75a044": "sniper shot spy.",
    "25986b7bc02f31d4fc7b273cb733feef": "request cupcake from waiter.",
    "2628aaa77d4e77bc36e799d565a83e77": "flirt with seduction target: 48%",
    "26442e507157bd7d9cbddd6150356ff0": "delegated purloin to ms. j.",
    "29ebb827c6d08d45f1e2bc1b5f06993c": "got drink from bartender.",
    "2d034815cfdb1306e9c697140bf042c0": "double agent joined conversation with spy.",
    "2e89204875819b9f5448152eda389c30": "flirt with seduction target: 32%",
    "2eaeedeae6f8dbc4a3149582c12222aa": "delegated purloin to ms. b.",
    "2f0cdf7cc401f92c4d34f4cca7032655": "flirt with seduction target: 34%",
    "2fdeb005aa5b68090c3a9130c5fe81bc": "flirt with seduction target: 70%",
    "3030c027b0685a2f445cabb477843472": "action test ignored: check watch",
    "32f4fa708cb96e2a9d45384e11514e6e": "flirt with seduction target: 41%",
    "33366c01b3e6f8299b3cf1d14f360bb4": "aborted watch check to add time.",
    "35223e69dde5ceb8fe18f8711ece2b02": "action test ignored: transfer microfilm",
    "3954f07db87d365583d71987e58fda6f": "flirt with seduction target: 57%",
    "39c1dd079ff9aa1274f5150d3304c7d1": "delegated purloin to mr. u.",
    "3a65f078b7ad9924ae0f3bf058b51169": "flirt with seduction target: 72%",
    "3f6b563150eea7b32708323cca213c54": "delegated purloin to dr. n.",
    "415ff3a1e6e51aaf0611421ac6e0d6fd": "flirt with seduction target: 29%",
    "441754b3111e3913e18e698ae9c207bc": "spy ran out of time.",
    "448b0b18c3a09ed41d84488a034c18f3": "fingerprinted ambassador.",
    "46b91310294671a31ad3a0623ea3cdb4": "flirt with seduction target: 25%",
    "47bd2c9d987d0e9ef1d145d8cd7033ce": "left alone while attempting banana bread.",
    "49bdce27aa60c4f34ffdafd86a8a7c16": "flirt with seduction target: 60%",
    "49f9b59d18b99f13583febd808cd7917": "delegated purloin to mr. g.",
    "4b24a9e9b9df01d427e2edf869e5ee9d": "bartender offered drink.",
    "4bcc20d93c4b850b8985b6197031f8e7": "flirt with seduction target: 35%",
    "4bcdc2d5fd310907ee499c433b776f0f": "flirt with seduction target: 54%",
    "4bd26f4a9e6c1edc3e2035de7c8a8c2a": "flirt with seduction target: 55%",
    "4ce8beafa62268bb71985ca4a9bead30": "flirt with seduction target: 66%",
    "4e41589a466f6ac7ff08c7829f7734d9": "flirt with seduction target: 26%",
    "4f32c7d2bf1e25f03b55fec2e552d10b": "bartender picked next customer.",
    "503a8976d8569cbb4a8502e56b55ed44": "interrupted speaker.",
    "53c9af79da8faaa274211676f6ffbda3": "rejected cupcake from bartender.",
    "54806d77104c14649b38f8f2c6903e97": "flirt with seduction target: 31%",
    "58af6e33a9bd712823a1abf9f2578c47": "flirt with seduction target: 56%",
    "58cf3c8119175ed44d89a7955d151177": "delegated purloin to dr. m.",
    "5915de854751bd0a7466146946874a65": "sniper shot too late for sync.",
    "59a992b89a032dd6af2243f69e4dcbb9": "flirt with seduction target: 77%",
    "5ae3800dcd8a3e50056b2209d9d6fb12": "delegated purloin to mr. s.",
    "5d8d9d2b4fe851884a8306aadfcc944d": "delegated purloin to ms. f.",
    "5eba266d222ef60ca6e0caa39d231bf7": "delegated purloin to mr. q.",
    "5fc24bc622f8cc183deb9413a858e9ef": "flirt with seduction target: 71%",
    "60fa7cfd5344d51d2d9d4d8a4d3db469": "flirt with seduction target: 86%",
    "612690ee57fdff9d320284a5399bb0ab": "flirt with seduction target: 76%",
    "6146b10d5097352f8072cbcef249c199": "got cupcake from bartender.",
    "623c1e0675228b9a540476be10c3156c": "fingerprinted drink.",
    "6336e31994ca52b268b5c6930a7c9cb4": "flirt with seduction target: 78%",
    "65fe6fe94761725d2938e374d85736ff": "started talking.",
    "67b9909e8f326fafeafaf50c7163e817": "flirt with seduction target: 95%",
    "685fe9f450388cacf8a31ece4021062a": "cast member picked up pending statue.",
    "697150cb5c35fa51bbcd4f214f30ae2e": "bugged ambassador while walking.",
    "6a3691df1947c3a5203323a4875865fa": "delegated purloin to mr. i.",
    "6ac3e883de358346fe230818e0fd485e": "action test canceled: inspect statues",
    "6cdc8223d458e091db83c2cbf7e71e22": "delegated purloin to ms. h.",
    "71c9717ee8921de8d7800ad71ca3a13e": "watch checked.",
    "759f3d9a0755f2b1b7521d5e93d4d0a9": "started fingerprinting drink.",
    "75fcdb86191a8bf01532c7da782c8116": "flirt with seduction target: 88%",
    "79073629942ab71d4bf3d2d6af006f88": "delegated purloin to mr. c.",
    "7ab168a3a87428f418702d60556e82e6": "flirt with seduction target: 21%",
    "7c16a3c821eb29f13d64ba472f17f79b": "fingerprinted cupcake.",
    "7ca1dd7181cdeca7e226d0eeeba132ca": "delegated purloin to mr. a.",
    "7f912b7c0084b3c01271aab0f7fc7fb6": "delegated purloin to ms. e.",
    "7fde0785cdfdee167da472222d4d217f": "action test red: check watch",
    "819d3fc05b3089cfb963072a4c151273": "delegating purloin guest list.",
    "82a204e8e852b37a851ef1f0b713c1cd": "action test ignored: fingerprint ambassador",
    "837bb26217155f84fb4bfe2b4b1367c1": "flirt with seduction target: 49%",
    "847a7b41637d81c653a52ff1a760985f": "took last bite of cupcake.",
    "847d70d8e075265323342a547298028a": "flirt with seduction target: 84%",
    "848cf551e0b342fb059f1102ba77d44a": "flirt with seduction target: 17%",
    "85173be8b0446f8321691d956ea68915": "delegated purloin to ms. t.",
    "88d9c0d39b79056a8d48aa032b26545a": "flirt with seduction target: 83%",
    "899f1f0dd0920ca2b84440266ee33e9b": "fingerprinted book.",
    "8aa018c5506557e9e1d428ca5f458e49": "flirt with seduction target: 37%",
    "8abde8f6aeec7ea307534e1311a718fd": "started fingerprinting cupcake.",
    "8ce1bf98721e89e5bcf7b23d32b14844": "action test canceled: seduce target",
    "8d1f6eddb0c4e7cb250e71763903bf7e": "flirt with seduction target: 74%",
    "8dbff9e4887361132f44da209cf5233f": "action test red: seduce target",
    "909b2e7a9500254b039e510c0a731249": "flirt with seduction target: 96%",
    "9302de372c9181d5af62fe374c1cb9a9": "marked spy neutral suspicion.",
    "9343fc0a48d8419556b162c4b4330893": "rejected drink from bartender.",
    "934f7f4c524b64ee00e8f17448e42d92": "flirt with seduction target: 50%",
    "962c97214930c5c4d1b0a38578b228f5": "flirt with seduction target: 63%",
    "964b8bc17191c68fa8be0c74ecbaebfa": "action test canceled: purloin guest list",
    "9a4c0c96de7d71a7b8202c735d24d29c": "inspect 1 statue enabled.",
    "9a768e854a76fac144d15ee7192d571c": "flirt with seduction target: 61%",
    "9bfe061d7d4be3ae6ca87e43f289bb6a": "flirt with seduction target: 73%",
    "9c6ac2a0fe4cb4fb4ab688212e6d8235": "flirt with seduction target: 20%",
    "9db0d8450e00977284a429cedf38aeaa": "action test canceled: contact double agent",
    "9ed2cbaff1f99b1db6e545f31bfbe303": "demand cupcake from bartender.",
    "a01c2f99726b38dbf360d05b3bf9e59a": "action test ignored: swap statue",
    "a49dc53706cbe18563c6b67722d3c9d5": "read book.",
    "a4a3c9196e006413811c5767bc24290a": "flirt with seduction target: 44%",
    "a5dc7ba96ca67a09a0756f5d1c12c2d9": "statue inspection cancelled.",
    "a760c91f6f6a24cfd6b830046b0de1ad": "flirt with seduction target: 62%",
    "a82457a167e64a02458cc50b43512af4": "missions completed. countdown pending.",
    "a8c292d03e71a5f1af6bd2fde4427738": "flirt with seduction target: 24%",
    "ab8ec690022a1248514b942b04b82e86": "flirt with seduction target: 81%",
    "acd4a096addff21933377af473527f21": "flirt with seduction target: 45%",
    "ace8be734b8e6e8df595348f21b23ced": "action test red: swap statue",
    "ad34799082002c1717a748510a54e769": "seduction canceled.",
    "ad5b6e0ee7acc0f0d71aa3aa9018625e": "marked spy less suspicious.",
    "af87659e0006fb2d27ef19b382379858": "delegated purloin to mr. d.",
    "b09dd8fbe9f7a681069139297089f119": "fake banana bread started.",
    "b146ae524d9761694064bfa940f59e64": "flirt with seduction target: 67%",
    "b2c88dbe05496b860577a7318138eeb4": "flirt with seduction target: 52%",
    "b987b04a2a4e32b5b5a7d68f3fbda3e7": "delegated purloin to mr. p.",
    "b9d893cd8998fe5ff11151b9e4d19f60": "action test canceled: check watch",
    "ba9a46cdc7b2e2fb041d2c742cf5dad7": "bug transitioned from standing to walking.",
    "bd936bc9d8569fd3b8bec5393a09ae1b": "flirt with seduction target: 80%",
    "bf68505aab9f5635a2a97c20e128b462": "action test ignored: purloin guest list",
    "c00da874cd9efc360bab63ba3a0e97b4": "action test canceled: transfer microfilm",
    "c1393151fa57a6955313dff48a550dc8": "gave up on bartender.",
    "c27e0e7d3e10937e93c2dae4929b95e8": "action test red: inspect statues",
    "c3833d5f3ba8e7562122ae5bc2fd25f5": "flirt with seduction target: 93%",
    "c3c1daf7160049a43fd21291cd1c23be": "flirt with seduction target: 43%",
    "c4e6ae8f7197bcf892c02e3c36731c2f": "flirt with seduction target: 28%",
    "c5b49f2c02fa8e9e8102c29135afaaa1": "flirt with seduction target: 53%",
    "c7d44c974a551b89c225c8b6497f6669": "rejected cupcake from waiter.",
    "c8de2be4461411624c90e1f338d79089": "flirt with seduction target: 91%",
    "c963ac0fbf80d05bcd22522dce82fb2a": "flirt with seduction target: 59%",
    "cacb73cd48d41f3e082155ae5b27098a": "banana bread aborted.",
    "cb2235998c9432bf2b67969f1782da6c": "failed flirt with seduction target.",
    "cb391063aa699063f30fb30d09d930a2": "flirt with seduction target: 92%",
    "ce169d862b96e4332fea2b87e4e70349": "started fingerprinting book.",
    "cee6523ae8fac2c9bdf4294e19330096": "flirt with seduction target: 46%",
    "cfe44cb30427c2b76952f258fd263207": "flirt with seduction target: 36%",
    "d0243803390cdf0b80ecce0a3a186bdb": "flirt with seduction target: 64%",
    "d0300447975a6647a9ff82cf9a404add": "action test red: purloin guest list",
    "d106b6ccd1f1ddde92e403ca460df534": "flirt with seduction target: 82%",
    "d3fd3c703a71a7bfcc322f08f85c594b": "flirt with seduction target: 87%",
    "d4a0f86d609da5c89b66d8a4b15a3fe9": "request cupcake from bartender.",
    "dd152858f24288047950885904d0d514": "flirt with seduction target: 40%",
    "de1a1170cbbef9f74c48c0c296b3241c": "flirt with seduction target: 58%",
    "de8984d8c5bfee14b6d5d624bde150bc": "delegated purloin to mr. k.",
    "df1af5c7c29ed3cf30c48d1971953e01": "flirt with seduction target: 90%",
    "e0667e13ed2258ecb4a8e25c807680a9": "flirt with seduction target: 23%",
    "e170f5097427974f65d45fbb72af10b5": "fake banana bread uttered.",
    "ea153b718afa28de67061b212e52d65a": "guest list returned.",
    "ee6d1467aa88c0f3e4c295ca12dfc262": "flirt with seduction target: 18%",
    "ef0f0c749f0185cc2916a1c6f7ee6ea7": "action test ignored: contact double agent",
    "ef663ea0d85f93acd6a9b64a410e832e": "flirt with seduction target: 79%",
    "ef935084b924d6a1dcedf57a25759fbf": "demand drink from bartender.",
    "f05f321c216219aeede9bc94bdb72e6d": "flirt with seduction target: 98%",
    "f0611fcc0e9df1efde54ec85e8fddb7c": "action test white: check watch",
    "f0e7902fb8b4916ce74b76478e8ab604": "request drink from bartender.",
    "f17dc7a76691f4059e592611f00d87a9": "flirt with seduction target: 99%",
    "f4d6d529674d1019afbb3dd8c26c8ca0": "guest list return pending.",
    "f5cc2ec0e31dfb1d9e34ef38a695e738": "flirt with seduction target: 89%",
    "f6f4dc6047d4bef82b73bd40bbeb0e3e": "delegated purloin to ms. r.",
    "fddbaf3ac68ea5dd87f0ab24c51f2d8f": "flirt with seduction target: 42%",
    "fed817294c78399897c5b77bbef0cd21": "inspect 1 statue selected.",
    "7eb6c49997c7feaf3f35a49175da3cd9": "dropped statue.",
    "769ff460ac58573d928c4c309f469d0f": "flirt with seduction target: ??%",
}

ACTOR_IMAGE_HASH_DICT = {
    "0fb96a733eebe09411e227360102c4f0": "spy",
    "9c12e97af292983969c66756a65bec4e": "sniper",
    "819b638a195b47fb6ca61ca5d80ad319": "game",
}

DIGIT_DICT = {
    "3b3024987024699ccf3a9f499237316e": "9",
    "d255e81708d321d798927e1921cdccfd": "9",
    "5e902ca8230067762fbe625ce4776bd2": "8",
    "c04166e6dc385d16099682934f5a7aa0": "8",
    "0119caf6c260ebc291c180e5c7ca1f4a": "7",
    "4b24b8cd4f2ac8adec1bc627ab4b6411": "7",
    "a2b138d0652eedcacea7f6ed77048a60": "6",
    "e4fac41013d1604961b34ac7bfba9989": "6",
    "90992c47deb02cfd398b78a64d3c340f": "5",
    "5ca652c4cd99a7b7e8d1fe86767ea9ea": "5",
    "dd78982af4b884f0445867709fb90910": "4",
    "a4f9f8efbafb56771db26b251ff7904e": "4",
    "f35378c67e9d817659506d70d0cfca86": "3",
    "4085c8ab395e1606c33fdd812a9fe593": "3",
    "5b25b5ec84697deaf9aea3b30cc9c732": "2",
    "fad37e64875d16ab3dd267f477d1b8df": "2",
    "acfd17d77acdf26659310ba006400306": "1",
    "56b4797333a8a978dc09ca930f33b160": "1",
    "c6582bfdae577240eec0fb186b54418f": "0",
    "14d84a05e212f0e88461c5bf3d5e9d32": "0",
    "5dac5ee740e383f279b42c86c3d254f4": "-",
    "b6e077626eccde142f3d895c294fab0d": "-",
    "ed1b59d9d8e604030b4bae6cabce5316": " ",
}


CATEGORIZATION_DICTIONARY = {
    ("game", "game started."): (
        TimelineCategory.GameStart,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "missions completed successfully."): (
        TimelineCategory.GameEnd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "missions completed. 10 second countdown."): (
        TimelineCategory.MissionCountdown,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "missions completed. countdown pending."): (
        TimelineCategory.MissionCountdown,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "overtime!"): (
        TimelineCategory.Overtime,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "sniper shot civilian."): (
        TimelineCategory.GameEnd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "sniper shot spy."): (
        TimelineCategory.GameEnd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "sniper shot too late for sync."): (
        TimelineCategory.NoCategory,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("game", "spy ran out of time."): (
        TimelineCategory.GameEnd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked book."): (
        TimelineCategory.Books | TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked less suspicious."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked neutral suspicion."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked spy less suspicious."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked spy neutral suspicion."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked spy suspicious."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "marked suspicious."): (
        TimelineCategory.SniperLights,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("sniper", "took shot."): (
        TimelineCategory.SniperShot,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "45 seconds added to match."): (
        TimelineCategory.TimeAdd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "aborted watch check to add time."): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "action test canceled: check watch"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd | TimelineCategory.ActionTest,
        Missions.NoMission,
        ActionTest.Canceled,
    ),
    ("spy", "action test canceled: contact double agent"): (
        TimelineCategory.ActionTest,
        Missions.Contact,
        ActionTest.Canceled,
    ),
    ("spy", "action test canceled: purloin guest list"): (
        TimelineCategory.ActionTest,
        Missions.Purloin,
        ActionTest.Canceled,
    ),
    ("spy", "action test canceled: inspect statues"): (
        TimelineCategory.ActionTest,
        Missions.Inspect,
        ActionTest.Canceled,
    ),
    ("spy", "action test canceled: seduce target"): (
        TimelineCategory.ActionTest,
        Missions.Seduce,
        ActionTest.Canceled,
    ),
    ("spy", "action test canceled: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTest,
        Missions.Transfer,
        ActionTest.Canceled,
    ),
    ("spy", "action test green: check watch"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd | TimelineCategory.ActionTest,
        Missions.NoMission,
        ActionTest.Green,
    ),
    ("spy", "action test green: contact double agent"): (
        TimelineCategory.ActionTest,
        Missions.Contact,
        ActionTest.Green,
    ),
    ("spy", "action test green: fingerprint ambassador"): (
        TimelineCategory.ActionTest,
        Missions.Fingerprint,
        ActionTest.Green,
    ),
    ("spy", "action test green: inspect statues"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Inspect,
        ActionTest.Green,
    ),
    ("spy", "action test green: purloin guest list"): (
        TimelineCategory.ActionTest,
        Missions.Purloin,
        ActionTest.Green,
    ),
    ("spy", "action test green: seduce target"): (
        TimelineCategory.ActionTest,
        Missions.Seduce,
        ActionTest.Green,
    ),
    ("spy", "action test green: swap statue"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Swap,
        ActionTest.Green,
    ),
    ("spy", "action test green: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTest,
        Missions.Transfer,
        ActionTest.Green,
    ),
    ("spy", "action test ignored: check watch"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd | TimelineCategory.ActionTest,
        Missions.NoMission,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: contact double agent"): (
        TimelineCategory.ActionTest,
        Missions.Contact,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: fingerprint ambassador"): (
        TimelineCategory.ActionTest,
        Missions.Fingerprint,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: inspect statues"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Inspect,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: purloin guest list"): (
        TimelineCategory.ActionTest,
        Missions.Purloin,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: seduce target"): (
        TimelineCategory.ActionTest,
        Missions.Seduce,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: swap statue"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Swap,
        ActionTest.Ignored,
    ),
    ("spy", "action test ignored: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTest,
        Missions.Transfer,
        ActionTest.Ignored,
    ),
    ("spy", "action test red: check watch"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd | TimelineCategory.ActionTest,
        Missions.NoMission,
        ActionTest.Red,
    ),
    ("spy", "action test red: contact double agent"): (
        TimelineCategory.ActionTest,
        Missions.Contact,
        ActionTest.Red,
    ),
    ("spy", "action test red: fingerprint ambassador"): (
        TimelineCategory.ActionTest,
        Missions.Fingerprint,
        ActionTest.Red,
    ),
    ("spy", "action test red: inspect statues"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Inspect,
        ActionTest.Red,
    ),
    ("spy", "action test red: purloin guest list"): (
        TimelineCategory.ActionTest,
        Missions.Purloin,
        ActionTest.Red,
    ),
    ("spy", "action test red: seduce target"): (
        TimelineCategory.ActionTest,
        Missions.Seduce,
        ActionTest.Red,
    ),
    ("spy", "action test red: swap statue"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Swap,
        ActionTest.Red,
    ),
    ("spy", "action test red: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTest,
        Missions.Transfer,
        ActionTest.Red,
    ),
    ("spy", "action test white: check watch"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd | TimelineCategory.ActionTest,
        Missions.NoMission,
        ActionTest.White,
    ),
    ("spy", "action test white: contact double agent"): (
        TimelineCategory.ActionTest,
        Missions.Contact,
        ActionTest.White,
    ),
    ("spy", "action test white: inspect statues"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Inspect,
        ActionTest.White,
    ),
    ("spy", "action test white: purloin guest list"): (
        TimelineCategory.ActionTest,
        Missions.Purloin,
        ActionTest.White,
    ),
    ("spy", "action test white: seduce target"): (
        TimelineCategory.ActionTest,
        Missions.Seduce,
        ActionTest.White,
    ),
    ("spy", "action test white: swap statue"): (
        TimelineCategory.Statues | TimelineCategory.ActionTest,
        Missions.Swap,
        ActionTest.White,
    ),
    ("spy", "action test white: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTest,
        Missions.Transfer,
        ActionTest.White,
    ),
    ("spy", "action triggered: bug ambassador"): (
        TimelineCategory.ActionTriggered,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: check watch"): (
        TimelineCategory.Watch | TimelineCategory.ActionTriggered,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: contact double agent"): (
        TimelineCategory.ActionTriggered,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: fingerprint ambassador"): (
        TimelineCategory.ActionTriggered,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: inspect statues"): (
        TimelineCategory.Statues | TimelineCategory.ActionTriggered,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: purloin guest list"): (
        TimelineCategory.ActionTriggered,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: seduce target"): (
        TimelineCategory.ActionTriggered,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: swap statue"): (
        TimelineCategory.Statues | TimelineCategory.ActionTriggered,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "action triggered: transfer microfilm"): (
        TimelineCategory.Books | TimelineCategory.ActionTriggered,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "all statues inspected."): (
        TimelineCategory.Statues | TimelineCategory.MissionComplete,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "ambassador cast."): (
        TimelineCategory.Cast,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "ambassador's personal space violated."): (
        TimelineCategory.NoCategory,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "banana bread aborted."): (
        TimelineCategory.NoCategory,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "banana bread uttered."): (
        TimelineCategory.BananaBread,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "bartender offered drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "bartender offered cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "bartender picked next customer."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "begin flirtation with seduction target."): (
        TimelineCategory.NoCategory,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "begin planting bug while standing."): (
        TimelineCategory.NoCategory,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "begin planting bug while walking."): (
        TimelineCategory.NoCategory,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "bug ambassador enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "bug ambassador selected."): (
        TimelineCategory.MissionSelected,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "bug transitioned from standing to walking."): (
        TimelineCategory.NoCategory,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "bugged ambassador while standing."): (
        TimelineCategory.MissionComplete,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "bugged ambassador while walking."): (
        TimelineCategory.MissionComplete,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "cast member picked up pending statue."): (
        TimelineCategory.Statues,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "character picked up pending statue."): (
        TimelineCategory.Statues,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "civilian cast."): (
        TimelineCategory.Cast,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "contact double agent enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "contact double agent selected."): (
        TimelineCategory.MissionSelected,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin timer expired."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to dr. m."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to dr. n."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. a."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. c."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. d."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. g."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. i."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. k."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. p."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. q."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. s."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to mr. u."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. b."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. e."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. f."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. h."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. j."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. l."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. o."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. r."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegated purloin to ms. t."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegating purloin guest list"): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "delegating purloin guest list."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "demand drink from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "demand cupcake from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "double agent cast."): (
        TimelineCategory.Cast,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "double agent contacted."): (
        TimelineCategory.MissionComplete,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "double agent joined conversation with spy."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "double agent left conversation with spy."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "dropped statue."): (
        TimelineCategory.Statues,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "failed flirt with seduction target."): (
        TimelineCategory.NoCategory,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "failed planting bug while walking."): (
        TimelineCategory.NoCategory,
        Missions.Bug,
        ActionTest.NoAT,
    ),
    ("spy", "fake banana bread started."): (
        TimelineCategory.BananaBread,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "fake banana bread uttered."): (
        TimelineCategory.BananaBread,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprint ambassador enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprint ambassador selected."): (
        TimelineCategory.MissionSelected,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted ambassador."): (
        TimelineCategory.MissionComplete,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted book."): (
        TimelineCategory.Books | TimelineCategory.MissionPartial,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted briefcase."): (
        TimelineCategory.Briefcase | TimelineCategory.MissionPartial,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted drink."): (
        TimelineCategory.Drinks | TimelineCategory.MissionPartial,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted cupcake."): (
        TimelineCategory.Drinks | TimelineCategory.MissionPartial,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinted statue."): (
        TimelineCategory.Statues | TimelineCategory.MissionPartial,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "fingerprinting failed."): (
        TimelineCategory.NoCategory,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: ??%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 100%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 15%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 16%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 17%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 18%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 19%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 20%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 21%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 22%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 23%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 24%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 25%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 26%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 27%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 28%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 29%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 30%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 31%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 32%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 33%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 34%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 35%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 36%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 37%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 38%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 39%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 40%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 41%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 42%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 43%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 44%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 45%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 46%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 47%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 48%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 49%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 50%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 51%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 52%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 53%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 54%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 55%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 56%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 57%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 58%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 59%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 60%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 61%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 62%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 63%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 64%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 65%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 66%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 67%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 68%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 69%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 70%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 71%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 72%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 73%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 74%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 75%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 76%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 77%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 78%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 79%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 80%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 81%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 82%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 83%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 84%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 85%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 86%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 87%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 88%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 89%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 90%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 91%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 92%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 93%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 94%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 95%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 96%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 97%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 98%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirt with seduction target: 99%"): (
        TimelineCategory.MissionPartial,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "flirtation cooldown expired."): (
        TimelineCategory.NoCategory,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "gave up on bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "get book from bookcase."): (
        TimelineCategory.Books,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "got drink from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "got cupcake from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "got drink from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "got cupcake from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "guest list purloin pending."): (
        TimelineCategory.NoCategory,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "guest list purloined."): (
        TimelineCategory.MissionComplete,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "guest list return pending."): (
        TimelineCategory.NoCategory,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "guest list returned."): (
        TimelineCategory.Drinks,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "gulped drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "chomped cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "held statue inspected."): (
        TimelineCategory.Statues | TimelineCategory.MissionPartial,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "hide microfilm in book."): (
        TimelineCategory.Books | TimelineCategory.MissionPartial,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 1 statue enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 1 statue selected."): (
        TimelineCategory.MissionSelected,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 2 statues enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 2 statues selected."): (
        TimelineCategory.MissionSelected,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 3 statues enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspect 3 statues selected."): (
        TimelineCategory.MissionSelected,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "inspection interrupted."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "statue inspection interrupted."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "interrupted speaker."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "left alone while attempting banana bread."): (
        TimelineCategory.BananaBread,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "left statue inspected."): (
        TimelineCategory.Statues | TimelineCategory.MissionPartial,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "left statue inspection interrupted."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "right statue inspection interrupted."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "left statue inspection cancelled."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "right statue inspection cancelled."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "statue inspection cancelled."): (
        TimelineCategory.NoCategory,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "missions reset."): (
        TimelineCategory.NoCategory,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "picked up fingerprintable briefcase (difficult)."): (
        TimelineCategory.Briefcase,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "picked up fingerprintable briefcase."): (
        TimelineCategory.Briefcase,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "picked up fingerprintable statue (difficult)."): (
        TimelineCategory.Statues,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "picked up fingerprintable statue."): (
        TimelineCategory.Statues,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "picked up statue."): (
        TimelineCategory.Statues,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "purloin guest list aborted."): (
        TimelineCategory.NoCategory,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "purloin guest list enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "purloin guest list selected."): (
        TimelineCategory.MissionSelected,
        Missions.Purloin,
        ActionTest.NoAT,
    ),
    ("spy", "put back statue."): (
        TimelineCategory.Statues,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "put book in bookcase."): (
        TimelineCategory.Books,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "read book."): (
        TimelineCategory.Books,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "real banana bread started."): (
        TimelineCategory.BananaBread,
        Missions.Contact,
        ActionTest.NoAT,
    ),
    ("spy", "rejected drink from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "rejected cupcake from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "rejected drink from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "rejected cupcake from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "remove microfilm from book."): (
        TimelineCategory.Books | TimelineCategory.MissionPartial,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "request drink from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "request cupcake from bartender."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "request drink from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "request cupcake from waiter."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "right statue inspected."): (
        TimelineCategory.Statues | TimelineCategory.MissionPartial,
        Missions.Inspect,
        ActionTest.NoAT,
    ),
    ("spy", "seduce target enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "seduce target selected."): (
        TimelineCategory.MissionSelected,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "seduction canceled."): (
        TimelineCategory.NoCategory,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "seduction target cast."): (
        TimelineCategory.Cast,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "sipped drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "bit cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy cast."): (TimelineCategory.Cast, Missions.NoMission, ActionTest.NoAT),
    ("spy", "spy enters conversation."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy joined conversation with double agent."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy leaves conversation."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy left conversation with double agent."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy picks up briefcase."): (
        TimelineCategory.Briefcase,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy player takes control from ai."): (
        TimelineCategory.NoCategory,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy puts down briefcase."): (
        TimelineCategory.Briefcase,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "spy returns briefcase."): (
        TimelineCategory.Briefcase,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "started fingerprinting book."): (
        TimelineCategory.Books,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "started fingerprinting briefcase."): (
        TimelineCategory.Briefcase,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "started fingerprinting drink."): (
        TimelineCategory.Drinks,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "started fingerprinting cupcake."): (
        TimelineCategory.Drinks,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "started fingerprinting statue."): (
        TimelineCategory.Statues,
        Missions.Fingerprint,
        ActionTest.NoAT,
    ),
    ("spy", "started talking."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "statue swap pending."): (
        TimelineCategory.Statues,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "statue swapped."): (
        TimelineCategory.Statues | TimelineCategory.MissionComplete,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "stopped talking."): (
        TimelineCategory.Conversation,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "suspected double agent cast."): (
        TimelineCategory.Cast,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "swap statue enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "swap statue selected."): (
        TimelineCategory.MissionSelected,
        Missions.Swap,
        ActionTest.NoAT,
    ),
    ("spy", "target seduced."): (
        TimelineCategory.MissionComplete,
        Missions.Seduce,
        ActionTest.NoAT,
    ),
    ("spy", "took last sip of drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "took last bite of cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "transfer microfilm enabled."): (
        TimelineCategory.MissionEnabled,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "transfer microfilm selected."): (
        TimelineCategory.MissionSelected,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "transferred microfilm."): (
        TimelineCategory.Books | TimelineCategory.MissionComplete,
        Missions.Transfer,
        ActionTest.NoAT,
    ),
    ("spy", "waiter gave up."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "waiter offered drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "waiter offered cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "waiter stopped offering drink."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "waiter stopped offering cupcake."): (
        TimelineCategory.Drinks,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "watch checked to add time"): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "watch checked to add time."): (
        TimelineCategory.Watch | TimelineCategory.TimeAdd,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
    ("spy", "watch checked."): (
        TimelineCategory.Watch,
        Missions.NoMission,
        ActionTest.NoAT,
    ),
}


@dataclass
# pylint: disable=too-many-instance-attributes
class TimelineEvent:
    actor: str
    _raw_time_str: str
    event: str
    cast_name: Tuple[Optional[Characters], ...]
    role: Tuple[Optional[Roles], ...]
    books: Tuple[Optional[Books], ...]
    elapsed_time: Optional[float] = field(default=None, init=False)
    time: Optional[float] = field(default=None, init=False)
    category: TimelineCategory = field(default=TimelineCategory.NoCategory, init=False)
    mission: Missions = field(default=Missions.NoMission, init=False)
    action_test: ActionTest = field(default=ActionTest.NoAT, init=False)

    def __post_init__(self):
        try:
            self.elapsed_time = float(self._raw_time_str)
        except ValueError:
            try:
                self.time = (
                    datetime.strptime(self._raw_time_str, "%M:%S.%f")
                    - datetime.strptime("00:00.0", "%M:%S.%f")
                ).total_seconds()
            except ValueError:
                self.time = (
                    datetime.strptime("00:00.0", "%M:%S.%f")
                    - datetime.strptime(self._raw_time_str, "-%M:%S.%f")
                ).total_seconds()
        self.category, self.mission, self.action_test = CATEGORIZATION_DICTIONARY[
            (self.actor, self.event)
        ]

        if self.event.startswith("delegated purloin to "):
            # assume there will be a single a character here, use that for the name
            self.event = "delegated purloin to {}.".format(
                CHARACTERS_TO_STRING[self.cast_name[0]].lower()
            )

        assert len(self.cast_name) == len(self.role)

    def __hash__(self):
        return hash(
            (
                self.actor,
                self.time,
                self.elapsed_time,
                self.event,
                self.cast_name,
                self.books,
                self.role,
                self.category,
                self.mission,
                self.action_test,
            )
        )

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return (
                self.actor,
                self.time,
                self.elapsed_time,
                self.event,
                self.cast_name,
                self.books,
                self.role,
                self.category,
                self.mission,
                self.action_test,
            ) == (
                other.actor,
                other.time,
                other.elapsed_time,
                other.event,
                other.cast_name,
                other.books,
                other.role,
                other.category,
                other.mission,
                other.action_test,
            )

        return NotImplemented

    def serialize(self):
        data = dict()
        data["actor"] = self.actor
        data["event"] = self.event
        data["cast_name"] = list(
            character.serialize()
            for character in self.cast_name
            if character is not None
        )
        data["role"] = list(role.name for role in self.role if role is not None)
        data["books"] = list(book.name for book in self.books if book is not None)
        data["elapsed_time"] = self.elapsed_time
        data["time"] = self.time
        data["category"] = self.category.serialize()
        data["mission"] = self.mission.name
        data["action_test"] = self.action_test.name

        return data


class Timeline(Sequence):
    def __init__(self, lines: List[TimelineEvent]):
        self.lines = lines
        self.parse_suspected_double_agents()

        super().__init__()

    def __getitem__(self, i):
        return self.lines[i]

    def __len__(self):
        return len(self.lines)

    def __repr__(self):  # pragma: no cover
        return self.__str__()

    def __str__(self):  # pragma: no cover
        return "\n".join(str(line) for line in self.lines)

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            try:
                return self.lines == other.lines
            # if lines is missing from either, they can't be equal
            except AttributeError:
                return False

        return NotImplemented

    def get_next_spy_action(self, event: TimelineEvent) -> Optional[TimelineEvent]:
        start_found = False

        for possible in self.lines:
            if start_found:
                if possible.actor == "spy":
                    return possible
            else:
                if possible == event:
                    start_found = True

        return None

    def parse_suspected_double_agents(self):
        # Games are parsed with all the yellow bars being assumed to be DoubleAgent.
        # Only after the game are the the suspected double agents identified and classified.
        suspected_das = set()

        for event in self:
            if (event.category & TimelineCategory.Cast) and (
                Roles.DoubleAgent in event.role
            ):
                assert len(event.role) == 1
                assert len(event.cast_name) == 1

                if event.event.startswith("suspected"):
                    suspected_das.add(event.cast_name[0])

        # iterate again in case there were sniper lights before cast assignment.
        for event in self:
            if set(event.cast_name) & suspected_das:
                event.role = tuple(
                    Roles.SuspectedDoubleAgent if cast in suspected_das else role
                    for cast, role in zip(event.cast_name, event.role)
                )

    def serialize(self):
        return [line.serialize() for line in self.lines]
