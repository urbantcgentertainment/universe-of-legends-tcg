#!/usr/bin/env python3
"""
Universe of Legends TCG - Auto-Renamer to Standard Format (card_001.png, card_002.png, ...)

Renames all card images in your 'Card_Images' folder to the exact standard IDs 
used by the HTML game (card_001.png, card_002.png, ...).

Usage:
  1. Place this script inside your 'Card_Images' folder (or pass the folder path as an argument).
  2. Run: python rename_to_card_numbers.py
"""

import os
import sys

SIZE_MAPPING = {
    "4216181": {
        "target": "card_001.png",
        "card_name": "Raya, Fearless Protector",
        "orig_title": "Raya_X1.png"
    },
    "4423474": {
        "target": "card_002.png",
        "card_name": "D-Rangers in Training",
        "orig_title": "Rangers_X3.png"
    },
    "4513959": {
        "target": "card_003.png",
        "card_name": "D-Ranger D-Fender",
        "orig_title": "Dfender_X3.png"
    },
    "4431094": {
        "target": "card_005.png",
        "card_name": "G0st, Simulated Tech Partner",
        "orig_title": "G0st.png"
    },
    "4317315": {
        "target": "card_006.png",
        "card_name": "Soldiers Ready for Battle",
        "orig_title": "SS.png"
    },
    "5098376": {
        "target": "card_008.png",
        "card_name": "Knox, Expanding Power",
        "orig_title": "KP.png"
    },
    "4801640": {
        "target": "card_009.png",
        "card_name": "Byte, Legend Collector",
        "orig_title": "BLC.png"
    },
    "3783343": {
        "target": "card_010.png",
        "card_name": "Jackson, Scientist in Training",
        "orig_title": "JS.png"
    },
    "2998550": {
        "target": "card_011.png",
        "card_name": "Key, Wanderer of the Crossroads",
        "orig_title": "Soilders_X3 3.png"
    },
    "4260745": {
        "target": "card_012.png",
        "card_name": "Tye, Guerrilla Raider",
        "orig_title": "TR.png"
    },
    "4777582": {
        "target": "card_013.png",
        "card_name": "Ron, Tempted by Time",
        "orig_title": "Card_Frame 3.png"
    },
    "3452407": {
        "target": "card_014.png",
        "card_name": "Barrier Healing",
        "orig_title": "Soilders_X3 5.png"
    },
    "4334447": {
        "target": "card_015.png",
        "card_name": "Confronting Bass",
        "orig_title": "RCB.png"
    },
    "3124767": {
        "target": "card_016.png",
        "card_name": "Cosmic Blast",
        "orig_title": "Soilders_X3 27.png"
    },
    "4816840": {
        "target": "card_017.png",
        "card_name": "Discovering Purpose",
        "orig_title": "Soilders_X3 28.png"
    },
    "3556850": {
        "target": "card_018.png",
        "card_name": "Enter the Multiverse",
        "orig_title": "Soilders_X3 32.png"
    },
    "2758052": {
        "target": "card_019.png",
        "card_name": "Essence Drain",
        "orig_title": "Soilders_X3 30.png"
    },
    "4144047": {
        "target": "card_020.png",
        "card_name": "Experimental Explosion",
        "orig_title": "Soilders_X3.png"
    },
    "3394147": {
        "target": "card_021.png",
        "card_name": "Final Gambit: Energy Overload",
        "orig_title": "Soilders_X3 2.png"
    },
    "3366502": {
        "target": "card_022.png",
        "card_name": "Final Gambit: Fated Contract",
        "orig_title": "Soilders_X3 36.png"
    },
    "3876644": {
        "target": "card_023.png",
        "card_name": "Focus Shot",
        "orig_title": "Soilders_X3 4.png"
    },
    "3589358": {
        "target": "card_024.png",
        "card_name": "Fracturing Reality",
        "orig_title": "Soilders_X3 22.png"
    },
    "2500788": {
        "target": "card_025.png",
        "card_name": "Helping Hand",
        "orig_title": "Soilders_X3 23.png"
    },
    "4829733": {
        "target": "card_026.png",
        "card_name": "Marie's Gossip",
        "orig_title": "Soilders_X3 35.png"
    },
    "3256385": {
        "target": "card_027.png",
        "card_name": "Mystic Strike",
        "orig_title": "Soilders_X3 31.png"
    },
    "3139710": {
        "target": "card_028.png",
        "card_name": "Soul Harvest",
        "orig_title": "Soilders_X3 40.png"
    },
    "3932504": {
        "target": "card_029.png",
        "card_name": "Star Field Re-Alignment",
        "orig_title": "Soilders_X3 33.png"
    },
    "3829156": {
        "target": "card_030.png",
        "card_name": "Ultimate Score",
        "orig_title": "Soilders_X3 36.png"
    },
    "3802385": {
        "target": "card_031.png",
        "card_name": "Universal Enlightenment",
        "orig_title": "Soilders_X3 34.png"
    },
    "4103973": {
        "target": "card_032.png",
        "card_name": "Zulu's Crushing Tactics",
        "orig_title": "RZC.png"
    },
    "4332943": {
        "target": "card_033.png",
        "card_name": "\"I am the Captain Now\"",
        "orig_title": "Soilders_X3 35.png"
    },
    "5115356": {
        "target": "card_034.png",
        "card_name": "Pocket Dimension",
        "orig_title": "Soilders_X3 34.png"
    },
    "4363260": {
        "target": "card_035.png",
        "card_name": "Rise of the Future Queen",
        "orig_title": "U.png"
    },
    "4987190": {
        "target": "card_036.png",
        "card_name": "Rise up King",
        "orig_title": "Soilders_X3 9.png"
    },
    "3863985": {
        "target": "card_037.png",
        "card_name": "Ultimate Promotion",
        "orig_title": "Soilders_X3 41.png"
    },
    "3940834": {
        "target": "card_038.png",
        "card_name": "High Noon",
        "orig_title": "Soilders_X3 8.png"
    },
    "4184953": {
        "target": "card_039.png",
        "card_name": "Raya's Watch",
        "orig_title": "Soilders_X3 37.png"
    },
    "4729649": {
        "target": "card_040.png",
        "card_name": "Energy Spire",
        "orig_title": "Spire_Energy.png"
    },
    "4231058": {
        "target": "card_041.png",
        "card_name": "Harnessed Spark of Wonder",
        "orig_title": "Spire_Energy 1.png"
    },
    "3926519": {
        "target": "card_042.png",
        "card_name": "Isis, the Diamond of Hope",
        "orig_title": "Spire_Energy.png"
    },
    "3672484": {
        "target": "card_043.png",
        "card_name": "Meteor, Tip of the Pyramid",
        "orig_title": "AMP.png"
    },
    "4251722": {
        "target": "card_044.png",
        "card_name": "Pearl of Burning Desire",
        "orig_title": "Spire_Energy 1.png"
    },
    "4490874": {
        "target": "card_045.png",
        "card_name": "Radiating Lotus",
        "orig_title": "Spire_Energy 2.png"
    },
    "3585953": {
        "target": "card_046.png",
        "card_name": "Stone of Life and Riches",
        "orig_title": "ASL.png"
    },
    "3606246": {
        "target": "card_047.png",
        "card_name": "The Vanguard Ascension",
        "orig_title": "AVA.png"
    },
    "4097123": {
        "target": "card_048.png",
        "card_name": "A Pirates Dream Theater",
        "orig_title": "Barrier_Blue 2.png"
    },
    "4221455": {
        "target": "card_049.png",
        "card_name": "Ancient City of Thebes",
        "orig_title": "Barrier_Blue 3.png"
    },
    "3862416": {
        "target": "card_050.png",
        "card_name": "Azalea Hall, Gateway to the Unknown",
        "orig_title": "Barrier_Blue 4.png"
    },
    "4378058": {
        "target": "card_051.png",
        "card_name": "Crossroad of Deals",
        "orig_title": "Barrier_Blue 1.png"
    },
    "4077188": {
        "target": "card_052.png",
        "card_name": "Crossroads of Justice",
        "orig_title": "Barrier_Blue 4.png"
    },
    "3898059": {
        "target": "card_053.png",
        "card_name": "Crossroads of Wealth",
        "orig_title": "Barrier_Blue 2.png"
    },
    "4440472": {
        "target": "card_054.png",
        "card_name": "LA, City of Dreams",
        "orig_title": "Barrier_Blue.png"
    },
    "4909948": {
        "target": "card_055.png",
        "card_name": "Mali, Kingdom of Riches",
        "orig_title": "Barrier_Blue 3.png"
    },
    "3547342": {
        "target": "card_056.png",
        "card_name": "The Sahara, Sands of Life and Death",
        "orig_title": "Barrier_Blue 4.png"
    },
    "4593446": {
        "target": "card_057.png",
        "card_name": "The Sin Parar",
        "orig_title": "Barrier_Blue 2.png"
    },
    "3860455": {
        "target": "card_058.png",
        "card_name": "Zulu's New Kingdom",
        "orig_title": "Barrier_Blue 1.png"
    },
    "3959477": {
        "target": "card_059.png",
        "card_name": "Bass's Pistol",
        "orig_title": "IBP.png"
    },
    "4087929": {
        "target": "card_060.png",
        "card_name": "D-Ryder, Version 1.5",
        "orig_title": "IDR.png"
    },
    "4007166": {
        "target": "card_061.png",
        "card_name": "Ion Blast Canon",
        "orig_title": "IIC.png"
    },
    "4184540": {
        "target": "card_062.png",
        "card_name": "Ion Cutlass",
        "orig_title": "Soilders_X3 20.png"
    },
    "3984622": {
        "target": "card_063.png",
        "card_name": "Ion Snip-Rifle",
        "orig_title": "Soilders_X3 19.png"
    },
    "4165414": {
        "target": "card_064.png",
        "card_name": "Ion Twin Pistols",
        "orig_title": "Soilders_X3 18.png"
    },
    "4441960": {
        "target": "card_065.png",
        "card_name": "Journal of Secrets",
        "orig_title": "Soilders_X3 25.png"
    },
    "3577212": {
        "target": "card_067.png",
        "card_name": "Master Spear",
        "orig_title": "IMS.png"
    },
    "4039320": {
        "target": "card_068.png",
        "card_name": "Mystical Pirate Glass",
        "orig_title": "Soilders_X3 24.png"
    },
    "3961000": {
        "target": "card_069.png",
        "card_name": "Peanut Coffee",
        "orig_title": "Soilders_X3 16.png"
    },
    "5126040": {
        "target": "card_070.png",
        "card_name": "Pearl Flintlocks",
        "orig_title": "Soilders_X3 21.png"
    },
    "3859008": {
        "target": "card_071.png",
        "card_name": "Proto-CDM",
        "orig_title": "IPC.png"
    },
    "4300637": {
        "target": "card_072.png",
        "card_name": "Raya's Jacket",
        "orig_title": "IRJ.png"
    },
    "3094827": {
        "target": "card_073.png",
        "card_name": "Shard of the Looking Glass",
        "orig_title": "Soilders_X3 17.png"
    },
    "3021044": {
        "target": "card_074.png",
        "card_name": "Shield of the Ancients",
        "orig_title": "Soilders_X3 22.png"
    },
    "4070552": {
        "target": "card_076.png",
        "card_name": "Akeem, Royal Companion",
        "orig_title": "Voodoo_Doll.png"
    },
    "4649198": {
        "target": "card_077.png",
        "card_name": "Alex, the Shot Caller",
        "orig_title": "Soilders_X3 7.png"
    },
    "3514889": {
        "target": "card_078.png",
        "card_name": "Alice Lost in Wonder",
        "orig_title": "Bass_Promo.png"
    },
    "4414918": {
        "target": "card_079.png",
        "card_name": "Alice, Blissful Wonder",
        "orig_title": "Soilders_X3.png"
    },
    "4234089": {
        "target": "card_080.png",
        "card_name": "Alice, Chaotic Wonder",
        "orig_title": "Card_Frame 2.png"
    },
    "4215594": {
        "target": "card_081.png",
        "card_name": "Alice, Questioning Wonder",
        "orig_title": "Card_Frame 1.png"
    },
    "4156550": {
        "target": "card_082.png",
        "card_name": "Alice, Void of Wonder",
        "orig_title": "Soilders_X3 1.png"
    },
    "4483996": {
        "target": "card_083.png",
        "card_name": "Anansi, Trickster at Heart",
        "orig_title": "Voodoo_Doll 3.png"
    },
    "4201510": {
        "target": "card_084.png",
        "card_name": "Baron, Man of Shadows",
        "orig_title": "Soilders_X3 4.png"
    },
    "4506355": {
        "target": "card_085.png",
        "card_name": "Bass, Protector of the Frontier",
        "orig_title": "BP.png"
    },
    "3746214": {
        "target": "card_086.png",
        "card_name": "Bass, Protector of the Frontier (Alt)",
        "orig_title": "Bass_Alt_X1.png"
    },
    "4820784": {
        "target": "card_087.png",
        "card_name": "Black Rabbit, Wonder-ing Traveler",
        "orig_title": "Bass_Promo 1.png"
    },
    "4049561": {
        "target": "card_088.png",
        "card_name": "Chris, Enlighted Battle Monk",
        "orig_title": "Card_Frame 5.png"
    },
    "4193242": {
        "target": "card_089.png",
        "card_name": "Cleopatra, Seducer of Hearts",
        "orig_title": "Soilders_X3 9.png"
    },
    "4331490": {
        "target": "card_090.png",
        "card_name": "Dart, Rustler of the West",
        "orig_title": "DW.png"
    },
    "4686672": {
        "target": "card_091.png",
        "card_name": "Edward, Shadow Dealer of the 7 Seas",
        "orig_title": "Soilders_X3 12.png"
    },
    "4347184": {
        "target": "card_092.png",
        "card_name": "George, Man of Science",
        "orig_title": "Soilders_X3 2.png"
    },
    "4828624": {
        "target": "card_093.png",
        "card_name": "Harriet, Freedom Conductor",
        "orig_title": "HFC.png"
    },
    "3525121": {
        "target": "card_094.png",
        "card_name": "Henri, Captain at Sea",
        "orig_title": "Soilders_X3 6.png"
    },
    "3980324": {
        "target": "card_095.png",
        "card_name": "Herald of the Fate's",
        "orig_title": "Soilders_X3 15.png"
    },
    "4324759": {
        "target": "card_096.png",
        "card_name": "Hidden with Power, Rachel",
        "orig_title": "Soilders_X3 2.png"
    },
    "3814316": {
        "target": "card_097.png",
        "card_name": "Jered, Freer of the Oppressed",
        "orig_title": "Soilders_X3 10.png"
    },
    "3358846": {
        "target": "card_098.png",
        "card_name": "Jordan, Crossroad Dealer",
        "orig_title": "Soilders_X3 4.png"
    },
    "4893179": {
        "target": "card_099.png",
        "card_name": "Kya, Eager to Explore",
        "orig_title": "Soilders_X3 10.png"
    },
    "3252619": {
        "target": "card_100.png",
        "card_name": "Leroy, Crossroads Musician",
        "orig_title": "Soilders_X3 5.png"
    },
    "4027406": {
        "target": "card_101.png",
        "card_name": "Marie, Misunderstood Witch",
        "orig_title": "Soilders_X3.png"
    },
    "4423091": {
        "target": "card_102.png",
        "card_name": "Mary, Deliverer of Justice",
        "orig_title": "Card_Frame.png"
    },
    "3996487": {
        "target": "card_103.png",
        "card_name": "Merv, Destine Magicain",
        "orig_title": "Voodoo_Doll 1.png"
    },
    "3505932": {
        "target": "card_105.png",
        "card_name": "Mr. Potter, the First Magician",
        "orig_title": "Soilders_X3 11.png"
    },
    "4826420": {
        "target": "card_106.png",
        "card_name": "Nate, Dead-shot Cowboy",
        "orig_title": "NC.png"
    },
    "4064137": {
        "target": "card_108.png",
        "card_name": "SLOTS",
        "orig_title": "Soilders_X3 11.png"
    },
    "4006135": {
        "target": "card_109.png",
        "card_name": "Tesla, Summoner of Storms",
        "orig_title": "TSS.png"
    },
    "3502443": {
        "target": "card_111.png",
        "card_name": "Toni, Teller of Legends",
        "orig_title": "Card_Frame 4.png"
    },
    "3538854": {
        "target": "card_112.png",
        "card_name": "Unknown Entity of the Universe",
        "orig_title": "Soilders_X3 16.png"
    },
    "4555631": {
        "target": "card_113.png",
        "card_name": "Zulu, the Warrior King",
        "orig_title": "ZK.png"
    },
    "3763710": {
        "target": "card_114.png",
        "card_name": "Alice, Unknown to Wonder",
        "orig_title": "Card_Frame.png"
    },
    "4722816": {
        "target": "card_115.png",
        "card_name": "Apex, the Wayward Eagle",
        "orig_title": "AE.png"
    },
    "2946531": {
        "target": "card_116.png",
        "card_name": "Belladonna, the Rising Star",
        "orig_title": "Soilders_X3 5.png"
    },
    "4947814": {
        "target": "card_117.png",
        "card_name": "Bishop, the War Elephant",
        "orig_title": "Soilders_X3 3.png"
    },
    "4667142": {
        "target": "card_118.png",
        "card_name": "Boa, the Striking Partner",
        "orig_title": "Soilders_X3 6.png"
    },
    "5050349": {
        "target": "card_119.png",
        "card_name": "Cleo, Bull of the High Seas",
        "orig_title": "Soilders_X3 12.png"
    },
    "4290935": {
        "target": "card_120.png",
        "card_name": "Curious Reader",
        "orig_title": "Bass_Promo 2.png"
    },
    "4578762": {
        "target": "card_121.png",
        "card_name": "D-Fensive Armor",
        "orig_title": "DA.png"
    },
    "4400271": {
        "target": "card_122.png",
        "card_name": "Dimensional Historian",
        "orig_title": "DH.png"
    },
    "3658174": {
        "target": "card_123.png",
        "card_name": "Lost legend of the Unknown",
        "orig_title": "Soilders_X3 14.png"
    },
    "4797378": {
        "target": "card_124.png",
        "card_name": "Loyal Follower's",
        "orig_title": "Followers_X3.png"
    },
    "4797334": {
        "target": "card_125.png",
        "card_name": "Loyal Followers",
        "orig_title": "LF.png"
    },
    "4083463": {
        "target": "card_126.png",
        "card_name": "Lynx, Barrier Protector",
        "orig_title": "Soilders_X3 17.png"
    },
    "4066265": {
        "target": "card_127.png",
        "card_name": "Minions of the Unknown",
        "orig_title": "Soilders_X3 15.png"
    },
    "3566690": {
        "target": "card_128.png",
        "card_name": "Ranger's Spirit",
        "orig_title": "Card_Frame 7.png"
    },
    "3474471": {
        "target": "card_129.png",
        "card_name": "Shaman's of Egypt",
        "orig_title": "Soilders_X3 8.png"
    },
    "4822135": {
        "target": "card_131.png",
        "card_name": "Souls Lost at Sea",
        "orig_title": "Soilders_X3 13.png"
    },
    "3561860": {
        "target": "card_132.png",
        "card_name": "Third Sight Duelers",
        "orig_title": "Soilders_X3 9.png"
    },
    "5155520": {
        "target": "card_133.png",
        "card_name": "Twilight, Watcher of All",
        "orig_title": "Soilders_X3 7.png"
    },
    "3962318": {
        "target": "card_134.png",
        "card_name": "Voodoo Doll",
        "orig_title": "Soilders_X3 18.png"
    },
    "4430278": {
        "target": "card_135.png",
        "card_name": "Wiccan in Training",
        "orig_title": "Soilders_X3 19.png"
    },
    "4400361": {
        "target": "card_136.png",
        "card_name": "\u0f0b\u0f0b\u0f0b\u0f0b",
        "orig_title": "Soilders_X3 13.png"
    },
    "3751002": {
        "target": "card_137.png",
        "card_name": "Ancient Politics",
        "orig_title": "Soilders_X3 39.png"
    },
    "4293806": {
        "target": "card_138.png",
        "card_name": "Chain Reaction",
        "orig_title": "Soilders_X3 1.png"
    },
    "3823494": {
        "target": "card_139.png",
        "card_name": "Defensive Matrix",
        "orig_title": "Soilders_X3 3.png"
    },
    "3453423": {
        "target": "card_140.png",
        "card_name": "Final Gambit: Last Words",
        "orig_title": "Soilders_X3 30.png"
    },
    "3860686": {
        "target": "card_141.png",
        "card_name": "Intervention",
        "orig_title": "Soilders_X3 31.png"
    },
    "3704229": {
        "target": "card_142.png",
        "card_name": "Mystic Circle",
        "orig_title": "Soilders_X3 32.png"
    },
    "3585792": {
        "target": "card_143.png",
        "card_name": "Raya's Defensive Measure",
        "orig_title": "Soilders_X3 10.png"
    },
    "4464453": {
        "target": "card_144.png",
        "card_name": "Star Aligned Shot",
        "orig_title": "Soilders_X3 38.png"
    },
    "3601373": {
        "target": "card_145.png",
        "card_name": "Targeted Cosmic Strike",
        "orig_title": "Soilders_X3 25.png"
    },
    "3666691": {
        "target": "card_146.png",
        "card_name": "Tech Reflect",
        "orig_title": "RTR.png"
    },
    "3748673": {
        "target": "card_147.png",
        "card_name": "Universal Slip",
        "orig_title": "Soilders_X3 6.png"
    }
}

