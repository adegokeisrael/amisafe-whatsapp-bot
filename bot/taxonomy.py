"""
AmiSafe harm taxonomy and all bot strings in 9 languages.

Each language entry contains:
  - greeting: first message the bot sends
  - choose_harm: prompt to select harm type
  - harm_types: dict of harm type keys → display label
  - describe_prompt: ask for description
  - evidence_prompt: ask for evidence attachment
  - evidence_types: labels for evidence options
  - disclosure_prompt: ask for disclosure level
  - disclosure_levels: labels for disclosure options
  - confirm_prompt: summary before final submission
  - confirm_yes / confirm_no: confirmation buttons
  - success_message: receipt message with {report_id} placeholder
  - cancel_message: if user cancels
  - help_message: if user types HELP
  - invalid_input: generic invalid input response
  - skip_evidence_prompt: option to skip (not recommended)

Language codes follow ISO 639-1 where available:
  en  — English
  ha  — Hausa
  yo  — Yoruba
  ig  — Igbo
  sw  — Swahili
  am  — Amharic
  so  — Somali
  zu  — Zulu
  pc  — Nigerian Pidgin (no standard ISO code)
"""

LANGUAGE_MENU = """🌍 *AmiSafe — AI Harm Reporter*

Choose your language / Zaɓi yaren ku / Yan ede rẹ / Họn asụsụ gị:

1️⃣  English
2️⃣  Hausa (هَوْسَ)
3️⃣  Yoruba
4️⃣  Igbo
5️⃣  Swahili
6️⃣  Amharic (አማርኛ)
7️⃣  Somali (Soomaali)
8️⃣  Zulu (isiZulu)
9️⃣  Nigerian Pidgin

Reply with a number (1–9)"""

LANGUAGE_CODES = {
    "1": "en",
    "2": "ha",
    "3": "yo",
    "4": "ig",
    "5": "sw",
    "6": "am",
    "7": "so",
    "8": "zu",
    "9": "pc",
}

HARM_TYPE_KEYS = [
    "FAKE_IMAGE_OR_VIDEO",
    "FALSE_INFORMATION",
    "UNFAIR_TREATMENT",
    "HARASSMENT_OR_INTIMIDATION",
    "FINANCIAL_HARM",
    "OTHER",
]

