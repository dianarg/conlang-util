#!/usr/bin/env python

import flavored_words

base = [
    'Amurtah',  # Okanta name for homeworld (Orbis Aurea)
    'Orakoe',  # name of moon (Orbis Argenta)
    'Harmarandh',  # name of first shamans
    'Haj-Harmarandh',  # great metropolis that fell
    'Uutoh',  # Okantan faith
]

# Names - consonant-heavy and followed by clan name
names = [
    'Arakhu',
    'Tauth-el',
    'Kithare',
    'Lenshura',
    'Yashka',
    'Zureen'
    'Tembarok',
    'Dahon',
    'Orukughan',
    'Raod-Rah',
    'Ijiria',
    'Najrim',
    'Hajok',
    'Jahokvar',
    'Indruva',
    'Hakuvim',
    'Korimim',
    'Tanisk',
    'Uskvallar',
    'Maelich',
    'Arkhonis',
    'Bekkar',
    'dushon',
    'kurthaya',
    'dahok',
    'hajon',
    'maelisk',
    'uskarok',
    'kimbare',
    'kumare',
    'zakuleem',
    ]

tribes = [
    'DkaHaruso',
    'Vikoth',
    'Korbasandra',
    'Shakora',
    'Kunthfar',
    'Sankal',
    'Uthora',
    'Omora',
    'Haknarahadan',
    'Arh Horok-Khara',  # (group of clans, "the True Way to the Future's Promise")
    # 'Skyreach',
]

# Other places:
places = [
    'Karkhota',
    'Pah',
    'Orush',
    'Bedor Wayes',
    'Tep Halaisu',
    'Gathkadrana',  # Fortress
    'Korbasandra',  # Wasteland
    'Pahnahadra',
    'Mikawdra',
    'Ankhor Naragh',
    'Kehella',  # Valley
    'Harok',
    'Harok-Shakora',
    'Aharak Jahora-nar',  # "Respite of the Ancient Disquiet"
    'Jornamur',
]


if __name__ == '__main__':
    all_names = base + names + tribes + places
    gen_names = flavored_words.generate_words(all_names, 20)
    # gen_names = flavored_words.generate_words(names, 20)
    print(('\n'.join(gen_names)))
