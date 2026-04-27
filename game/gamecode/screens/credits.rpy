init offset = -1

screen credits():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("Credits"), scroll="viewport"):

        style_prefix "credits"

        vbox:
            label "[config.name!t] - Credits"
            text _("Version [config.version!t]\n")
            text ""
            if renpy.variant("mobile"):
                vbox:
                    text "Tap twice to open a link!"
            elif renpy.variant("pc"):
                vbox:
                    text "Use {i}shift{/i} + {i}click{/i} to open links!"
            text ""
            text "Threshold - {a=https://monstergirldreams.blogspot.ca}Dev Blog{/a} - {a=https://www.patreon.com/MonsterGirlDreams}Patreon{/a}"
            text "  Makes this game and multiple different things in it."
            text ""
            text ""
            text "{i}Artist Credits{/i}"
            text ""
            text "Jiffic - {a=https://www.pixiv.net/member.php?id=5691625}Pixiv{/a}"
            text "  Made art for: Perpetua, Nicci, Sofia, Jora, Elly, Elena, Original Elena, Shizu, Camilla, Himika, Mizuko, Minoni, Feng, Venefica, Gren, Nova, Iabel, the Town background, Sofia's Background, Capital Background, the kiss mark graphic, the world map, the lust crest status marker, and the patreon banner."
            text ""
            text "Applehead - {a=https://twitter.com/mistimagi}Twitter{/a} - {a=https://kalayara.deviantart.com/gallery/}Deviant Art{/a}"
            text "  Made art for: Kyra, Mika, Matango, Toxic Matango, Alraune, Rosaura, Amber, Ancilla, Trisha, Belle, The Elf, The Lizard Girl, The Salarisi, The Manticore, The Minotaur and her lewd cg, Galvi, The Kunoichi Trainee, The Voltlin, and The Tengu. The forest background, and mountain background. (As well as the original Black Knight.)"
            text ""
            text "Plasmid - {a=https://twitter.com/Plasmidhentai/}Twitter{/a} - {a=https://www.patreon.com/plasmid#_=_}Patreon{/a}"
            text "  Made art for: Amy, The Original Mimic, and Mara."
            text ""
            text "Houra - {a=https://bsky.app/profile/hourapro.bsky.social}Bluesky{/a} - {a=https://www.hourapro.com/}Houra's Website{/a}"
            text "  Made art for: Lillian, the Church Background, the Harpy, the Harpy Tengu, the Ghost, Amber Store BG, the Willpower Temple BG, and Inn Lobby BG. (Also the original Imp)."
            text ""
            text "NickBeja - {a=https://www.deviantart.com/nickbeja}Deviant Art{/a} - {a=https://www.patreon.com/nickbeja}Patreon{/a}"
            text "  Made art for: The Blue Slime, Nara, and the Lake BG. (As well as Original Vili)."
            text ""
            text "ADOPOLICH - {a=https://twitter.com/ADOPOLICH}Twitter{/a} - {a=https://www.pixiv.net/member.php?id=27601141}Pixiv{/a}"
            text "  Made art for: Aiko, Bed-Chan, Kotone, Lumiren, The Black Knight, The loot bag, Stella, Ushris, the Caverns background, the underwater background, and art for D.P. and her lewd CG."
            text ""
            text "Kenshin187 - {a=https://twitter.com/kenshinx187}Twitter{/a} - {a=https://twitter.com/lonerurouni187}TwitterSFW{/a} - {a=https://artalley.porn/@kenshin187}Mastodon{/a}"
            text "  Made art for: Vivian, Selena, and Elezibeth Regalia."
            text ""
            text "Otani - {a=https://twitter.com/tani_00tani}Twitter{/a} - {a=https://tanitani00tani34.wixsite.com/gottanitei/blank}Website{/a} - {a=https://www.pixiv.net/en/users/20325366}Pixiv{/a}"
            text "  Made art for: The generic imp, Vili, Catherine, Jennifer, Heather, The Mimic, Auria, Rika, Relria, Fashionable Succubus, Voltlin Livewire, Melody+Cadence, and Noir. Forest Dungeon BG."
            text ""
            text "Crescentia - {a=https://twitter.com/Crescentia4tuna}Twitter{/a} - {a=https://crescentia-fortuna.newgrounds.com/}Newgrounds{/a}"
            text "  Made art for: Beris."
            text ""
            text "Elakan  - {a=https://twitter.com/ElakanDraws}Twitter{/a}"
            text "  Made art for: Ceris, and the Labyrinth Backgrounds."
            text ""
            text "Danimarion  - {a=https://twitter.com/DanimarionDD}Twitter{/a}"
            text "  Made art for: Player Room BG and Inn Brothel Room BG."
            text ""
            text "Nav - {a=https://twitter.com/thatnav}Twitter{/a} - {a=https://www.pixiv.net/en/users/981085}Pixiv{/a}"
            text "  Made art for: Malicia."
            text ""
            text "DOPPEL - {a=https://x.com/doppelarts}Twitter{/a} - {a=https://bsky.app/profile/hinezumigogatsu.bsky.social}Bluesky{/a}"
            text "  Made art for: Vivian's Bedroom BG, the Guild Hall BG, and Kotone's Chamber BG."

            text ""
            text "ShivanHunter - Generously created the current UI."
            text ""
            text ""
            text "{a=https://mega.nz/file/OQ4kAIYI#r0Sp_QY22HQSdGGXBIW-_a0WYfILpM_EHI7JMndvY98}Repository of depreciated art assets.{/a}"
            text ""
            text ""
            text "{i}Writing Credits{/i}"
            text ""
            text "Valentin Cognito"
            text "  The current official editor."
            text "  Wrote the Minoni Hoof Stepping Scene, reading 'Lucidian Sweethearts!♥' variations with Minoni, 'Talk about books.' with Minoni and Manuscript arc, all of Gren, Jora stream bathing, a number of scenes for Selena, some of the Ancilla random facts, her pampering service scenes and her Helpless domination service scene, the Venefica Dream Scene, Venefica titfuck loss scene, scenes for Ushris: the breast worship scene, Ask about her tail, Pet her tail!, Ask about her claws, and the footjob scene related to it; Auria puff puff scene, Complimentary Compliments scene, treasure chest gloryhole paizuri, and money draining scenes; the walks with amy content."
            text "  Ambrosia's Hugging Handjob, 'Lazily lie together and let her slime suck you off.' and 'Languid Lovemaking.' scenes, Perpetua's Domineering Cum-Milking Slime Blanket scene, The cute Harpy brothel Scene, Fashionable Succubus Sex Scene, Cathy Capital Sex Scene, Ampere scenes for: where you're her chair, where you eat her out, going back to her place+breed her, and her place+loveydovey sex, Lovol's Handjob Scene, Lovol in the Arcade, The Lovol+Ampere threesome scenes, visiting the ghost Trio at the Big Lake, the kisses and blowjob scenes for the Fashionable succubus, Trisha's Lovey-Dovey Domestic Dream, Heather's Bed Temptation, and the food eating descriptions in the bar."
            text "  The Matango Den event, and the Matango Sex Loss scene. Melody and Cadence's Stanceless Loss scene. The Elf, Harpy Tengu, Harpy sex, Salaris blowjob, Voltlin Livewire titfuck, alraune make out, victory scenes. Shizu's 'Have her give you a footjob!' scene when you beat her on the mountain. Relria's Level Drain Titty Pillow Head Massage.♥︎♥︎. All of Malicia's Doll play scenes except for the inital 'Become her doll!'"
            text ""
            text "GameSalamander - Discord:(game_salamander) - {a=https://twitter.com/GameSalamander?s=09}Twitter{/a} - Does writing commissions."
            text "  Wrote the Kunoichi Feet Dream, the sex loss scene for Kyra, breast smothering minotaur loss, the no stance loss scene and sex stance win scene for the generic lizard girl, and the three roleplay scenes for Beris."
            text ""
            text "Oluap"
            text "  Wrote the Kunoichi Bottom brothel scene, defeating the bubble slime sex, double bubble slime brothel scene, Mara Glory Hole scene, Ghost Glory Hole scene, and Lizard Toll Bridge event."
            text ""
            text "Zhuan"
            text "  Wrote the Shizu Punishment Training scene, Camilla titfuck and sex loss scenes, Nursing handjob and Riding While milked scenes for Belle, Elena's two bar sex scenes, Kunoichi Trainee Glory Hole brothel event, the Kunoichi Rope trap event, Nicci's nursing HJ loss, and the Dark Elf glory hole event."
            text ""
            text "Nekoalchemy - Discord:(nekoalchemy) - Does writing commissions."
            text "  Wrote the Solo Imp loss scene, Solo Imp Brothel Scene, Solo Elf Brothel Scene, Elf Sex Dream Scene, the Nara neutral loss scene, and Galvi's intro, sex scene, and titfuck scene."
            text ""
            text "WilliamTheShatner - The now retired, unofficial, official editor. Also wrote some of the Ancilla random facts."
            text ""
            text ""
            text "{i}Code credits!{/i}"
            text ""
            text "Feltcutemightcleanlater"
            text "  Contributed and helps maintain the modding docs. Overhauls to game and mod data processing, additional user interface QoL and polish, expanding internal json functions and validation, porting the game from renpy v7 to v8, improvements to the Slime Parade minigame, miscellaneous code and QoL contributions."
            text ""
            text "Noeru and Feltcutemightcleanlater - Created the desktop platform's in-game mod manager."
            text ""
            text "Feniks - Color picker for renpy add on"
            text "{a=https://feniksdev.com}feniksdev.com{/a} - {a=https://feniksdev.itch.io/color-picker-for-renpy}Color Picker{/a}"




            text ""
            text ""
            text "{i}Music and SFX from the following.{/i} File names identify creator."
            text ""
            text "{a=https://www.bandlab.com/blackh20}Stalkwick{/a}: Discord (Stalwick#1518)"
            text "  Notably for providing: The Forest Dungeon Ambience (Forest Dungeon Lurking), 'Dreaming', 'Rough Travels', and 'Won't You be my experiment'."
            text ""
            text "{a=http://freemusicarchive.org/music/Ask%20Again/}Art Of Escapism/Ask Again/Mid Air Machine{/a}"
            text ""
            text "{a=https://www.purple-planet.com/}Purple Planet{/a}"
            text ""
            text "{a=http://wingless-seraph.net/}Wingless Seraph{/a}"
            text ""
            text "{a=https://dova-s.jp/_contents/author/profile193.html}MFP【Marron Fields Production】{/a}"
            text ""
            text "{a=https://dova-s.jp/_contents/author/profile220.html}Chocolate mint{/a}"
            text ""
            text "{a=https://dova-s.jp/_contents/author/profile162.html}Manbo Second Class{/a}"
            text ""
            text "{a=https://dova-s.jp/_contents/author/profile295.html}shimtone{/a}"
            text ""
            text "{a=https://dova-s.jp/_contents/author/profile217.html}Tanaka Tamago{/a}"
            text ""
            text "{a=https://maou.audio/}Maoudamashii{/a}"
            text ""
            text "{a=https://soundcloud.com/q7oumurij7fr/sets/rengoku-teien}Rengoku-Teien{/a}"
            text ""
            text "{a=https://pocket-se.info/}Pocket Sound{/a}"
            text ""
            text "{a=http://d-symphony.com/index.html}Dragon's symphony{/a}"
            text ""
            text "{a=https://www.dlsite.com/home/circle/profile/=/maker_id/RG32138.html}ayato sound create{/a}"
            text ""
            text "{a=https://www.dlsite.com/home/circle/profile/=/maker_id/RG07477.html}pierrotlunaire{/a}"              
            text ""
            text "{a=https://www.dlsite.com/home/work/=/product_id/RJ249087.html}BEEMYU{/a}"           
            text ""
            text "{a=https://otologic.jp/}Otologic{/a}"           
            text ""
            text "{a=http://www.kurage-kosho.info/guide.html}kurage-kosho{/a}"
            text ""
            text ""
            text "{i}SFX from the following.{/i}"
            text ""
            text "{a=https://www.dlsite.com/home/circle/profile/=/maker_id/RG05893.html}A water flea{/a} - {a=https://www.dlsite.com/maniax/work/=/product_id/RJ246489.html}Mizinko Materials: Sounds for Monster Girls{/a}"
            text ""
            text "{a=https://www.dlsite.com/home/circle/profile/=/maker_id/RG17630.html}pigmyon studio{/a} - {a=https://www.dlsite.com/home/work/=/product_id/RJ237368.html}Audio Material pigmyon sound effects 023 - Smartphone Ringtones -{/a} - {a=https://www.dlsite.com/home/work/=/product_id/RJ232739.html}pigmyon sound effects 020 - Finger Snapping -{/a}"
            text "" 
            text "{a=https://www.dlsite.com/home/circle/profile/=/maker_id/RG14009.html}Onteishu{/a} - {a=https://www.dlsite.com/maniax/work/=/product_id/RJ072991.html}Erotic SFX You Can Use{/a}"
            text "" 
            text "{a=https://www.dlsite.com/home/circle/profile/=/maker_id/RG21728.html}Orange Lovers{/a} - {a=https://www.dlsite.com/maniax/work/=/product_id/RJ113172.html}Orange Lovers Voice Materials Collection: Fellatio Voice{/a}"          
            text ""
            text "{a=https://taira-komori.jpn.org/freesound.html}taira-komori{/a}"
            text ""
            text "{a=http://osabisi.sakura.ne.jp/m2/index}Osabisi{/a}"

            text ""
            text ""
            text "Special thanks to: My patrons, Ren'Py, people who send me feedback and point out typos, Feltcutemightcleanlater for a myriad of QoL adds, and of course, you for playing this game."
            text ""
            text ""
            text "About Ren'Py"
            text ""
            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


## This is redefined in options.rpy to add text to the about screen.
define gui.about = ""


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size
