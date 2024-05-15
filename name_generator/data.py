from typing import Dict, List

dwarf_data: Dict[str, List] = {
    "name1_col1": [
        "al",
        "an",
        "aur",
        "BAR",
        "Bil",
        "Brun",
        "Bag",
        "Ban",
        "BAn",
        "BArn",
        "eil",
        "faR",
        "ful",
        "gan",
        "gal",
        "grim",
        "gim",
        "hil",
        "lon",
        "skar",
        "vAs",
        "vin",
        "thor",
        "thor",
    ],
    "name1_col2": [
        "viss",
        "arr",
        "angr",
        "vangr",
        "urr",
        "unn",
        "dr",
        "dinn",
        "inn",
        "sten",
    ],
    "name1_col2_female": ["et", "ja", "is", "i", "ssi", "da"],
    "name1_female_suffixes": ["a"],
    "transformations": [
        {"input": "A", "outputs": ["i", "a", "o", "u"]},  # any vowel
        {"input": "R", "outputs": ["l", "r"]},
        {"input": "B", "outputs": ["b", "d", "h"]},
    ],
}

anglo_data: Dict[str, List] = {
    "name1_col1": [
        "AR",
        "kAR",
        "kAs",
        "rAn",
        "brAn",
        "dAn",
        "frEn",
        "gEn",
        "hAR",
        "sEg",
        "sAN",
        "tIm",
        "bEn",
        "As",
    ],
    "name1_col2": [
        "An",
        "RAm",
        "lAn",
        "nAr",
        "rAth",
        "ric",
        "ret",
        "lyn",
        "mAnd",
        "der",
        "win",
    ],
    "name1_male_suffixes": [
        "ARt",
        "wArd",
        "son",
        "on",
        "fried",
        "wAll",
        "hardt",
        "aRd",
        "ey",
        "duin",
        "ly",
    ],
    "name1_female_suffixes": ["a", "ia", "ie", "isa"],
    "name2_col1": [
        "white",
        "red",
        "black",
        "grey",
        "west",
        "east",
        "fair",
        "rose",
        "grave",
        "wood",
        "daven",
        "ast",
        "avon",
        "bal",
        "bex",
        "blen",
        "brad",
        "row",
        "car",
        "cul",
        "dal",
        "dun",
        "dry",
        "fin",
        "gart",
        "gil",
        "glen",
        "kil",
        "king",
        "kirk",
        "knock",
        "lang",
        "lock",
        "lind",
        "nor",
        "pen",
        "pit",
        "pol",
        "pont",
        "ply",
        "strat",
        "stan",
        "swin",
        "tarn",
        "win",
        "wel",
        "roy",
        "grim",
        "mor",
    ],
    "name2_col2": [
        "beck",
        "berg",
        "berry",
        "bury",
        "burgh",
        "bourne",
        "burn",
        "cott",
        "den",
        "firth",
        "ham",
        "holme",
        "hurst",
        "ing",
        "low",
        "lyn",
        "mere",
        "more",
        "pool",
        "shaw",
        "stead",
        "ster",
        "stow",
        "ton",
        "ward",
        "wick",
        "wich",
        "worth",
        "field",
        "ford",
        "hill",
        "dale",
        "fell",
        "shire",
        "stein",
        "rock",
        "mill",
        "bridge",
        "son",
        "bluff",
    ],
    "transformations": [
        {"input": "E", "outputs": ["a", "i", "e"]},
        {"input": "I", "outputs": ["i", "e", "y"]},
        {"input": "A", "outputs": ["i", "a", "o", "u", "e"]},
        {"input": "R", "outputs": ["l", "r"]},
        {"input": "N", "outputs": ["n", "m"]},
    ],
}

french_data: Dict[str, List] = {
    "name1_col1": [
        "IN",
        "IB",
        "Il",
        "aB",
        "Is",
        "RuB",
        "RIB",
        "sIB",
        "arn",
        "auB",
        "clIB",
        "BIR",
        "jul",
        "vic",
    ],
    "name1_col2": [
        "ton",
        "is",
        "En",
        "Ant",
        "And",
        "ieR",
        "el",
        "Irt",
        "ois",
        "et",
        "ert",
        "ard",
    ],
    "name1_female_suffixes": [
        "*a",
        "ia",
        "*e",
    ],
    "name1_male_suffixes": [
        "d#ré",
        "eau",
        "aise",
        "r#ien",
        "ein",
        "erré",
        "ain",
    ],
    "name2_col1": [
        "nI",
        "vI",
        "rou",
        "for",
        "bAr",
        "clar",
        "lIv",
        "lI",
        "caste",
        "tour",
        "sAtte",
        "cAlle",
        "I",
        "Atin",
        "hAL",
    ],
    "name2_col2": [
        "ville",
        "val",
        "blAc",
        "mont",
        "court",
        "menil",
        "chatel",
        "vast",
        "bec",
        "dalle",
        "tuit",
        "fleur",
        "lan",
    ],
    "name2_prefixes": ["d'", "de ", "du "],
    "transformations": [
        {"input": "A", "outputs": ["a", "e", "i", "o", "u"]},
        {"input": "I", "outputs": ["e", "a", "i"]},
        {"input": "N", "outputs": ["n", "m"]},
        {"input": "L", "outputs": ["l", "r"]},
        {"input": "B", "outputs": ["l", "r", "m", "n", "c", "ch", "v", "s"]},
    ],
}

compound_tables: Dict[str, List] = {
    "nature_col1": [
        "green",
        "mist",
        "willow",
        "dream",
        "dusk",
        "night",
        "sage",
        "green",
        "dew",
        "high",
        "bright",
        "cliff",
        "hawk",
        "wind",
        "rain",
        "shadow",
        "sun",
        "cloud",
        "storm",
    ],
    "nature_col2": [
        "wood",
        "shade",
        "glade",
        "blossom",
        "wing",
        "vale",
        "grove",
        "thorn",
        "bark",
        "grass",
        "song",
        "weave",
        "heart",
        "whisper",
        "hunter",
        "root",
    ],
    "mountain_col1": [
        "shield",
        "deep",
        "dark",
        "steel",
        "heavy",
        "grim",
        "stout",
        "battle",
        "iron",
        "stone",
        "dust",
        "mountain",
        "strong",
        "great",
        "proud",
        "brave",
        "gravel",
    ],
    "mountain_col2": [
        "scream",
        "rage",
        "grip",
        "brew",
        "mail",
        "blaze",
        "strike",
        "helm",
        "spear",
        "beard",
        "fury",
        "break",
        "hammer",
        "brow",
        "cask",
        "mace",
        "mead",
        "pike",
        "pick",
    ],
    "generic_col1": [
        "ash",
        "swift",
        "cold",
        "gold",
        "silk",
        "dragon",
        "red",
        "lion",
        "glory",
        "black",
        "blue",
        "hell",
        "demon",
        "fire",
        "wine",
    ],
    "generic_col2": [
        "bane",
        "scar",
        "mark",
        "shine",
        "stride",
        "brand",
        "river",
        "rider",
        "crest",
        "blade",
        "bluff",
        "blood",
        "cloak",
        "born",
        "sworn",
        "fist",
        "ship",
        "arm",
        "gaze",
    ],
}