STRINGS = {
    # ─────────────────────────────── ENGLISH ───────────────────────────────
    "en": {
        "greeting": (
            "👋 Welcome to *AmiSafe*.\n\n"
            "This tool lets you report AI-related harm safely and anonymously. "
            "No account or personal information is needed.\n\n"
            "Your report helps researchers, journalists, and regulators understand "
            "AI harms happening in African communities.\n\n"
            "Type *HELP* at any time, or *STOP* to cancel."
        ),
        "choose_harm": (
            "📋 *What type of harm did you experience?*\n\n"
            "1️⃣  Fake image or video (deepfake, AI-generated photo)\n"
            "2️⃣  False information (AI-generated fake news, misinformation)\n"
            "3️⃣  Unfair treatment (AI discriminated against me — hiring, loans, etc.)\n"
            "4️⃣  Harassment or intimidation (AI used to threaten or target me)\n"
            "5️⃣  Financial harm (AI scam, fraud, or financial deception)\n"
            "6️⃣  Other\n\n"
            "Reply with a number (1–6)"
        ),
        "harm_types": {
            "FAKE_IMAGE_OR_VIDEO": "Fake image or video",
            "FALSE_INFORMATION": "False information",
            "UNFAIR_TREATMENT": "Unfair treatment",
            "HARASSMENT_OR_INTIMIDATION": "Harassment or intimidation",
            "FINANCIAL_HARM": "Financial harm",
            "OTHER": "Other",
        },
        "describe_prompt": (
            "📝 *Please describe what happened.*\n\n"
            "In a few sentences: What did you see or experience? "
            "Which platform or app was it on? How did it affect you?\n\n"
            "_(You don't need to include your name or personal details.)_"
        ),
        "evidence_prompt": (
            "📎 *Please attach evidence.*\n\n"
            "Send one of:\n"
            "📸  A screenshot or photo of the harmful content\n"
            "🎤  A voice note describing what you saw\n\n"
            "Evidence makes your report credible and actionable.\n"
            "If you cannot attach evidence now, type *SKIP* — but your report "
            "will carry less weight."
        ),
        "disclosure_prompt": (
            "🔒 *How would you like to share your report?*\n\n"
            "1️⃣  *Private* — stored only on your device. Not shared with anyone.\n"
            "2️⃣  *Anonymous Research* — shared with researchers as anonymous data. "
            "No personal details included.\n"
            "3️⃣  *Verified Partner* — shared with vetted civil society organisations "
            "(e.g. Paradigm Initiative) who may follow up on your report.\n\n"
            "Reply with a number (1–3)"
        ),
        "disclosure_levels": {
            "PRIVATE": "Private",
            "ANONYMOUS_RESEARCH": "Anonymous Research",
            "VERIFIED_PARTNER": "Verified Partner",
        },
        "confirm_prompt": (
            "✅ *Please confirm your report:*\n\n"
            "📌 Harm type: *{harm_type}*\n"
            "📌 Description: _{description}_\n"
            "📌 Evidence: *{evidence_status}*\n"
            "📌 Disclosure: *{disclosure_level}*\n\n"
            "Type *YES* to submit, or *NO* to cancel."
        ),
        "confirm_yes": "YES",
        "confirm_no": "NO",
        "success_message": (
            "✅ *Report submitted. Thank you.*\n\n"
            "Your report ID: `{report_id}`\n\n"
            "Keep this ID — you can use it to update or withdraw your report.\n\n"
            "Your report is now part of AmiSafe's community intelligence database. "
            "Together, these reports help hold AI systems accountable in African communities.\n\n"
            "_AmiSafe — Built for Africa, by Africa._"
        ),
        "private_success_message": (
            "✅ *Report saved privately.*\n\n"
            "Your report ID: `{report_id}`\n\n"
            "This report is stored only within your conversation. "
            "It has not been shared with any organisation.\n\n"
            "You can change the disclosure level at any time by contacting us with your report ID."
        ),
        "cancel_message": "Report cancelled. No data has been stored. Type *START* to begin a new report.",
        "help_message": (
            "ℹ️ *AmiSafe Help*\n\n"
            "AmiSafe lets you report AI-related harms safely and anonymously.\n\n"
            "Commands:\n"
            "• *START* — begin a new report\n"
            "• *STOP* or *CANCEL* — cancel and clear your current session\n"
            "• *SKIP* — skip the evidence step (not recommended)\n"
            "• *HELP* — show this message\n\n"
            "Your phone number is never stored. Reports are encrypted.\n\n"
            "For support: amisafe@example.org"
        ),
        "invalid_input": "I didn't understand that. Please reply with a number from the options above, or type *HELP*.",
        "evidence_received": "📎 Evidence received and secured. ",
        "skip_evidence_warning": (
            "⚠️ You are skipping evidence attachment. "
            "Reports without evidence carry less weight. Continuing..."
        ),
    },

    # ─────────────────────────────── HAUSA ────────────────────────────────
    "ha": {
        "greeting": (
            "👋 Barka da zuwa *AmiSafe*.\n\n"
            "Wannan kayan aiki yana ba ka damar rarraba cutarwa da ke da alaƙa da AI "
            "cikin aminci da asirce. Ba a buƙatar asusun ko bayanin sirri.\n\n"
            "Rahotonka yana taimaka wa masu bincike, 'yan jarida, da masu tsara doka "
            "su fahimci cutarwar AI da ke faruwa a al'ummomin Afirka.\n\n"
            "Rubuta *TAIMAKO* a kowane lokaci, ko *TSAYA* don soke."
        ),
        "choose_harm": (
            "📋 *Wane nau'in cutarwa ka fuskanta?*\n\n"
            "1️⃣  Hoton karya ko bidiyo (deepfake, hoto da AI ya ƙirƙira)\n"
            "2️⃣  Bayanin karya (labarai na karya da AI ya samar)\n"
            "3️⃣  Rashin adalci (AI ya nuna wariya a kaina — aiki, aro, da sauransu)\n"
            "4️⃣  Cin zarafi ko tsoratarwa (an yi amfani da AI don barazana ko kai hari a kaina)\n"
            "5️⃣  Asarar kuɗi (zamba ta AI, yaudara)\n"
            "6️⃣  Wani abu\n\n"
            "Amsa da lamba (1–6)"
        ),
        "harm_types": {
            "FAKE_IMAGE_OR_VIDEO": "Hoton karya ko bidiyo",
            "FALSE_INFORMATION": "Bayanin karya",
            "UNFAIR_TREATMENT": "Rashin adalci",
            "HARASSMENT_OR_INTIMIDATION": "Cin zarafi ko tsoratarwa",
            "FINANCIAL_HARM": "Asarar kuɗi",
            "OTHER": "Wani abu",
        },
        "describe_prompt": (
            "📝 *Da fatan za a bayyana abin da ya faru.*\n\n"
            "A cikin 'yan jimla: Mene ne ka gani ko ka fuskanta? "
            "Wace dandali ko app ce? Ta yaya ya shafe ka?\n\n"
            "_(Ba sai ka haɗa sunanka ko bayanan sirri ba.)_"
        ),
        "evidence_prompt": (
            "📎 *Da fatan za a haɗa shaida.*\n\n"
            "Aika ɗaya daga cikin:\n"
            "📸  Hoton allon ko hoto na abun cutarwa\n"
            "🎤  Saƙon murya yana bayyana abin da ka gani\n\n"
            "Idan ba za ka iya haɗa shaida yanzu ba, rubuta *TSALLAKE*."
        ),
        "disclosure_prompt": (
            "🔒 *Yaya kake son raba rahotonka?*\n\n"
            "1️⃣  *Sirri* — an adana a cikin tattaunawarku kawai.\n"
            "2️⃣  *Bincike na Asirce* — an raba da masu bincike a matsayin bayanai na asirce.\n"
            "3️⃣  *Abokin Tarayya* — an raba da ƙungiyoyin farar hula (misali Paradigm Initiative).\n\n"
            "Amsa da lamba (1–3)"
        ),
        "disclosure_levels": {
            "PRIVATE": "Sirri",
            "ANONYMOUS_RESEARCH": "Bincike na Asirce",
            "VERIFIED_PARTNER": "Abokin Tarayya",
        },
        "confirm_prompt": (
            "✅ *Da fatan za a tabbatar da rahotonka:*\n\n"
            "📌 Nau'in cutarwa: *{harm_type}*\n"
            "📌 Bayani: _{description}_\n"
            "📌 Shaida: *{evidence_status}*\n"
            "📌 Buɗe: *{disclosure_level}*\n\n"
            "Rubuta *I* don aika, ko *A'A* don soke."
        ),
        "confirm_yes": "I",
        "confirm_no": "A'A",
        "success_message": (
            "✅ *An aika rahoton. Na gode.*\n\n"
            "ID na rahotonka: `{report_id}`\n\n"
            "Kiyaye wannan ID — za ka iya amfani da shi don sabunta ko janye rahotonka."
        ),
        "private_success_message": (
            "✅ *An adana rahoton a sirce.*\n\n"
            "ID na rahotonka: `{report_id}`\n\n"
            "Ba a raba wannan rahoto da kowane ƙungiya ba."
        ),
        "cancel_message": "An soke rahoton. Ba a adana bayanai ba. Rubuta *FARA* don fara sabon rahoto.",
        "help_message": (
            "ℹ️ *Taimakon AmiSafe*\n\n"
            "Umarni:\n"
            "• *FARA* — fara sabon rahoto\n"
            "• *TSAYA* ko *SOKE* — soke zaman yanzu\n"
            "• *TSALLAKE* — tsallake matakin shaida\n"
            "• *TAIMAKO* — nuna wannan saƙon\n\n"
            "Ba a adana lambar wayarka ba. Rahotanni ana ɓoye su."
        ),
        "invalid_input": "Ban fahimci wannan ba. Da fatan za a amsa da lamba daga zaɓuɓɓukan da ke sama, ko rubuta *TAIMAKO*.",
        "evidence_received": "📎 An karbi shaida kuma an tsare ta. ",
        "skip_evidence_warning": "⚠️ Kana tsallake haɗa shaida. Rahotanni ba tare da shaida ba suna da ƙarancin nauyi. Ana ci gaba...",
    },

    # ─────────────────────────────── YORUBA ───────────────────────────────
    "yo": {
        "greeting": (
            "👋 Kaabọ si *AmiSafe*.\n\n"
            "Ohun elo yii gba ọ laaye lati ròyin ipalara ti o ni ibatan si AI "
            "ni ailewu ati lainidanimọ. Ko si akọọlẹ tabi alaye ti ara ẹni ti o nilo.\n\n"
            "Ìjábọ rẹ ṣe iranlọwọ fun awọn oniwadi, awọn akọroyin, ati awọn ilana "
            "lati loye ipalara AI ti n ṣẹlẹ ni agbegbe Afirika.\n\n"
            "Tẹ *IRANLỌWỌ* ni akoko eyikeyi, tabi *DẸKUN* lati fagilee."
        ),
        "choose_harm": (
            "📋 *Iru ipalara wo ni o ni iriri?*\n\n"
            "1️⃣  Aworan eke tabi fidio (deepfake, aworan ti AI ṣẹda)\n"
            "2️⃣  Alaye eke (iroyin eke ti AI ṣẹda)\n"
            "3️⃣  Itọju aiṣododo (AI ṣe iyasoto si mi — iṣẹ, awin, ati bẹbẹ lọ)\n"
            "4️⃣  Ipọnju tabi ihalẹ (AI lo lati halẹ tabi fojusi mi)\n"
            "5️⃣  Ipalara owo (jibiti AI, irọ owo)\n"
            "6️⃣  Ohun miiran\n\n"
            "Dahun pẹlu nọmba (1–6)"
        ),
        "harm_types": {
            "FAKE_IMAGE_OR_VIDEO": "Aworan eke tabi fidio",
            "FALSE_INFORMATION": "Alaye eke",
            "UNFAIR_TREATMENT": "Itọju aiṣododo",
            "HARASSMENT_OR_INTIMIDATION": "Ipọnju tabi ihalẹ",
            "FINANCIAL_HARM": "Ipalara owo",
            "OTHER": "Ohun miiran",
        },
        "describe_prompt": (
            "📝 *Jọwọ ṣapejuwe ohun ti o ṣẹlẹ.*\n\n"
            "Ni awọn gbolohun diẹ: Kini o rii tabi ni iriri? "
            "Pẹpẹ tabi app wo ni? Bawo ni o ṣe kan ọ?\n\n"
            "_(O ko nilo lati fi orukọ rẹ tabi alaye ti ara ẹni sii.)_"
        ),
        "evidence_prompt": (
            "📎 *Jọwọ so ẹri pọ.*\n\n"
            "Firanṣẹ ọkan ninu:\n"
            "📸  Aworan iboju tabi fọto ti akoonu ti o le ṣe ipalara\n"
            "🎤  Akọsilẹ ohun ti n ṣapejuwe ohun ti o rii\n\n"
            "Ti o ko ba le so ẹri pọ ni bayi, tẹ *FO*."
        ),
        "disclosure_prompt": (
            "🔒 *Bawo ni o fẹ pin ìjábọ rẹ?*\n\n"
            "1️⃣  *Aṣiri* — ti a fipamọ sinu ibaraẹnisọrọ rẹ nikan.\n"
            "2️⃣  *Iwadii Alainidanimọ* — pin pẹlu awọn oniwadi bi data alainidanimọ.\n"
            "3️⃣  *Alabaṣiṣẹpọ Idaniloju* — pin pẹlu awọn ẹgbẹ awujọ araalu.\n\n"
            "Dahun pẹlu nọmba (1–3)"
        ),
        "disclosure_levels": {
            "PRIVATE": "Aṣiri",
            "ANONYMOUS_RESEARCH": "Iwadii Alainidanimọ",
            "VERIFIED_PARTNER": "Alabaṣiṣẹpọ Idaniloju",
        },
        "confirm_prompt": (
            "✅ *Jọwọ jẹrisi ìjábọ rẹ:*\n\n"
            "📌 Iru ipalara: *{harm_type}*\n"
            "📌 Apejuwe: _{description}_\n"
            "📌 Ẹri: *{evidence_status}*\n"
            "📌 Ifihan: *{disclosure_level}*\n\n"
            "Tẹ *BẸẸNI* lati fi ranṣẹ, tabi *RARA* lati fagilee."
        ),
        "confirm_yes": "BẸẸNI",
        "confirm_no": "RARA",
        "success_message": (
            "✅ *Ìjábọ ti fi ranṣẹ. E dupe.*\n\n"
            "ID ìjábọ rẹ: `{report_id}`\n\n"
            "Pa ID yii mọ — o le lo lati ṣe imudojuiwọn tabi yọ ìjábọ rẹ kuro."
        ),
        "private_success_message": (
            "✅ *Ìjábọ ti fipamọ ni ikọkọ.*\n\n"
            "ID ìjábọ rẹ: `{report_id}`\n\n"
            "A ko pin ìjábọ yii pẹlu eyikeyi ẹgbẹ."
        ),
        "cancel_message": "Ìjábọ ti fagilee. Ko si data ti o fipamọ. Tẹ *BẸRẸ* lati bẹrẹ ìjábọ tuntun.",
        "help_message": (
            "ℹ️ *Iranlọwọ AmiSafe*\n\n"
            "Awọn aṣẹ:\n"
            "• *BẸRẸ* — bẹrẹ ìjábọ tuntun\n"
            "• *DẸKUN* tabi *FAGILEE* — fagilee igba lọwọlọwọ\n"
            "• *FO* — fori igbesẹ ẹri\n"
            "• *IRANLỌWỌ* — ṣafihan ifiranṣẹ yii\n\n"
            "Nọmba foonu rẹ ko fipamọ. Awọn ìjábọ ti fi ẹ̀yà pamọ́."
        ),
        "invalid_input": "Mi o loye iyẹn. Jọwọ dahun pẹlu nọmba lati awọn aṣayan loke, tabi tẹ *IRANLỌWỌ*.",
        "evidence_received": "📎 Ẹri ti gba ati ti fi pamọ. ",
        "skip_evidence_warning": "⚠️ O n fo so ẹri pọ. Awọn ìjábọ laisi ẹri ni iwuwo ti o kere. Tẹsiwaju...",
    },

    # ─────────────────────────────── IGBO ─────────────────────────────────
    "ig": {
        "greeting": (
            "👋 Nnọọ na *AmiSafe*.\n\n"
            "Ngwa a na-enye gị ohere ịkọ maka ihe ize ndụ AI metụtara n'ụzọ nchekwa "
            "na enweghị aha. Achọghị akwụnti ma ọ bụ ozi nkeonwe.\n\n"
            "Akụkọ gị na-enyere ndị ọchụchọ, ndị nta akụkọ, na ụlọ ọrụ ọchị iwu "
            "ike ịghọta mmerụ AI na-eme n'obodo Afrịka.\n\n"
            "Pịa *ENYEMAKA* n'oge ọ bụla, ma ọ bụ *KWỤSỊ* ka ịhapụ."
        ),
        "choose_harm": (
            "📋 *Kedụ ụdị mmerụ i nwetara?*\n\n"
            "1️⃣  Foto ma ọ bụ vidiyo ọghọm (deepfake, foto AI mepụtara)\n"
            "2️⃣  Ozi ụgha (ọchịchọ ụgha AI mepụtara)\n"
            "3️⃣  Ọzụzụ na-ezighi ezi (AI mesoro m ụkpụrụ ọjọọ — ọrụ, mbinye ego, kkk)\n"
            "4️⃣  Ịta aghụghọ ma ọ bụ iyi egwu (ejiri AI iti m egwu ma ọ bụ ịkpagide m)\n"
            "5️⃣  Mmerụ ego (aghụghọ AI, ntụgharị ego)\n"
            "6️⃣  Ihe ọzọ\n\n"
            "Zaghachi na nọmba (1–6)"
        ),
        "harm_types": {
            "FAKE_IMAGE_OR_VIDEO": "Foto ma ọ bụ vidiyo ọghọm",
            "FALSE_INFORMATION": "Ozi ụgha",
            "UNFAIR_TREATMENT": "Ọzụzụ na-ezighi ezi",
            "HARASSMENT_OR_INTIMIDATION": "Ịta aghụghọ ma ọ bụ iyi egwu",
            "FINANCIAL_HARM": "Mmerụ ego",
            "OTHER": "Ihe ọzọ",
        },
        "describe_prompt": (
            "📝 *Biko kọọ ihe mere.*\n\n"
            "N'ahịrịokwu ole na ole: Gịnị ka i hụrụ ma ọ bụ nwetara? "
            "Ohere ma ọ bụ ngwa gịnị ka ọ bụ? Olee otú o metụtara gị?\n\n"
            "_(Ọ dịghị mkpa itinye aha gị ma ọ bụ nkọwa onwe gị.)_"
        ),
        "evidence_prompt": (
            "📎 *Biko tinye ihe akaebe.*\n\n"
            "Zipu otu n'ime:\n"
            "📸  Ụtụ ihuenyo ma ọ bụ foto nke ihe mmerụ\n"
            "🎤  Ndekọ olu na-akọwa ihe i hụrụ\n\n"
            "Ọ bụrụ na ị nweghị ike itinye ihe akaebe ugbu a, pịa *WỤFE*."
        ),
        "disclosure_prompt": (
            "🔒 *Olee otú ị chọrọ ịkekọrịta akụkọ gị?*\n\n"
            "1️⃣  *Nzuzo* — echekwara naanị n'ọgbakọ gị.\n"
            "2️⃣  *Nyocha Enweghị Aha* — kekọrịtara na ndị ọchụchọ dị ka data enweghị aha.\n"
            "3️⃣  *Onye Mmekọ Nkwenye* — kekọrịtara na ndị otu obodo mmadụ.\n\n"
            "Zaghachi na nọmba (1–3)"
        ),
        "disclosure_levels": {
            "PRIVATE": "Nzuzo",
            "ANONYMOUS_RESEARCH": "Nyocha Enweghị Aha",
            "VERIFIED_PARTNER": "Onye Mmekọ Nkwenye",
        },
        "confirm_prompt": (
            "✅ *Biko kwenye akụkọ gị:*\n\n"
            "📌 Ụdị mmerụ: *{harm_type}*\n"
            "📌 Nkọwa: _{description}_\n"
            "📌 Ihe akaebe: *{evidence_status}*\n"
            "📌 Ikpughe: *{disclosure_level}*\n\n"
            "Pịa *EE* ka iziga, ma ọ bụ *MBĀ* ka ihapụ."
        ),
        "confirm_yes": "EE",
        "confirm_no": "MBĀ",
        "success_message": (
            "✅ *Ezitere akụkọ. Daalụ.*\n\n"
            "ID akụkọ gị: `{report_id}`\n\n"
            "Chekwaa ID a — ị nwere ike iji ya melite ma ọ bụ weghara akụkọ gị."
        ),
        "private_success_message": (
            "✅ *Echekwara akụkọ n'ime nzuzo.*\n\n"
            "ID akụkọ gị: `{report_id}`\n\n"
            "Akekọrịtaghị akụkọ a na otu ọ bụla."
        ),
        "cancel_message": "Ehichapụrụ akụkọ. Echekwaghị ozi ọ bụla. Pịa *BIDO* ka ịmalite akụkọ ọhụrụ.",
        "help_message": (
            "ℹ️ *Enyemaka AmiSafe*\n\n"
            "Iwu:\n"
            "• *BIDO* — bido akụkọ ọhụrụ\n"
            "• *KWỤSỊ* ma ọ bụ *HAPỤ* — hapụ nnọkọ ugbu a\n"
            "• *WỤFE* — wụfe nzọụkwụ ihe akaebe\n"
            "• *ENYEMAKA* — gosi ozi a\n\n"
            "Echekwaghị nọmba ekwentị gị. Echebere akụkọ."
        ),
        "invalid_input": "Aghọtabeghị nke ahụ. Biko zaghachi na nọmba site n'nhọrọ ndị dị n'elu, ma ọ bụ pịa *ENYEMAKA*.",
        "evidence_received": "📎 Natara ihe akaebe ma chekwaa ya. ",
        "skip_evidence_warning": "⚠️ I na-awụfe itinye ihe akaebe. Akụkọ enweghị ihe akaebe na-adị n'ụkwụ dị ala. Na-aga n'ihu...",
    },

    # ─────────────────────────────── SWAHILI ──────────────────────────────
    "sw": {
        "greeting": (
            "👋 Karibu *AmiSafe*.\n\n"
            "Zana hii inakuruhusu kuripoti madhara yanayohusiana na AI "
            "kwa usalama na bila kutambuliwa. Akaunti au taarifa za kibinafsi hazihitajiki.\n\n"
            "Ripoti yako husaidia watafiti, waandishi wa habari, na mamlaka kuelewa "
            "madhara ya AI yanayotokea katika jamii za Afrika.\n\n"
            "Andika *MSAADA* wakati wowote, au *SIMAMA* kufuta."
        ),
        "choose_harm": (
            "📋 *Ni aina gani ya madhara uliyopitia?*\n\n"
            "1️⃣  Picha au video bandia (deepfake, picha iliyotengenezwa na AI)\n"
            "2️⃣  Habari za uongo (habari za uongo zilizoundwa na AI)\n"
            "3️⃣  Matibabu yasiyokuwa ya haki (AI ilinibagua — kazi, mkopo, n.k.)\n"
            "4️⃣  Unyanyasaji au vitisho (AI ilitumika kunisumbua au kunilengea)\n"
            "5️⃣  Madhara ya kifedha (ulaghai wa AI, udanganyifu wa pesa)\n"
            "6️⃣  Kingine\n\n"
            "Jibu kwa nambari (1–6)"
        ),
        "harm_types": {
            "FAKE_IMAGE_OR_VIDEO": "Picha au video bandia",
            "FALSE_INFORMATION": "Habari za uongo",
            "UNFAIR_TREATMENT": "Matibabu yasiyokuwa ya haki",
            "HARASSMENT_OR_INTIMIDATION": "Unyanyasaji au vitisho",
            "FINANCIAL_HARM": "Madhara ya kifedha",
            "OTHER": "Kingine",
        },
        "describe_prompt": (
            "📝 *Tafadhali eleza kilichotokea.*\n\n"
            "Kwa maneno machache: Uliona au ulipitia nini? "
            "Ilikuwa kwenye jukwaa au programu gani? Ilikuathirije?\n\n"
            "_(Huhitaji kujumuisha jina lako au maelezo ya kibinafsi.)_"
        ),
        "evidence_prompt": (
            "📎 *Tafadhali ambatanisha ushahidi.*\n\n"
            "Tuma moja ya:\n"
            "📸  Picha ya skrini au picha ya maudhui hatari\n"
            "🎤  Ujumbe wa sauti unaelezea ulichoona\n\n"
            "Ikiwa huwezi kuambatanisha ushahidi sasa, andika *RUKA*."
        ),
        "disclosure_prompt": (
            "🔒 *Ungependa kushiriki ripoti yako vipi?*\n\n"
            "1️⃣  *Faragha* — imehifadhiwa katika mazungumzo yako tu.\n"
            "2️⃣  *Utafiti wa Bila Jina* — imeshirikiwa na watafiti kama data bila jina.\n"
            "3️⃣  *Mshirika Aliyehakikishwa* — imeshirikiwa na mashirika ya kiraia.\n\n"
            "Jibu kwa nambari (1–3)"
        ),
        "disclosure_levels": {
            "PRIVATE": "Faragha",
            "ANONYMOUS_RESEARCH": "Utafiti wa Bila Jina",
            "VERIFIED_PARTNER": "Mshirika Aliyehakikishwa",
        },
        "confirm_prompt": (
            "✅ *Tafadhali thibitisha ripoti yako:*\n\n"
            "📌 Aina ya madhara: *{harm_type}*\n"
            "📌 Maelezo: _{description}_\n"
            "📌 Ushahidi: *{evidence_status}*\n"
            "📌 Ufafanuzi: *{disclosure_level}*\n\n"
            "Andika *NDIO* kutuma, au *HAPANA* kufuta."
        ),
        "confirm_yes": "NDIO",
        "confirm_no": "HAPANA",
        "success_message": (
            "✅ *Ripoti imetumwa. Asante.*\n\n"
            "ID ya ripoti yako: `{report_id}`\n\n"
            "Hifadhi ID hii — unaweza kuitumia kusasisha au kuondoa ripoti yako."
        ),
        "private_success_message": (
            "✅ *Ripoti imehifadhiwa kwa faragha.*\n\n"
            "ID ya ripoti yako: `{report_id}`\n\n"
            "Ripoti hii haijashirikiwa na shirika lolote."
        ),
        "cancel_message": "Ripoti imefutwa. Hakuna data iliyohifadhiwa. Andika *ANZA* kuanzisha ripoti mpya.",
        "help_message": (
            "ℹ️ *Msaada wa AmiSafe*\n\n"
            "Amri:\n"
            "• *ANZA* — anza ripoti mpya\n"
            "• *SIMAMA* au *FUTA* — futa kikao cha sasa\n"
            "• *RUKA* — ruka hatua ya ushahidi\n"
            "• *MSAADA* — onyesha ujumbe huu\n\n"
            "Nambari yako ya simu haihifadhiwi. Ripoti zimesimbwa."
        ),
        "invalid_input": "Sikuelewa hiyo. Tafadhali jibu kwa nambari kutoka kwa chaguzi hapo juu, au andika *MSAADA*.",
        "evidence_received": "📎 Ushahidi umepokelewa na kuhifadhiwa kwa usalama. ",
        "skip_evidence_warning": "⚠️ Unaruka kuambatanisha ushahidi. Ripoti bila ushahidi zina uzito mdogo. Inaendelea...",
    },

    # ─────────────────────────────── AMHARIC ──────────────────────────────
    "am": {
        "greeting": (
            "👋 እንኳን ወደ *AmiSafe* በደህና መጡ።\n\n"
            "ይህ መሣሪያ ከ AI ጋር ተያያዥነት ያለው ጉዳትን በደህና እና ሳይታወቁ ሪፖርት "
            "እንዲያደርጉ ያስችልዎታል። ምንም መለያ ወይም የግል መረጃ አያስፈልግም።\n\n"
            "ሪፖርትዎ ተመራማሪዎች፣ ጋዜጠኞች እና ቁጥጥር ባለሥልጣናት "
            "በአፍሪካ ማህበረሰቦች ውስጥ ያሉ AI ጉዳቶችን እንዲረዱ ይረዳቸዋል።\n\n"
            "ለእርዳታ *እርዳታ* ብለው ይፃፉ፣ ወይም ለመሰረዝ *ቆም* ይፃፉ።"
        ),
        "choose_harm": (
            "📋 *ምን አይነት ጉዳት አጋጠምዎ?*\n\n"
            "1️⃣  ሐሰተኛ ምስል ወይም ቪዲዮ (deepfake፣ AI የፈጠረ ፎቶ)\n"
            "2️⃣  ሐሰተኛ መረጃ (AI የፈጠረ ሐሰተኛ ዜና)\n"
            "3️⃣  ኢፍትሃዊ አያያዝ (AI አድልዎ አሳየ — ሥራ፣ ብድር፣ ወዘተ)\n"
            "4️⃣  ትንኮሳ ወይም ማስፈራሪያ (AI ለማስፈራራት ወይም ለማነጣጠር ጥቅም ላይ ዋለ)\n"
            "5️⃣  የገንዘብ ጉዳት (የ AI ማጭበርበር፣ ማታለል)\n"
            "6️⃣  ሌላ\n\n"
            "በቁጥር መልስ ይስጡ (1–6)"
        ),
        "harm_types": {
            "FAKE_IMAGE_OR_VIDEO": "ሐሰተኛ ምስል ወይም ቪዲዮ",
            "FALSE_INFORMATION": "ሐሰተኛ መረጃ",
            "UNFAIR_TREATMENT": "ኢፍትሃዊ አያያዝ",
            "HARASSMENT_OR_INTIMIDATION": "ትንኮሳ ወይም ማስፈራሪያ",
            "FINANCIAL_HARM": "የገንዘብ ጉዳት",
            "OTHER": "ሌላ",
        },
        "describe_prompt": (
            "📝 *እባኮትን የሆነውን ይግለጹ።*\n\n"
            "በጥቂት ዓረፍተ ነገሮች ውስጥ: ምን አዩ ወይም ምን አጋጠምዎ? "
            "ምን ዓይነት መድረክ ወይም መተግበሪያ ነበር? ምን ያህል ጎዳዎ?\n\n"
            "_(ስምዎን ወይም የግል ዝርዝሮቻቸውን ማካተት አያስፈልግም።)_"
        ),
        "evidence_prompt": (
            "📎 *እባኮትን ማስረጃ ያያዙ።*\n\n"
            "ከሚከተሉት አንዱን ይላኩ:\n"
            "📸  የጎዳ ይዘቱ የስክሪን ሾት ወይም ፎቶ\n"
            "🎤  ያዩትን የሚገልጽ የድምፅ ማስታወሻ\n\n"
            "አሁን ማስረጃ ማያያዝ ካልቻሉ *ዝለሉ* ብለው ይፃፉ።"
        ),
        "disclosure_prompt": (
            "🔒 *ሪፖርትዎን እንዴት ማጋራት ይፈልጋሉ?*\n\n"
            "1️⃣  *ሚስጥራዊ* — ሪፖርቱ ሚስጥራዊ ሆኖ ይቀመጣል።\n"
            "2️⃣  *ስም-አልባ ምርምር* — ስም-አልባ ውሂብ ሆኖ ከተመራማሪዎች ጋር ይጋራል።\n"
            "3️⃣  *ተረጋጋጭ አጋር* — ከሲቪል ማህበረሰብ ድርጅቶች ጋር ይጋራል።\n\n"
            "በቁጥር መልስ ይስጡ (1–3)"
        ),
        "disclosure_levels": {
            "PRIVATE": "ሚስጥራዊ",
            "ANONYMOUS_RESEARCH": "ስም-አልባ ምርምር",
            "VERIFIED_PARTNER": "ተረጋጋጭ አጋር",
        },
        "confirm_prompt": (
            "✅ *እባኮትን ሪፖርትዎን ያረጋግጡ:*\n\n"
            "📌 የጉዳት አይነት: *{harm_type}*\n"
            "📌 ገለፃ: _{description}_\n"
            "📌 ማስረጃ: *{evidence_status}*\n"
            "📌 ይፋ ማድረጊያ: *{disclosure_level}*\n\n"
            "ለመላክ *አዎ* ይፃፉ፣ ወይም ለመሰረዝ *አይ* ይፃፉ።"
        ),
        "confirm_yes": "አዎ",
        "confirm_no": "አይ",
        "success_message": (
            "✅ *ሪፖርቱ ተላከ። አመሰግናለሁ።*\n\n"
            "የሪፖርት ID: `{report_id}`\n\n"
            "ይህን ID ያስቀምጡ — ሪፖርትዎን ለማዘመን ወይም ለማስወገድ ሊጠቀሙበት ይችላሉ።"
        ),
        "private_success_message": (
            "✅ *ሪፖርቱ በሚስጥር ተቀምጧል።*\n\n"
            "የሪፖርት ID: `{report_id}`\n\n"
            "ይህ ሪፖርት ከምንም ድርጅት ጋር አልተጋራም።"
        ),
        "cancel_message": "ሪፖርቱ ተሰረዘ። ምንም ውሂብ አልተቀመጠም። አዲስ ሪፖርት ለመጀመር *ጀምር* ብለው ይፃፉ።",
        "help_message": (
            "ℹ️ *የ AmiSafe እርዳታ*\n\n"
            "ትዕዛዞች:\n"
            "• *ጀምር* — አዲስ ሪፖርት ጀምር\n"
            "• *ቆም* ወይም *ሰርዝ* — አሁን ያለውን ክፍለ ጊዜ ሰርዝ\n"
            "• *ዝለሉ* — የማስረጃ ደረጃን ዝለሉ\n"
            "• *እርዳታ* — ይህን ማስታወሻ አሳይ\n\n"
            "የስልክ ቁጥርዎ አይቀመጥም። ሪፖርቶች ተመሰጠሩ።"
        ),
        "invalid_input": "ያንን አልተረዳሁም። እባኮትን ከላይ ካሉት ምርጫዎች ቁጥር ይጠቀሙ፣ ወይም *እርዳታ* ብለው ይፃፉ።",
        "evidence_received": "📎 ማስረጃ ተቀብሏል እና ተጠብቋል። ",
        "skip_evidence_warning": "⚠️ ማስረጃ ሳያያዙ እያለፉ ነው። ያለ ማስረጃ ሪፖርቶች ያነሰ ክብደት አላቸው። እየቀጠለ...",
    },

    # ─────────────────────────────── SOMALI ───────────────────────────────
    "so": {
        "greeting": (
            "👋 Ku soo dhawow *AmiSafe*.\n\n"
            "Aaladdan waxa ay kugu oggolaanaysaa inaad ku warbixi kartid waxyeelada "
            "la xiriirta AI si ammaan ah oo cidna kugu garan wayso. "
            "Xisaab ama macluumaad shakhsi ah looma baahna.\n\n"
            "Warbiximahaagu waxa ay ku caawisaa cilmi-baarayaasha, wariyayaasha, iyo "
            "hay'adaha xukuumadda inay fahmaan waxyeelada AI ee ka dhacaysa bulshada Afrika.\n\n"
            "Qor *CAAWIN* waqti kasta, ama *JOOJI* si aad u joojiso."
        ),
        "choose_harm": (
            "📋 *Nooca waxyeelada kee ayaad la kulmay?*\n\n"
            "1️⃣  Sawir ama muuqaal been ah (deepfake, sawir AI sameeya)\n"
            "2️⃣  Macluumaad been ah (wararka been ah ee AI sameeya)\n"
            "3️⃣  Dil been ah (AI ayaa i kala soocay — shaqo, amaah, iwm)\n"
            "4️⃣  Xasuuq ama hanaansho (AI ayaa loo isticmaalay inay i hanaanshadaan)\n"
            "5️⃣  Waxyeelada dhaqaale (khiyaamo AI, tartiib lacageed)\n"
            "6️⃣  Kale\n\n"
            "Ka jawaab nambar (1–6)"
        ),
        "harm_types": {
            "FAKE_IMAGE_OR_VIDEO": "Sawir ama muuqaal been ah",
            "FALSE_INFORMATION": "Macluumaad been ah",
            "UNFAIR_TREATMENT": "Dil been ah",
            "HARASSMENT_OR_INTIMIDATION": "Xasuuq ama hanaansho",
            "FINANCIAL_HARM": "Waxyeelada dhaqaale",
            "OTHER": "Kale",
        },
        "describe_prompt": (
            "📝 *Fadlan sharax waxa dhacay.*\n\n"
            "Dhowr jumle: Maxaad aragtay ama la kulmay? "
            "Maxay ahayd madal ama app-ka? Sideed kuugu dhiifsatay?\n\n"
            "_(Magacaaga ama macluumaadka shakhsiyadeed kuma darsan kartid.)_"
        ),
        "evidence_prompt": (
            "📎 *Fadlan ku xidh caddayn.*\n\n"
            "Dir mid ka mid ah:\n"
            "📸  Sawir shaasha ama sawir waxyeelada\n"
            "🎤  Xogta codka oo sharaxaysa waxa aad aragtay\n\n"
            "Haddaad hadda caddayn ku xidhi karin, qor *UBO*."
        ),
        "disclosure_prompt": (
            "🔒 *Sideed jeceshahay inaad wadaagto warbiximahaaga?*\n\n"
            "1️⃣  *Sirta* — waxaa lagu kaydiyaa wadahadashada kaliya.\n"
            "2️⃣  *Cilmi-baaris Aan Magac Lahayn* — cilmi-baarayaasha la wadaagaa xogta.\n"
            "3️⃣  *Kaalmada la Xaqiijiyay* — hay'adaha bulshada rayidka ah la wadaagaa.\n\n"
            "Ka jawaab nambar (1–3)"
        ),
        "disclosure_levels": {
            "PRIVATE": "Sirta",
            "ANONYMOUS_RESEARCH": "Cilmi-baaris Aan Magac Lahayn",
            "VERIFIED_PARTNER": "Kaalmada la Xaqiijiyay",
        },
        "confirm_prompt": (
            "✅ *Fadlan xaqiiji warbiximahaaga:*\n\n"
            "📌 Nooca waxyeelada: *{harm_type}*\n"
            "📌 Sharaxaad: _{description}_\n"
            "📌 Caddayn: *{evidence_status}*\n"
            "📌 Muujinta: *{disclosure_level}*\n\n"
            "Qor *HEE* si aad u dirto, ama *MAYA* si aad u joojisto."
        ),
        "confirm_yes": "HEE",
        "confirm_no": "MAYA",
        "success_message": (
            "✅ *Warbiximaha waa la diray. Mahadsanid.*\n\n"
            "ID warbiximahaaga: `{report_id}`\n\n"
            "ID-ga hay — waad isticmaali kartaa si aad u cusbooneysiiso ama u beddesho."
        ),
        "private_success_message": (
            "✅ *Warbiximaha waa lagu kaydiyay sirta.*\n\n"
            "ID warbiximahaaga: `{report_id}`\n\n"
            "Warbiximahaan laguma wadaageen hay'ad kasta."
        ),
        "cancel_message": "Warbiximaha waa la joojiyay. Xog laguma kaydinin. Qor *BILOW* si aad u bilowdo warbixi cusub.",
        "help_message": (
            "ℹ️ *Caawinada AmiSafe*\n\n"
            "Amarrada:\n"
            "• *BILOW* — bilow warbixi cusub\n"
            "• *JOOJI* ama *BAADIL* — jooji xaaladda hadda\n"
            "• *UBO* — ka bood tallaabooyinka caddaynta\n"
            "• *CAAWIN* — muuji fariintaan\n\n"
            "Lambarka taleefankaaga laguma kaydiyee. Warbiximaha waa la gufiyay."
        ),
        "invalid_input": "Taas ma fahmin. Fadlan ka jawaab nambar xulashooyinka kore, ama qor *CAAWIN*.",
        "evidence_received": "📎 Caddaynta waa la helay oo lagu ammaanay. ",
        "skip_evidence_warning": "⚠️ Waad ka booday xidida caddaynta. Warbiximaha aan caddayn lahayn miisaan yaraan. Waxay sii socotaa...",
    },

    # ─────────────────────────────── ZULU ─────────────────────────────────
    "zu": {
        "greeting": (
            "👋 Sawubona, wamukelekile ku-*AmiSafe*.\n\n"
            "Ithuluzi leli likuvumela ukuba ubike ukulimala okuhlobene ne-AI "
            "ngokuphepha nangaphandle kokudalulwa. Akudingeki i-akhawunti noma ulwazi lomuntu siqu.\n\n"
            "Umbiko wakho usiza abacwaningi, abahleli bamaphephandaba, nezisimamisi "
            "ukuqonda ukulimala kwe-AI okwenzeka emiphakathini yase-Afrika.\n\n"
            "Bhala *USIZO* nganoma yisiphi isikhathi, noma *MISA* ukukhansela."
        ),
        "choose_harm": (
            "📋 *Yiluphi uhlobo lokulimala owazizwa ulona?*\n\n"
            "1️⃣  Isithombe noma ividiyo esamanga (deepfake, isithombe esenziwe yi-AI)\n"
            "2️⃣  Ulwazi olwamanga (izindaba zamanga ezenziwe yi-AI)\n"
            "3️⃣  Ukuphathwa ngokungafanele (i-AI yangihlukumeza — umsebenzi, isikweletu, njll.)\n"
            "4️⃣  Ukuhlukunyezwa noma ukusatshiswa (i-AI yasetshenziswa ukungihlukumeza)\n"
            "5️⃣  Ukulimala kwezezimali (inkohliso ye-AI, ukukhohlisa)\n"
            "6️⃣  Okunye\n\n"
            "Phendula ngenombolo (1–6)"
        ),
        "harm_types": {
            "FAKE_IMAGE_OR_VIDEO": "Isithombe noma ividiyo esamanga",
            "FALSE_INFORMATION": "Ulwazi olwamanga",
            "UNFAIR_TREATMENT": "Ukuphathwa ngokungafanele",
            "HARASSMENT_OR_INTIMIDATION": "Ukuhlukunyezwa noma ukusatshiswa",
            "FINANCIAL_HARM": "Ukulimala kwezezimali",
            "OTHER": "Okunye",
        },
        "describe_prompt": (
            "📝 *Sicela uchaze okwenzekile.*\n\n"
            "Ngezimusho ezimbalwa: Uboneni noma wazizwani? "
            "Kwakuyi-platform noma i-app yani? Zakuthinta kanjani?\n\n"
            "_(Akudingeki ufake igama lakho noma imininingwane yomuntu siqu.)_"
        ),
        "evidence_prompt": (
            "📎 *Sicela ulaxe ubufakazi.*\n\n"
            "Thumela enye yalezi:\n"
            "📸  Isithombe se-screen noma isithombe sokuqukethwe okulimaza\n"
            "🎤  Umlayezo wezwi ochaziwe ukulimala okubonile\n\n"
            "Uma ungakwazi ukulaxa ubufakazi manje, bhala *YEQA*."
        ),
        "disclosure_prompt": (
            "🔒 *Ungathanda kanjani ukwabelana ngombiko wakho?*\n\n"
            "1️⃣  *Imfihlo* — igcinwe engxoxweni yakho kuphela.\n"
            "2️⃣  *Ucwaningo Olungaziwa* — wabelanwe nabacwaningi njengolwazi olungaziwa.\n"
            "3️⃣  *Umlingani Oshayile* — wabelanwe nezinhlangano zomphakathi wezikhaya.\n\n"
            "Phendula ngenombolo (1–3)"
        ),
        "disclosure_levels": {
            "PRIVATE": "Imfihlo",
            "ANONYMOUS_RESEARCH": "Ucwaningo Olungaziwa",
            "VERIFIED_PARTNER": "Umlingani Oshayile",
        },
        "confirm_prompt": (
            "✅ *Sicela uqinisekise umbiko wakho:*\n\n"
            "📌 Uhlobo lokulimala: *{harm_type}*\n"
            "📌 Incazelo: _{description}_\n"
            "📌 Ubufakazi: *{evidence_status}*\n"
            "📌 Ukudalula: *{disclosure_level}*\n\n"
            "Bhala *YEBO* ukuthumela, noma *CHA* ukukhansela."
        ),
        "confirm_yes": "YEBO",
        "confirm_no": "CHA",
        "success_message": (
            "✅ *Umbiko uthunywe. Ngiyabonga.*\n\n"
            "I-ID yombiko wakho: `{report_id}`\n\n"
            "Gcina le-ID — ungayisebenzisa ukuphinde ushintshe noma ususe umbiko wakho."
        ),
        "private_success_message": (
            "✅ *Umbiko ugcinwe ngemfihlo.*\n\n"
            "I-ID yombiko wakho: `{report_id}`\n\n"
            "Lo mbiko awabelanwanga nayo neyiphi inhlangano."
        ),
        "cancel_message": "Umbiko ukhansele. Akukho datha egciniwe. Bhala *QALA* ukuqala umbiko omusha.",
        "help_message": (
            "ℹ️ *Usizo lwe-AmiSafe*\n\n"
            "Imiyalo:\n"
            "• *QALA* — qala umbiko omusha\n"
            "• *MISA* noma *KHANSELA* — khansela iseshini yamanje\n"
            "• *YEQA* — yeqa isigaba sobufakazi\n"
            "• *USIZO* — bonisa lo mlayezo\n\n"
            "Inombolo yakho yocingo ayigcinwa. Imibiko ibethelelwe."
        ),
        "invalid_input": "Angizwanga lokho. Sicela uphendule ngenombolo ezinketho ezingenhla, noma ubhale *USIZO*.",
        "evidence_received": "📎 Ubufakazi bumukelwe futhi buphephile. ",
        "skip_evidence_warning": "⚠️ Uyeqa ukulaxa ubufakazi. Imibiko engenabo ubufakazi inesilinganiso esiphansi. Iyaqhubeka...",
    },

    # ───────────────────────── NIGERIAN PIDGIN ────────────────────────────
    "pc": {
        "greeting": (
            "👋 Welcome to *AmiSafe*.\n\n"
            "Dis tool go let you report AI wahala wey happen to you, "
            "safe and nobody go know say na you. You no need account or any personal info.\n\n"
            "Your report go help researchers, journalists, and government people "
            "understand wetin AI dey do to African communities.\n\n"
            "Type *HELP* anytime, or *STOP* to cancel."
        ),
        "choose_harm": (
            "📋 *Wetin kind wahala you experience?*\n\n"
            "1️⃣  Fake picture or video (deepfake, AI-generated picture)\n"
            "2️⃣  False information (AI-generated fake news)\n"
            "3️⃣  Unfair treatment (AI discriminate against me — job, loan, etc.)\n"
            "4️⃣  Harassment or threat (person use AI to disturb or target me)\n"
            "5️⃣  Money wahala (AI scam, financial fraud)\n"
            "6️⃣  Something else\n\n"
            "Reply with number (1–6)"
        ),
        "harm_types": {
            "FAKE_IMAGE_OR_VIDEO": "Fake picture or video",
            "FALSE_INFORMATION": "False information",
            "UNFAIR_TREATMENT": "Unfair treatment",
            "HARASSMENT_OR_INTIMIDATION": "Harassment or threat",
            "FINANCIAL_HARM": "Money wahala",
            "OTHER": "Something else",
        },
        "describe_prompt": (
            "📝 *Abeg describe wetin happen.*\n\n"
            "For few sentences: Wetin you see or experience? "
            "Which platform or app e be? How e affect you?\n\n"
            "_(You no need put your name or personal details.)_"
        ),
        "evidence_prompt": (
            "📎 *Abeg attach evidence.*\n\n"
            "Send one of:\n"
            "📸  Screenshot or photo of the harmful content\n"
            "🎤  Voice note describing wetin you see\n\n"
            "If you no fit attach evidence now, type *SKIP*."
        ),
        "disclosure_prompt": (
            "🔒 *How you wan share your report?*\n\n"
            "1️⃣  *Private* — only saved in your conversation. Nobody go see am.\n"
            "2️⃣  *Anonymous Research* — share with researchers as anonymous data.\n"
            "3️⃣  *Verified Partner* — share with civil society orgs (like Paradigm Initiative).\n\n"
            "Reply with number (1–3)"
        ),
        "disclosure_levels": {
            "PRIVATE": "Private",
            "ANONYMOUS_RESEARCH": "Anonymous Research",
            "VERIFIED_PARTNER": "Verified Partner",
        },
        "confirm_prompt": (
            "✅ *Abeg confirm your report:*\n\n"
            "📌 Wahala type: *{harm_type}*\n"
            "📌 Description: _{description}_\n"
            "📌 Evidence: *{evidence_status}*\n"
            "📌 Sharing: *{disclosure_level}*\n\n"
            "Type *YES* to submit, or *NO* to cancel."
        ),
        "confirm_yes": "YES",
        "confirm_no": "NO",
        "success_message": (
            "✅ *Report don land. Thank you.*\n\n"
            "Your report ID: `{report_id}`\n\n"
            "Keep this ID — you fit use am to update or remove your report.\n\n"
            "Your report don enter AmiSafe community database. "
            "All these reports together dey help hold AI accountable for African communities.\n\n"
            "_AmiSafe — Built for Africa, by Africa._"
        ),
        "private_success_message": (
            "✅ *Report don save private.*\n\n"
            "Your report ID: `{report_id}`\n\n"
            "This report no share with any organisation."
        ),
        "cancel_message": "Report cancelled. No data saved. Type *START* to begin new report.",
        "help_message": (
            "ℹ️ *AmiSafe Help*\n\n"
            "Commands:\n"
            "• *START* — begin new report\n"
            "• *STOP* or *CANCEL* — cancel current session\n"
            "• *SKIP* — skip evidence step\n"
            "• *HELP* — show this message\n\n"
            "Your phone number no dey stored. Reports dey encrypted."
        ),
        "invalid_input": "I no understand that. Abeg reply with number from the options above, or type *HELP*.",
        "evidence_received": "📎 Evidence received and secured. ",
        "skip_evidence_warning": "⚠️ You dey skip evidence attachment. Reports without evidence carry less weight. Continuing...",
    },
}


def get_strings(language_code: str) -> dict:
    """Return strings for a given language, falling back to English."""
    return STRINGS.get(language_code, STRINGS["en"])


def get_harm_type_label(harm_type: str, language_code: str) -> str:
    strings = get_strings(language_code)
    return strings["harm_types"].get(harm_type, harm_type.replace("_", " ").title())


def get_disclosure_label(disclosure_level: str, language_code: str) -> str:
    strings = get_strings(language_code)
    return strings["disclosure_levels"].get(disclosure_level, disclosure_level)