def rename_folder(folder_path='.'):
    folder_path = os.path.abspath(folder_path)
    if not os.path.exists(folder_path):
        print(f"Directory '{folder_path}' does not exist.")
        return

    print(f"=== Renaming to Standard card_XXX.png Format in: {folder_path} ===
")
    
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    renamed = 0
    already_renamed = 0
    unmatched = 0

    for filename in files:
        if filename.endswith('.py') or filename.endswith('.csv') or filename.startswith('.'):
            continue

        filepath = os.path.join(folder_path, filename)
        size = os.path.getsize(filepath)

        match = SIZE_MAPPING.get(size) or SIZE_MAPPING.get(str(size))
        if match:
            target_name = match['target']
            card_name = match['card_name']
            target_path = os.path.join(folder_path, target_name)

            if filename == target_name:
                print(f"[OK] Already named: {target_name} ({card_name})")
                already_renamed += 1
                continue

            try:
                os.rename(filepath, target_path)
                print(f"[RENAMED] '{filename}' -> '{target_name}' ({card_name})")
                renamed += 1
            except Exception as e:
                print(f"[ERROR] Could not rename '{filename}': {e}")
        else:
            print(f"[SKIP] Unknown file: '{filename}' (size: {size} bytes)")
            unmatched += 1

    print(f"
=== Renaming Complete ===")
    print(f"Renamed: {renamed}")
    print(f"Already correct: {already_renamed}")
    print(f"Unmatched: {unmatched}")
    print(f"Total processed: {len(files)}")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    rename_folder(target)
