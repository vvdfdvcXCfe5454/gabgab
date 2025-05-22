from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Exon import Abishnoi as abishnoi
from Exon.modules.resources.fonts import Fonts


@abishnoi.on_cmd(["font", "fonts"])
async def style_buttons(c, m, cb=False):
    buttons = [
        [
            InlineKeyboardButton("𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛", callback_data="style+typewriter"),
            InlineKeyboardButton("𝕆𝕦𝕥𝕝𝕚𝕟𝕖", callback_data="style+outline"),
            InlineKeyboardButton("𝐒𝐞𝐫𝐢𝐟", callback_data="style+serif"),
        ],
        [
            InlineKeyboardButton("𝑺𝒆𝒓𝒊𝒇", callback_data="style+bold_cool"),
            InlineKeyboardButton("𝑆𝑒𝑟𝑖𝑓", callback_data="style+cool"),
            InlineKeyboardButton("Sᴍᴀʟʟ Cᴀᴘs", callback_data="style+small_cap"),
        ],
        [
            InlineKeyboardButton("𝓈𝒸𝓇𝒾𝓅𝓉", callback_data="style+script"),
            InlineKeyboardButton("𝓼𝓬𝓻𝓲𝓹𝓽", callback_data="style+script_bolt"),
            InlineKeyboardButton("ᵗⁱⁿʸ", callback_data="style+tiny"),
        ],
        [
            InlineKeyboardButton("ᑕOᗰIᑕ", callback_data="style+comic"),
            InlineKeyboardButton("𝗦𝗮𝗻𝘀", callback_data="style+sans"),
            InlineKeyboardButton("𝙎𝙖𝙣𝙨", callback_data="style+slant_sans"),
        ],
        [
            InlineKeyboardButton("𝘚𝘢𝘯𝘴", callback_data="style+slant"),
            InlineKeyboardButton("𝖲𝖺𝗇𝗌", callback_data="style+sim"),
            InlineKeyboardButton("Ⓒ︎Ⓘ︎Ⓡ︎Ⓒ︎Ⓛ︎Ⓔ︎Ⓢ︎", callback_data="style+circles"),
        ],
        [
            InlineKeyboardButton("🅒︎🅘︎🅡︎🅒︎🅛︎🅔︎🅢︎", callback_data="style+circle_dark"),
            InlineKeyboardButton("𝔊𝔬𝔱𝔥𝔦𝔠", callback_data="style+gothic"),
            InlineKeyboardButton("𝕲𝖔𝖙𝖍𝖎𝖈", callback_data="style+gothic_bolt"),
        ],
        [
            InlineKeyboardButton("C͜͡l͜͡o͜͡u͜͡d͜͡s͜͡", callback_data="style+cloud"),
            InlineKeyboardButton("H̆̈ă̈p̆̈p̆̈y̆̈", callback_data="style+happy"),
            InlineKeyboardButton("S̑̈ȃ̈d̑̈", callback_data="style+sad"),
        ],
        [InlineKeyboardButton("ɴᴇxᴛ ➻", callback_data="nxt")],
    ]
    if not cb:
        await m.reply_text(
            m.text, reply_markup=InlineKeyboardMarkup(buttons), quote=True
        )
    else:
        await m.answer()
        await m.message.edit_reply_markup(InlineKeyboardMarkup(buttons))


@abishnoi.on_cb("nxt")
async def nxt(c, m):
    if m.data == "nxt":
        buttons = [
            [
                InlineKeyboardButton("🇸 🇵 🇪 🇨 🇮 🇦 🇱 ", callback_data="style+special"),
                InlineKeyboardButton("🅂🅀🅄🄰🅁🄴🅂", callback_data="style+squares"),
                InlineKeyboardButton(
                    "🆂︎🆀︎🆄︎🅰︎🆁︎🅴︎🆂︎", callback_data="style+squares_bold"
                ),
            ],
            [
                InlineKeyboardButton("ꪖꪀᦔꪖꪶꪊᥴ𝓲ꪖ", callback_data="style+andalucia"),
                InlineKeyboardButton("爪卂几ᘜ卂", callback_data="style+manga"),
                InlineKeyboardButton("S̾t̾i̾n̾k̾y̾", callback_data="style+stinky"),
            ],
            [
                InlineKeyboardButton(
                    "B̥ͦu̥ͦb̥ͦb̥ͦl̥ͦe̥ͦs̥ͦ", callback_data="style+bubbles"
                ),
                InlineKeyboardButton(
                    "U͟n͟d͟e͟r͟l͟i͟n͟e͟", callback_data="style+underline"
                ),
                InlineKeyboardButton("꒒ꍏꀷꌩꌃꀎꁅ", callback_data="style+ladybug"),
            ],
            [
                InlineKeyboardButton("R҉a҉y҉s҉", callback_data="style+rays"),
                InlineKeyboardButton("B҈i҈r҈d҈s҈", callback_data="style+birds"),
                InlineKeyboardButton("S̸l̸a̸s̸h̸", callback_data="style+slash"),
            ],
            [
                InlineKeyboardButton("s⃠t⃠o⃠p⃠", callback_data="style+stop"),
                InlineKeyboardButton(
                    "S̺͆k̺͆y̺͆l̺͆i̺͆n̺͆e̺͆", callback_data="style+skyline"
                ),
                InlineKeyboardButton("A͎r͎r͎o͎w͎s͎", callback_data="style+arrows"),
            ],
            [
                InlineKeyboardButton("ዪሀክቿነ", callback_data="style+qvnes"),
                InlineKeyboardButton("S̶t̶r̶i̶k̶e̶", callback_data="style+strike"),
                InlineKeyboardButton("F༙r༙o༙z༙e༙n༙", callback_data="style+frozen"),
            ],
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="nxt+0")],
        ]
        await m.answer()
        await m.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
    else:
        await style_buttons(c, m, cb=True)


@abishnoi.on_cb("style")
async def style(c, m):
    await m.answer()
    cmd, style = m.data.split("+")

    if style == "andalucia":
        cls = Fonts.andalucia
    elif style == "arrows":
        cls = Fonts.arrows
    elif style == "birds":
        cls = Fonts.birds
    elif style == "bold_cool":
        cls = Fonts.bold_cool
    elif style == "bubbles":
        cls = Fonts.bubbles
    elif style == "circle_dark":
        cls = Fonts.dark_circle
    elif style == "circles":
        cls = Fonts.circles
    elif style == "cloud":
        cls = Fonts.cloud
    elif style == "comic":
        cls = Fonts.comic
    elif style == "cool":
        cls = Fonts.cool
    elif style == "frozen":
        cls = Fonts.frozen
    elif style == "gothic":
        cls = Fonts.gothic
    elif style == "gothic_bolt":
        cls = Fonts.bold_gothic
    elif style == "happy":
        cls = Fonts.happy
    elif style == "ladybug":
        cls = Fonts.ladybug
    elif style == "manga":
        cls = Fonts.manga
    elif style == "outline":
        cls = Fonts.outline
    elif style == "qvnes":
        cls = Fonts.rvnes
    elif style == "rays":
        cls = Fonts.rays
    elif style == "sad":
        cls = Fonts.sad
    elif style == "sans":
        cls = Fonts.san
    elif style == "script":
        cls = Fonts.script
    elif style == "script_bolt":
        cls = Fonts.bold_script
    elif style == "serif":
        cls = Fonts.serief
    elif style == "sim":
        cls = Fonts.sim
    elif style == "skyline":
        cls = Fonts.skyline
    elif style == "slant":
        cls = Fonts.slant
    elif style == "slant_sans":
        cls = Fonts.slant_san
    elif style == "slash":
        cls = Fonts.slash
    elif style == "small_cap":
        cls = Fonts.smallcap
    elif style == "special":
        cls = Fonts.special
    elif style == "squares":
        cls = Fonts.square
    elif style == "squares_bold":
        cls = Fonts.dark_square
    elif style == "stinky":
        cls = Fonts.stinky
    elif style == "stop":
        cls = Fonts.stop
    elif style == "strike":
        cls = Fonts.strike
    elif style == "tiny":
        cls = Fonts.tiny
    elif style == "typewriter":
        cls = Fonts.typewriter
    elif style == "underline":
        cls = Fonts.underline
    new_text = cls(m.message.reply_to_message.text)
    try:
        await m.message.edit_text(new_text, reply_markup=m.message.reply_markup)
    except Exception:
        pass


__mod_name__ = "𝐅ᴏɴᴛs"
