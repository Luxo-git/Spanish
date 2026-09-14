#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entraînement à la conjugaison espagnole — version graphique (Tkinter)
=======================================================================
Thème visuel « nature » (vert kaki / marron), navigation par un vrai menu
principal avec trois boutons centrés :
  - 🥾 Jeu de conjugaison : entraînement chronométré (60s), avec filtre de
    temps et mode "toutes les personnes"
  - 🌲 Cours : rappel des règles de formation, exemples et verbes
    irréguliers pour le présent, l'imparfait et le passé simple
  - 🗣️ Traduction : traduire des phrases générées par l'application

Lance le script avec :  python3 entrainement_conjugaison_gui.py
(Tkinter est inclus dans l'installation standard de Python)

Note : les « images issues de la nature » sont représentées par des emoji
(🏔️ 🌲 🪨 🫐 🏞️ …) plutôt que des fichiers image, afin que ce script reste
un fichier Python unique et portable, sans dépendance à des images externes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import re
import sys
import os
import unicodedata


def resource_path(relative_path):
    """Retourne le chemin d'une ressource, que le script tourne en direct
    ou packagé en exécutable (PyInstaller)."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# ---------------------------------------------------------------------------
# Données de conjugaison (utilisées par le jeu)
# ---------------------------------------------------------------------------

PRONOMS = ["yo", "tú", "él/ella/Ud.", "nosotros", "vosotros", "ellos/Uds."]
TEMPS = ["présent", "imparfait", "passé simple"]

REGULAR_VERBS = [
    "hablar", "estudiar", "trabajar", "viajar", "comprar", "cantar", "bailar", "caminar",
    "comer", "aprender", "vender", "deber", "correr",
    "vivir", "escribir", "abrir", "decidir", "asistir",
]

IRREGULAR_VERBS = {
    "ser": {
        "présent": ["soy", "eres", "es", "somos", "sois", "son"],
        "imparfait": ["era", "eras", "era", "éramos", "erais", "eran"],
        "passé simple": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"],
    },
    "estar": {
        "présent": ["estoy", "estás", "está", "estamos", "estáis", "están"],
        "passé simple": ["estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron"],
    },
    "tener": {
        "présent": ["tengo", "tienes", "tiene", "tenemos", "tenéis", "tienen"],
        "passé simple": ["tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron"],
    },
    "ir": {
        "présent": ["voy", "vas", "va", "vamos", "vais", "van"],
        "imparfait": ["iba", "ibas", "iba", "íbamos", "ibais", "iban"],
        "passé simple": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"],
    },
    "hacer": {
        "présent": ["hago", "haces", "hace", "hacemos", "hacéis", "hacen"],
        "passé simple": ["hice", "hiciste", "hizo", "hicimos", "hicisteis", "hicieron"],
    },
    "poder": {
        "présent": ["puedo", "puedes", "puede", "podemos", "podéis", "pueden"],
        "passé simple": ["pude", "pudiste", "pudo", "pudimos", "pudisteis", "pudieron"],
    },
    "querer": {
        "présent": ["quiero", "quieres", "quiere", "queremos", "queréis", "quieren"],
        "passé simple": ["quise", "quisiste", "quiso", "quisimos", "quisisteis", "quisieron"],
    },
    "decir": {
        "présent": ["digo", "dices", "dice", "decimos", "decís", "dicen"],
        "passé simple": ["dije", "dijiste", "dijo", "dijimos", "dijisteis", "dijeron"],
    },
    "venir": {
        "présent": ["vengo", "vienes", "viene", "venimos", "venís", "vienen"],
        "passé simple": ["vine", "viniste", "vino", "vinimos", "vinisteis", "vinieron"],
    },
    "saber": {
        "présent": ["sé", "sabes", "sabe", "sabemos", "sabéis", "saben"],
        "passé simple": ["supe", "supiste", "supo", "supimos", "supisteis", "supieron"],
    },
    "ver": {
        "imparfait": ["veía", "veías", "veía", "veíamos", "veíais", "veían"],
        "passé simple": ["vi", "viste", "vio", "vimos", "visteis", "vieron"],
    },
    "poner": {
        "passé simple": ["puse", "pusiste", "puso", "pusimos", "pusisteis", "pusieron"],
    },
    "traer": {
        "passé simple": ["traje", "trajiste", "trajo", "trajimos", "trajisteis", "trajeron"],
    },
    "dar": {
        "passé simple": ["di", "diste", "dio", "dimos", "disteis", "dieron"],
    },
}

ALL_VERBS = REGULAR_VERBS + list(IRREGULAR_VERBS.keys())

REGULAR_ENDINGS = {
    "présent": {
        "ar": ["o", "as", "a", "amos", "áis", "an"],
        "er": ["o", "es", "e", "emos", "éis", "en"],
        "ir": ["o", "es", "e", "imos", "ís", "en"],
    },
    "imparfait": {
        "ar": ["aba", "abas", "aba", "ábamos", "abais", "aban"],
        "er": ["ía", "ías", "ía", "íamos", "íais", "ían"],
        "ir": ["ía", "ías", "ía", "íamos", "íais", "ían"],
    },
    "passé simple": {
        "ar": ["é", "aste", "ó", "amos", "asteis", "aron"],
        "er": ["í", "iste", "ió", "imos", "isteis", "ieron"],
        "ir": ["í", "iste", "ió", "imos", "isteis", "ieron"],
    },
}

# ---------------------------------------------------------------------------
# Direction artistique : thème nature — vert kaki & marron
# ---------------------------------------------------------------------------

FONT_FAMILY = "Comic Sans MS"

BG_APP = "#F3ECD9"        # sable clair / parchemin
BG_CARD = "#FFFDF7"       # carte crème, presque blanche
BG_SETTINGS = "#E8E1C8"   # bandeau réglages, kaki très clair
BORDER_SETTINGS = "#C9BE9A"

COL_TEXT = "#3B2F27"      # brun foncé (texte principal)
COL_MUTED = "#7A6A55"     # brun-gris (texte secondaire)
COL_OK = "#4C7A3D"        # vert forêt (bonne réponse)
COL_KO = "#A0522D"        # terre cuite (mauvaise réponse)
COL_STREAK = "#B8860B"    # doré/miel (série)
COL_ACCENT = "#A0522D"    # rouille (mode difficile actif, encarts conseils)

COL_KAKI = "#7D8F5A"          # vert kaki principal (présent)
COL_KAKI_DARK = "#4B5D2A"     # vert olive foncé (titres, boutons menu)
COL_BROWN = "#8B5E3C"         # marron moyen (imparfait)
COL_BROWN_DARK = "#4B3621"    # marron foncé (passé simple, titres)
COL_MOSS = "#5C6B3C"          # vert mousse foncé (onglet traduction)

TENSE_COLORS = {
    "présent": COL_KAKI,
    "imparfait": COL_BROWN,
    "passé simple": COL_BROWN_DARK,
}
TENSE_EMOJI = {
    "présent": "🌲",
    "imparfait": "🏞️",
    "passé simple": "🪨",
}
TENSE_SUBTITLES = {
    "présent": "Presente de indicativo",
    "imparfait": "Pretérito imperfecto",
    "passé simple": "Pretérito indefinido",
}

TRAD_COLOR = COL_MOSS
TRAD_EMOJI = "🗣️"

DUREE_QUESTION = 60  # secondes

CORRECT_MESSAGES = [
    "Excellent ! 🎉", "Génial ! 🙌", "Parfait ! ✨", "Trop fort(e) ! 💪",
    "Bravo ! 👏", "Carrément ! 🚀", "Nailed it ! 🌟",
]
WRONG_MESSAGES = [
    "Pas tout à fait... 🤔", "Presque ! 😅", "On retente ! 💡", "Ça arrive ! 🌱",
]
TIMEOUT_MESSAGES = [
    "Trop lent cette fois ! ⏰", "Le temps est passé vite ! ⌛", "La prochaine sera la bonne ! 🕒",
]

# ---------------------------------------------------------------------------
# Contenu du cours (repris de la fiche PDF, + quelques conseils en plus)
# ---------------------------------------------------------------------------

COURS_DATA = {
    "présent": {
        "intro": (
            "On retire la terminaison de l'infinitif (-AR, -ER, -IR) et on ajoute "
            "les terminaisons suivantes :"
        ),
        "groupes": {
            "-AR (hablar)": ["habl-o", "habl-as", "habl-a", "habl-amos", "habl-áis", "habl-an"],
            "-ER (comer)": ["com-o", "com-es", "com-e", "com-emos", "com-éis", "com-en"],
            "-IR (vivir)": ["viv-o", "viv-es", "viv-e", "viv-imos", "viv-ís", "viv-en"],
        },
        "exemples": [
            ("Yo hablo español todos los días.", "Je parle espagnol tous les jours."),
            ("¿Tú comes carne o eres vegetariano?", "Tu manges de la viande ou tu es végétarien ?"),
            ("Nosotros vivimos en Madrid desde 2020.", "Nous vivons à Madrid depuis 2020."),
        ],
        "astuce": (
            "Astuce : au présent, seule la forme « nosotros/vosotros » garde toujours la "
            "voyelle de l'infinitif (-amos/-áis, -emos/-éis, -imos/-ís) ; c'est un repère "
            "pratique pour retrouver le groupe du verbe."
        ),
        "irreguliers": [
            ("ser (être)", ["soy", "eres", "es", "somos", "sois", "son"]),
            ("estar (être/état)", ["estoy", "estás", "está", "estamos", "estáis", "están"]),
            ("tener (avoir)", ["tengo", "tienes", "tiene", "tenemos", "tenéis", "tienen"]),
            ("ir (aller)", ["voy", "vas", "va", "vamos", "vais", "van"]),
            ("hacer (faire)", ["hago", "haces", "hace", "hacemos", "hacéis", "hacen"]),
            ("poder (pouvoir)", ["puedo", "puedes", "puede", "podemos", "podéis", "pueden"]),
            ("querer (vouloir)", ["quiero", "quieres", "quiere", "queremos", "queréis", "quieren"]),
            ("decir (dire)", ["digo", "dices", "dice", "decimos", "decís", "dicen"]),
            ("venir (venir)", ["vengo", "vienes", "viene", "venimos", "venís", "vienen"]),
            ("saber (savoir)", ["sé", "sabes", "sabe", "sabemos", "sabéis", "saben"]),
        ],
        "note_irreguliers": (
            "Ces verbes présentent des irrégularités fréquentes : diphtongaison (e→ie, o→ue), "
            "irrégularité à la 1ère personne (tengo, hago, digo, sé) ou conjugaison totalement "
            "irrégulière (ser, ir)."
        ),
        "conseil": (
            "💡 À retenir en plus : la structure « ir a + infinitif » (voy a comer) sert à "
            "exprimer un futur proche, exactement comme « aller + infinitif » en français."
        ),
    },
    "imparfait": {
        "intro": (
            "L'imparfait (« pretérito imperfecto ») sert à décrire des actions habituelles ou "
            "en cours dans le passé, sans limite de temps précise (équivalent de l'imparfait "
            "français)."
        ),
        "groupes": {
            "-AR (hablar)": ["habl-aba", "habl-abas", "habl-aba", "habl-ábamos", "habl-abais", "habl-aban"],
            "-ER (comer)": ["com-ía", "com-ías", "com-ía", "com-íamos", "com-íais", "com-ían"],
            "-IR (vivir)": ["viv-ía", "viv-ías", "viv-ía", "viv-íamos", "viv-íais", "viv-ían"],
        },
        "exemples": [
            ("Cuando era niño, jugaba en el parque cada tarde.",
             "Quand j'étais enfant, je jouais au parc chaque après-midi."),
            ("Mis padres vivían en Barcelona en los años 90.",
             "Mes parents vivaient à Barcelone dans les années 90."),
            ("Nosotros comíamos juntos todos los domingos.",
             "Nous mangions ensemble tous les dimanches."),
        ],
        "astuce": (
            "Bon à savoir : l'imparfait espagnol est le temps le plus régulier de tous — il "
            "n'existe que trois verbes irréguliers dans toute la langue !"
        ),
        "irreguliers": [
            ("ser (être)", ["era", "eras", "era", "éramos", "erais", "eran"]),
            ("ir (aller)", ["iba", "ibas", "iba", "íbamos", "ibais", "iban"]),
            ("ver (voir)", ["veía", "veías", "veía", "veíamos", "veíais", "veían"]),
        ],
        "note_irreguliers": (
            "Tous les autres verbes, y compris ceux irréguliers au présent (tener, hacer, "
            "poder…), sont parfaitement réguliers à l'imparfait."
        ),
        "conseil": (
            "💡 À retenir en plus : l'imparfait espagnol s'emploie presque exactement comme en "
            "français — pour décrire, exprimer une habitude passée ou une action en cours dans "
            "le passé (« était », « jouait », « vivaient »…)."
        ),
    },
    "passé simple": {
        "intro": (
            "Le passé simple (« pretérito indefinido ») exprime une action ponctuelle et "
            "achevée dans le passé (équivalent du passé composé / passé simple français selon "
            "le contexte)."
        ),
        "groupes": {
            "-AR (hablar)": ["habl-é", "habl-aste", "habl-ó", "habl-amos", "habl-asteis", "habl-aron"],
            "-ER (comer)": ["com-í", "com-iste", "com-ió", "com-imos", "com-isteis", "com-ieron"],
            "-IR (vivir)": ["viv-í", "viv-iste", "viv-ió", "viv-imos", "viv-isteis", "viv-ieron"],
        },
        "exemples": [
            ("Ayer hablé con mi jefe sobre el proyecto.", "Hier j'ai parlé avec mon patron du projet."),
            ("Ella vivió dos años en Argentina.", "Elle a vécu deux ans en Argentine."),
            ("El año pasado fuimos de vacaciones a México.",
             "L'année dernière nous sommes partis en vacances au Mexique."),
        ],
        "astuce": (
            "Attention : c'est le temps qui compte le plus d'irrégularités en espagnol — "
            "beaucoup de verbes très courants changent de radical (tuve, hice, dije…)."
        ),
        "irreguliers": [
            ("ser / ir", ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"]),
            ("estar (être)", ["estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron"]),
            ("tener (avoir)", ["tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron"]),
            ("hacer (faire)", ["hice", "hiciste", "hizo", "hicimos", "hicisteis", "hicieron"]),
            ("poder (pouvoir)", ["pude", "pudiste", "pudo", "pudimos", "pudisteis", "pudieron"]),
            ("poner (mettre)", ["puse", "pusiste", "puso", "pusimos", "pusisteis", "pusieron"]),
            ("querer (vouloir)", ["quise", "quisiste", "quiso", "quisimos", "quisisteis", "quisieron"]),
            ("venir (venir)", ["vine", "viniste", "vino", "vinimos", "vinisteis", "vinieron"]),
            ("decir (dire)", ["dije", "dijiste", "dijo", "dijimos", "dijisteis", "dijeron"]),
            ("traer (apporter)", ["traje", "trajiste", "trajo", "trajimos", "trajisteis", "trajeron"]),
            ("dar (donner)", ["di", "diste", "dio", "dimos", "disteis", "dieron"]),
            ("saber (savoir)", ["supe", "supiste", "supo", "supimos", "supisteis", "supieron"]),
        ],
        "note_irreguliers": (
            "Remarque : « ser » et « ir » partagent exactement la même conjugaison au passé "
            "simple — seul le contexte permet de les distinguer (fui = « je fus » ou « j'allai »)."
        ),
        "conseil": (
            "💡 À retenir en plus : en Espagne, on utilise souvent « he hablado » (passé "
            "composé) pour une action récente, et le passé simple pour une action plus "
            "lointaine ou totalement terminée. En Amérique latine, le passé simple est "
            "largement préféré dans les deux cas."
        ),
    },
}

# ---------------------------------------------------------------------------
# Banque de phrases pour l'onglet Traduction (français -> espagnol)
# ---------------------------------------------------------------------------

TRANSLATION_SENTENCES = {
    "présent": [
        ("Je parle espagnol tous les jours.", "Yo hablo español todos los días."),
        ("Tu manges trop vite.", "Tú comes demasiado rápido."),
        ("Elle vit à Séville.", "Ella vive en Sevilla."),
        ("Nous avons deux voitures.", "Nosotros tenemos dos coches."),
        ("Ils vont au cinéma le samedi.", "Ellos van al cine los sábados."),
        ("Vous faites les devoirs ensemble.", "Vosotros hacéis los deberes juntos."),
        ("Je suis étudiant en espagnol.", "Yo soy estudiante de español."),
        ("Elle veut un café.", "Ella quiere un café."),
        ("Nous vivons à Madrid depuis 2020.", "Nosotros vivimos en Madrid desde 2020."),
        ("Tu peux m'aider, s'il te plaît ?", "¿Tú puedes ayudarme, por favor?"),
    ],
    "imparfait": [
        ("Quand j'étais enfant, je jouais au parc.", "Cuando era niño, jugaba en el parque."),
        ("Mes parents vivaient à Barcelone.", "Mis padres vivían en Barcelona."),
        ("Nous mangions ensemble le dimanche.", "Nosotros comíamos juntos los domingos."),
        ("Tu parlais beaucoup avec tes grands-parents.", "Tú hablabas mucho con tus abuelos."),
        ("Elle allait à la plage chaque été.", "Ella iba a la playa cada verano."),
        ("Vous regardiez la télé après le dîner.", "Vosotros veíais la tele después de cenar."),
        ("J'avais un chien quand j'étais petit.", "Yo tenía un perro cuando era niño."),
        ("Ils étaient très fatigués.", "Ellos estaban muy cansados."),
        ("Nous étudiions l'espagnol au lycée.", "Nosotros estudiábamos español en el instituto."),
        ("Elle travaillait à Madrid avant.", "Ella trabajaba en Madrid antes."),
    ],
    "passé simple": [
        ("Hier, j'ai parlé avec mon patron.", "Ayer hablé con mi jefe."),
        ("Elle a eu un accident le mois dernier.", "Ella tuvo un accidente el mes pasado."),
        ("Nous sommes allés à Barcelone en 2019.", "Nosotros fuimos a Barcelona en 2019."),
        ("Tu as fait le dîner hier soir.", "Tú hiciste la cena anoche."),
        ("Ils sont venus à la fête samedi.", "Ellos vinieron a la fiesta el sábado."),
        ("Vous avez dit la vérité.", "Vosotros dijisteis la verdad."),
        ("J'ai vu ce film l'année dernière.", "Yo vi esa película el año pasado."),
        ("Elle a pu terminer le projet à temps.", "Ella pudo terminar el proyecto a tiempo."),
        ("Nous avons eu une bonne surprise.", "Nosotros tuvimos una buena sorpresa."),
        ("Il a mis le livre sur la table.", "Él puso el libro en la mesa."),
    ],
}


def regular_conjugation(verbe, temps):
    groupe = verbe[-2:]
    radical = verbe[:-2]
    return [radical + t for t in REGULAR_ENDINGS[temps][groupe]]


def get_conjugation(verbe, temps):
    if verbe in IRREGULAR_VERBS and temps in IRREGULAR_VERBS[verbe]:
        return IRREGULAR_VERBS[verbe][temps]
    return regular_conjugation(verbe, temps)


def normalize(texte):
    texte = texte.strip().lower()
    texte = unicodedata.normalize("NFKD", texte)
    return "".join(c for c in texte if not unicodedata.combining(c))


def normalize_sentence(texte):
    """Comparaison tolérante pour des phrases entières : accents, casse,
    ponctuation et espaces multiples sont ignorés."""
    texte = normalize(texte)
    texte = re.sub(r"[¿¡?!.,;:]", "", texte)
    texte = re.sub(r"\s+", " ", texte).strip()
    return texte


# ---------------------------------------------------------------------------
# Application graphique
# ---------------------------------------------------------------------------

class ConjugaisonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🇪🇸 Entraînement conjugaison espagnole")
        self.geometry("880x860")
        self.minsize(820, 800)
        self.configure(bg=BG_APP)
        self._set_app_icon()

        # État du jeu
        self.score = 0
        self.total = 0
        self.streak = 0
        self.best_streak = 0
        self.temps_restant = DUREE_QUESTION
        self.timer_id = None
        self.en_correction = False
        self.mode_toutes_personnes = False
        self.entries = []
        self.feedback_labels = []
        self.verbe = None
        self.temps = None
        self.pronom_idx = None
        self.bonne_reponse = None
        self.current_page = None

        # État de l'onglet Traduction
        self.score_trad = 0
        self.total_trad = 0
        self.trad_en_correction = False
        self.trad_phrase_fr = None
        self.trad_phrase_es = None
        self.trad_temps = None

        self._setup_styles()
        self._build_pages()

        self.bind("<Return>", lambda e: self._on_enter())
        self.protocol("WM_DELETE_WINDOW", self.quitter)

        self._show_page(self.menu_frame)

    # ------------------------------------------------------------------
    # Icône de l'application
    # ------------------------------------------------------------------

    def _set_app_icon(self):
        ico_path = resource_path(os.path.join("assets", "icon.ico"))
        png_path = resource_path(os.path.join("assets", "icon.png"))
        try:
            if os.path.exists(ico_path):
                self.iconbitmap(ico_path)
                return
        except tk.TclError:
            pass
        try:
            if os.path.exists(png_path):
                self._icon_img = tk.PhotoImage(file=png_path)
                self.iconphoto(True, self._icon_img)
        except tk.TclError:
            pass

    # ------------------------------------------------------------------
    # Styles
    # ------------------------------------------------------------------

    def _setup_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TEntry", font=(FONT_FAMILY, 16), padding=6,
            fieldbackground="#FFFDF7", bordercolor=BORDER_SETTINGS
        )
        style.configure("TSpinbox", font=(FONT_FAMILY, 12), padding=4)

        style.configure(
            "Quit.TButton", font=(FONT_FAMILY, 13, "bold"),
            padding=(14, 10), background="#D8CDA9", foreground=COL_TEXT
        )
        style.map("Quit.TButton", background=[("active", "#C9BE9A")])

        for temps, color in TENSE_COLORS.items():
            style_name = f"{temps}.TButton"
            style.configure(
                style_name, font=(FONT_FAMILY, 15, "bold"),
                padding=(18, 12), background=color, foreground="white", borderwidth=0
            )
            style.map(style_name, background=[("active", color)])

        style.configure(
            "traduction.TButton", font=(FONT_FAMILY, 15, "bold"),
            padding=(18, 12), background=TRAD_COLOR, foreground="white", borderwidth=0
        )
        style.map("traduction.TButton", background=[("active", TRAD_COLOR)])

    # ------------------------------------------------------------------
    # Construction des pages (menu / jeu / cours / traduction) empilées
    # ------------------------------------------------------------------

    def _build_pages(self):
        container = tk.Frame(self, bg=BG_APP)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.menu_frame = tk.Frame(container, bg=BG_APP)
        self.jeu_frame = tk.Frame(container, bg=BG_APP)
        self.cours_frame = tk.Frame(container, bg=BG_APP)
        self.traduction_frame = tk.Frame(container, bg=BG_APP)

        for frame in (self.menu_frame, self.jeu_frame, self.cours_frame, self.traduction_frame):
            frame.grid(row=0, column=0, sticky="nsew")

        self._build_menu(self.menu_frame)
        self._build_jeu_page(self.jeu_frame)
        self._build_cours_page(self.cours_frame)
        self._build_traduction_page(self.traduction_frame)

    def _show_page(self, frame):
        if frame is not self.jeu_frame:
            self._stop_timer()
        self.current_page = frame
        frame.tkraise()

    # ==================================================================
    # MENU PRINCIPAL
    # ==================================================================

    def _build_menu(self, parent):
        tk.Label(
            parent, text="🏔️   🌲   🪨   🫐   🏞️", font=(FONT_FAMILY, 30),
            bg=BG_APP, fg=COL_KAKI_DARK
        ).pack(pady=(56, 10))

        tk.Label(
            parent, text="🇪🇸 Entraînement conjugaison espagnole",
            font=(FONT_FAMILY, 27, "bold"), bg=BG_APP, fg=COL_BROWN_DARK,
            justify="center"
        ).pack(pady=(0, 8))

        tk.Label(
            parent,
            text="Pars à l'aventure à travers les temps espagnols,\ncomme une randonnée en pleine nature.",
            font=(FONT_FAMILY, 13, "italic"), bg=BG_APP, fg=COL_MUTED, justify="center"
        ).pack(pady=(0, 50))

        cards = tk.Frame(parent, bg=BG_APP)
        cards.pack()

        self._build_menu_card(
            cards, emoji="🥾", title="Jeu de conjugaison",
            subtitle="Entraîne-toi contre le chrono (60s)\net progresse temps après temps.",
            color=COL_KAKI_DARK, command=lambda: self._go_to_jeu()
        ).grid(row=0, column=0, padx=16, pady=10)

        self._build_menu_card(
            cards, emoji="🌲", title="Cours",
            subtitle="Révise les règles de formation,\nles exemples et les verbes irréguliers.",
            color=COL_BROWN, command=self._go_to_cours
        ).grid(row=0, column=1, padx=16, pady=10)

        self._build_menu_card(
            cards, emoji="🗣️", title="Traduction",
            subtitle="Traduis des phrases générées\npar l'application, temps après temps.",
            color=TRAD_COLOR, command=self._go_to_traduction
        ).grid(row=0, column=2, padx=16, pady=10)

        tk.Label(
            parent, text="🍃  Tu pourras revenir ici à tout moment via « 🏠 Menu »  🍃",
            font=(FONT_FAMILY, 10, "italic"), bg=BG_APP, fg=COL_MUTED
        ).pack(pady=30)

    def _build_menu_card(self, parent, emoji, title, subtitle, color, command):
        card = tk.Frame(
            parent, bg=color, width=235, height=225,
            highlightbackground=COL_BROWN_DARK, highlightthickness=2
        )
        card.pack_propagate(False)

        icon = tk.Label(card, text=emoji, font=(FONT_FAMILY, 36), bg=color)
        icon.pack(pady=(24, 6))
        title_lbl = tk.Label(card, text=title, font=(FONT_FAMILY, 15, "bold"), bg=color, fg="white")
        title_lbl.pack()
        subtitle_lbl = tk.Label(
            card, text=subtitle, font=(FONT_FAMILY, 9), bg=color, fg="#F3ECD9", justify="center"
        )
        subtitle_lbl.pack(pady=(8, 0))

        for widget in (card, icon, title_lbl, subtitle_lbl):
            widget.configure(cursor="hand2")
            widget.bind("<Button-1>", lambda e: command())

        return card

    def _go_to_jeu(self, temps_filter=None):
        if temps_filter is not None:
            self._set_temps_filter(temps_filter)
        self._show_page(self.jeu_frame)
        self.nouvelle_question()

    def _go_to_cours(self):
        self._show_page(self.cours_frame)

    def _go_to_traduction(self):
        self._show_page(self.traduction_frame)
        self.nouvelle_phrase()

    def _go_to_menu(self):
        self._show_page(self.menu_frame)

    # ==================================================================
    # PAGE : JEU DE CONJUGAISON
    # ==================================================================

    def _build_jeu_page(self, parent):
        topbar = tk.Frame(parent, bg=BG_APP)
        topbar.pack(fill="x")
        tk.Button(
            topbar, text="🏠 Menu", font=(FONT_FAMILY, 11, "bold"),
            bg="#D8CDA9", fg=COL_TEXT, relief="flat", bd=0, padx=12, pady=6,
            cursor="hand2", command=self._go_to_menu
        ).pack(side="left", padx=16, pady=10)

        self._build_header(parent)
        self._build_settings_bar(parent)
        self._build_score_bar(parent)
        self._build_question_area(parent)
        self._build_footer(parent)

    def _build_header(self, parent):
        self.header_frame = tk.Frame(parent, bg=TENSE_COLORS["présent"], height=120)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        left = tk.Frame(self.header_frame, bg=TENSE_COLORS["présent"])
        left.pack(side="left", padx=24, pady=16, anchor="w")

        self.title_label = tk.Label(
            left, text="🌲 PRÉSENT", font=(FONT_FAMILY, 28, "bold"),
            fg="white", bg=TENSE_COLORS["présent"]
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            left, text="Presente de indicativo", font=(FONT_FAMILY, 13, "italic"),
            fg="white", bg=TENSE_COLORS["présent"]
        )
        self.subtitle_label.pack(anchor="w")

        right = tk.Frame(self.header_frame, bg=TENSE_COLORS["présent"])
        right.pack(side="right", padx=24, pady=16, anchor="e")

        tk.Label(right, text="⏱", font=(FONT_FAMILY, 30), fg="white",
                 bg=TENSE_COLORS["présent"]).pack(side="left")
        self.timer_label = tk.Label(
            right, text=f"{DUREE_QUESTION}s", font=(FONT_FAMILY, 32, "bold"),
            fg="white", bg=TENSE_COLORS["présent"]
        )
        self.timer_label.pack(side="left", padx=(6, 0))

    def _build_settings_bar(self, parent):
        outer = tk.Frame(parent, bg=BG_SETTINGS, highlightbackground=BORDER_SETTINGS, highlightthickness=1)
        outer.pack(fill="x", padx=20, pady=(14, 0))

        row1 = tk.Frame(outer, bg=BG_SETTINGS)
        row1.pack(fill="x", padx=10, pady=(10, 4))

        tk.Label(
            row1, text="📚 Temps à réviser :",
            font=(FONT_FAMILY, 12, "bold"), bg=BG_SETTINGS, fg=COL_BROWN_DARK
        ).pack(side="left", padx=(0, 10))

        self.temps_filter = None  # None = tous les temps (aléatoire)
        self.temps_buttons = {}
        choix_temps = [("🔀 Tous les temps", None)] + [
            (f"{TENSE_EMOJI[t]} {t.capitalize()}", t) for t in TEMPS
        ]
        for label, value in choix_temps:
            btn = tk.Button(
                row1, text=label, font=(FONT_FAMILY, 11, "bold"),
                relief="flat", bd=0, padx=10, pady=6, cursor="hand2",
                command=lambda v=value: self._set_temps_filter(v)
            )
            btn.pack(side="left", padx=4)
            self.temps_buttons[value] = btn

        row2 = tk.Frame(outer, bg=BG_SETTINGS)
        row2.pack(fill="x", padx=10, pady=(4, 10))

        tk.Label(
            row2, text="🌾 Mode difficile :",
            font=(FONT_FAMILY, 12, "bold"), bg=BG_SETTINGS, fg=COL_BROWN_DARK
        ).pack(side="left", padx=(0, 10))

        self.toutes_personnes_on = False
        self.toutes_personnes_btn = tk.Button(
            row2, font=(FONT_FAMILY, 11, "bold"), relief="flat", bd=0,
            padx=10, pady=6, cursor="hand2", command=self._toggle_toutes_personnes
        )
        self.toutes_personnes_btn.pack(side="left", padx=4)

        self._refresh_temps_buttons()
        self._refresh_toutes_personnes_button()

    def _set_temps_filter(self, valeur):
        self.temps_filter = valeur
        self._refresh_temps_buttons()

    def _refresh_temps_buttons(self):
        for valeur, btn in self.temps_buttons.items():
            actif = valeur == self.temps_filter
            couleur = TENSE_COLORS[valeur] if valeur else COL_BROWN_DARK
            if actif:
                btn.config(bg=couleur, fg="white")
            else:
                btn.config(bg="#FFFFFF", fg=COL_BROWN_DARK)

    def _toggle_toutes_personnes(self):
        self.toutes_personnes_on = not self.toutes_personnes_on
        self._refresh_toutes_personnes_button()

    def _refresh_toutes_personnes_button(self):
        if self.toutes_personnes_on:
            self.toutes_personnes_btn.config(
                text="🌾 Toutes les personnes : ON", bg=COL_ACCENT, fg="white"
            )
        else:
            self.toutes_personnes_btn.config(
                text="🌾 Toutes les personnes : OFF", bg="#FFFFFF", fg=COL_BROWN_DARK
            )

    def _build_score_bar(self, parent):
        bar = tk.Frame(parent, bg=BG_APP)
        bar.pack(fill="x", padx=20, pady=(10, 6))

        self.score_label = tk.Label(
            bar, text="🏆 Score : 0/0", font=(FONT_FAMILY, 15, "bold"),
            bg=BG_APP, fg=COL_TEXT
        )
        self.score_label.pack(side="left")

        self.streak_label = tk.Label(
            bar, text="", font=(FONT_FAMILY, 15, "bold"),
            bg=BG_APP, fg=COL_STREAK
        )
        self.streak_label.pack(side="right")

    def _build_question_area(self, parent):
        outer = tk.Frame(parent, bg=BG_APP)
        outer.pack(fill="both", expand=True, padx=20, pady=10)

        self.question_frame = tk.Frame(
            outer, bg=BG_CARD, highlightbackground=TENSE_COLORS["présent"], highlightthickness=3
        )
        self.question_frame.pack(fill="both", expand=True)

        self.result_label = tk.Label(
            parent, text="", font=(FONT_FAMILY, 15, "bold"), bg=BG_APP,
            wraplength=680, justify="left"
        )
        self.result_label.pack(fill="x", padx=24, pady=(0, 6))

    def _build_footer(self, parent):
        footer = tk.Frame(parent, bg=BG_APP)
        footer.pack(fill="x", padx=20, pady=16)

        self.quitter_btn = ttk.Button(
            footer, text="🚪 Quitter", style="Quit.TButton", command=self.quitter
        )
        self.quitter_btn.pack(side="left")

        self.valider_btn = ttk.Button(
            footer, text="✅ Valider  (Entrée)", style="présent.TButton", command=self._on_enter
        )
        self.valider_btn.pack(side="right")

    # ------------------------------------------------------------------
    # Cycle d'une question
    # ------------------------------------------------------------------

    def nouvelle_question(self):
        self._stop_timer()
        self.en_correction = False
        self.result_label.config(text="")

        self.verbe = random.choice(ALL_VERBS)
        self.temps = self.temps_filter if self.temps_filter is not None else random.choice(TEMPS)

        self.mode_toutes_personnes = self.toutes_personnes_on

        conjugaisons = get_conjugation(self.verbe, self.temps)
        if self.mode_toutes_personnes:
            self.bonne_reponse = conjugaisons
            self.pronom_idx = None
        else:
            self.pronom_idx = random.randint(0, 5)
            self.bonne_reponse = conjugaisons[self.pronom_idx]

        self._update_header()
        self._render_question()
        self._start_timer()

    def _update_header(self):
        color = TENSE_COLORS[self.temps]
        emoji = TENSE_EMOJI[self.temps]
        self.header_frame.config(bg=color)
        for child in self.header_frame.winfo_children():
            child.config(bg=color)
            for sub in child.winfo_children():
                sub.config(bg=color)
        self.title_label.config(text=f"{emoji} {self.temps.upper()}")
        self.subtitle_label.config(text=TENSE_SUBTITLES[self.temps])
        self.question_frame.config(highlightbackground=color)
        self.valider_btn.config(style=f"{self.temps}.TButton")

    def _render_question(self):
        for w in self.question_frame.winfo_children():
            w.destroy()
        self.entries = []
        self.feedback_labels = []

        tk.Label(
            self.question_frame, text=f"📝 Verbe : {self.verbe}",
            font=(FONT_FAMILY, 22, "bold"), bg=BG_CARD, fg=COL_TEXT
        ).pack(pady=(26, 6))

        if self.mode_toutes_personnes:
            tk.Label(
                self.question_frame,
                text="🌾 Conjugue le verbe pour TOUTES les personnes :",
                font=(FONT_FAMILY, 13, "italic"), bg=BG_CARD, fg=COL_ACCENT
            ).pack(pady=(0, 16))

            grid = tk.Frame(self.question_frame, bg=BG_CARD)
            grid.pack(pady=4)

            for i, pronom in enumerate(PRONOMS):
                tk.Label(
                    grid, text=pronom, font=(FONT_FAMILY, 13, "bold"),
                    bg=BG_CARD, fg=COL_MUTED, width=13, anchor="e"
                ).grid(row=i, column=0, padx=(0, 10), pady=6, sticky="e")

                entry = ttk.Entry(grid, font=(FONT_FAMILY, 14), width=18)
                entry.grid(row=i, column=1, pady=6, sticky="w")
                self.entries.append(entry)

                fb = tk.Label(grid, text="", font=(FONT_FAMILY, 13, "bold"), bg=BG_CARD)
                fb.grid(row=i, column=2, padx=(12, 0), pady=6, sticky="w")
                self.feedback_labels.append(fb)

            self.entries[0].focus_set()
        else:
            tk.Label(
                self.question_frame, text=f"👉 Conjugue pour : « {PRONOMS[self.pronom_idx]} »",
                font=(FONT_FAMILY, 17), bg=BG_CARD, fg=COL_MUTED
            ).pack(pady=(0, 20))

            entry = ttk.Entry(self.question_frame, font=(FONT_FAMILY, 20), width=22, justify="center")
            entry.pack(pady=6, ipady=6)
            entry.focus_set()
            self.entries.append(entry)

    # ------------------------------------------------------------------
    # Chrono
    # ------------------------------------------------------------------

    def _start_timer(self):
        self.temps_restant = DUREE_QUESTION
        self._update_timer_label()
        self._tick()

    def _tick(self):
        if self.temps_restant <= 0:
            self._on_timeout()
            return
        self._update_timer_label()
        self.temps_restant -= 1
        self.timer_id = self.after(1000, self._tick)

    def _update_timer_label(self):
        self.timer_label.config(text=f"{self.temps_restant}s")
        self.timer_label.config(fg="#F3C6B0" if self.temps_restant <= 10 else "white")

    def _stop_timer(self):
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None

    def _on_timeout(self):
        self._stop_timer()
        self._corriger(timeout=True)

    # ------------------------------------------------------------------
    # Validation / correction
    # ------------------------------------------------------------------

    def _on_enter(self):
        if self.current_page is self.jeu_frame:
            if self.en_correction:
                self.nouvelle_question()
            else:
                self._stop_timer()
                self._corriger(timeout=False)
        elif self.current_page is self.traduction_frame:
            if self.trad_en_correction:
                self.nouvelle_phrase()
            else:
                self._corriger_traduction()

    def _corriger(self, timeout):
        self.en_correction = True
        self.total += 1

        if self.mode_toutes_personnes:
            nb_correct = 0
            for i, entry in enumerate(self.entries):
                valeur = "" if timeout else entry.get()
                correcte = self.bonne_reponse[i]
                ok = normalize(valeur) == normalize(correcte)
                entry.config(state="disabled")
                if ok:
                    nb_correct += 1
                    self.feedback_labels[i].config(text=f"✅ {correcte}", fg=COL_OK)
                else:
                    self.feedback_labels[i].config(text=f"❌ {correcte}", fg=COL_KO)

            parfait = nb_correct == 6
            if parfait:
                self.score += 1
                self.streak += 1
                self.best_streak = max(self.best_streak, self.streak)
                msg = random.choice(CORRECT_MESSAGES)
                self.result_label.config(text=f"{msg} Les 6 formes sont correctes !", fg=COL_OK)
            else:
                self.streak = 0
                msg = random.choice(TIMEOUT_MESSAGES if timeout else WRONG_MESSAGES)
                self.result_label.config(text=f"{msg} ({nb_correct}/6 formes correctes)", fg=COL_KO)
        else:
            entry = self.entries[0]
            valeur = "" if timeout else entry.get()
            ok = normalize(valeur) == normalize(self.bonne_reponse)
            entry.config(state="disabled")
            if ok:
                self.score += 1
                self.streak += 1
                self.best_streak = max(self.best_streak, self.streak)
                msg = random.choice(CORRECT_MESSAGES)
                self.result_label.config(text=msg, fg=COL_OK)
            else:
                self.streak = 0
                msg = random.choice(TIMEOUT_MESSAGES if timeout else WRONG_MESSAGES)
                self.result_label.config(
                    text=f"{msg} La bonne réponse était : {self.bonne_reponse}", fg=COL_KO
                )

        self.score_label.config(text=f"🏆 Score : {self.score}/{self.total}")
        self.streak_label.config(text=f"🔥 Série : {self.streak}" if self.streak >= 2 else "")
        self.valider_btn.config(text="▶ Question suivante  (Entrée)")

    def quitter(self):
        self._stop_timer()
        recap = []
        if self.total > 0:
            pourcentage = 100 * self.score / self.total
            recap.append(
                f"🎮 Jeu de conjugaison : {self.score}/{self.total} ({pourcentage:.0f} %) "
                f"— meilleure série {self.best_streak} 🔥"
            )
        if self.total_trad > 0:
            pourcentage_trad = 100 * self.score_trad / self.total_trad
            recap.append(f"🗣️ Traduction : {self.score_trad}/{self.total_trad} ({pourcentage_trad:.0f} %)")
        if recap:
            messagebox.showinfo("Fin de la session", "\n\n".join(recap))
        self.destroy()

    # ==================================================================
    # PAGE : COURS
    # ==================================================================

    def _build_cours_page(self, parent):
        topbar = tk.Frame(parent, bg=BG_APP)
        topbar.pack(fill="x")
        tk.Button(
            topbar, text="🏠 Menu", font=(FONT_FAMILY, 11, "bold"),
            bg="#D8CDA9", fg=COL_TEXT, relief="flat", bd=0, padx=12, pady=6,
            cursor="hand2", command=self._go_to_menu
        ).pack(side="left", padx=16, pady=10)

        body_container = tk.Frame(parent, bg=BG_APP)
        body_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(body_container, bg=BG_APP, highlightthickness=0)
        scrollbar = ttk.Scrollbar(body_container, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG_APP)

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _resize_inner(event):
            canvas.coords(canvas_window, event.width / 2, 0)
            canvas.itemconfig(canvas_window, width=min(event.width - 40, 720))
        canvas.bind("<Configure>", _resize_inner)

        def _on_mousewheel(event):
            delta = -1 * (event.delta // 120) if event.delta else (1 if event.num == 5 else -1)
            canvas.yview_scroll(delta, "units")
        canvas.bind("<Enter>", lambda e: (
            canvas.bind_all("<MouseWheel>", _on_mousewheel),
            canvas.bind_all("<Button-4>", _on_mousewheel),
            canvas.bind_all("<Button-5>", _on_mousewheel),
        ))
        canvas.bind("<Leave>", lambda e: (
            canvas.unbind_all("<MouseWheel>"),
            canvas.unbind_all("<Button-4>"),
            canvas.unbind_all("<Button-5>"),
        ))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(
            inner, text="🍃 🌲 🍃  Rappel de cours — la conjugaison espagnole  🍃 🌲 🍃",
            font=(FONT_FAMILY, 19, "bold"), bg=BG_APP, fg=COL_BROWN_DARK, justify="center"
        ).pack(pady=(20, 4))
        tk.Label(
            inner, text="Règles de formation, exemples et verbes irréguliers les plus utilisés.",
            font=(FONT_FAMILY, 12, "italic"), bg=BG_APP, fg=COL_MUTED, justify="center"
        ).pack(pady=(0, 16))

        for temps in TEMPS:
            self._build_cours_section(inner, temps)

        tk.Frame(inner, bg=BG_APP, height=20).pack()

    def _build_cours_section(self, parent, temps):
        data = COURS_DATA[temps]
        color = TENSE_COLORS[temps]
        emoji = TENSE_EMOJI[temps]

        card = tk.Frame(parent, bg=BG_CARD, highlightbackground=color, highlightthickness=3)
        card.pack(pady=(0, 20))

        # Bandeau titre
        banner = tk.Frame(card, bg=color)
        banner.pack(fill="x")
        tk.Label(
            banner, text=f"{emoji} {temps.upper()}", font=(FONT_FAMILY, 20, "bold"),
            bg=color, fg="white", justify="center"
        ).pack(pady=(10, 0))
        tk.Label(
            banner, text=TENSE_SUBTITLES[temps], font=(FONT_FAMILY, 11, "italic"),
            bg=color, fg="white", justify="center"
        ).pack(pady=(0, 10))

        body = tk.Frame(card, bg=BG_CARD)
        body.pack(pady=16, padx=20)

        # Règles de formation
        tk.Label(
            body, text="Règles de formation (verbes réguliers)",
            font=(FONT_FAMILY, 14, "bold"), bg=BG_CARD, fg=COL_TEXT, justify="center"
        ).pack(pady=(0, 4))
        tk.Label(
            body, text=data["intro"], font=(FONT_FAMILY, 11), bg=BG_CARD, fg=COL_TEXT,
            wraplength=620, justify="center"
        ).pack(pady=(0, 10))

        self._table_groupes(body, data["groupes"], color)

        # Exemples
        tk.Label(
            body, text="Exemples", font=(FONT_FAMILY, 14, "bold"), bg=BG_CARD, fg=COL_TEXT,
            justify="center"
        ).pack(pady=(16, 4))
        for es, fr in data["exemples"]:
            tk.Label(
                body, text=f"{es}\n{fr}", font=(FONT_FAMILY, 11), bg=BG_CARD, fg=COL_TEXT,
                wraplength=620, justify="center"
            ).pack(pady=6)

        # Astuce
        tk.Label(
            body, text=data["astuce"], font=(FONT_FAMILY, 10, "italic"), bg=BG_CARD, fg=COL_MUTED,
            wraplength=620, justify="center"
        ).pack(pady=(10, 4))

        # Verbes irréguliers
        tk.Label(
            body, text="Verbes irréguliers les plus utilisés",
            font=(FONT_FAMILY, 14, "bold"), bg=BG_CARD, fg=COL_TEXT, justify="center"
        ).pack(pady=(16, 6))

        self._table_irreguliers(body, data["irreguliers"], color)

        tk.Label(
            body, text=data["note_irreguliers"], font=(FONT_FAMILY, 10, "italic"),
            bg=BG_CARD, fg=COL_MUTED, wraplength=620, justify="center"
        ).pack(pady=(8, 4))

        # Conseil complémentaire (info ajoutée par rapport au PDF)
        conseil_box = tk.Frame(body, bg="#F0E6C8", highlightbackground=COL_BROWN, highlightthickness=1)
        conseil_box.pack(pady=(12, 4))
        tk.Label(
            conseil_box, text=data["conseil"], font=(FONT_FAMILY, 10, "bold"),
            bg="#F0E6C8", fg=COL_BROWN_DARK, wraplength=600, justify="center"
        ).pack(padx=10, pady=8)

        # Bouton de raccourci vers le jeu sur ce temps précis
        entrainer_btn = tk.Button(
            body, text=f"🥾 S'entraîner sur le {temps} ▶", font=(FONT_FAMILY, 11, "bold"),
            bg=color, fg="white", relief="flat", bd=0, padx=14, pady=8, cursor="hand2",
            command=lambda t=temps: self._go_to_jeu(t)
        )
        entrainer_btn.pack(pady=(10, 0))

    def _table_groupes(self, parent, groupes, color):
        table = tk.Frame(parent, bg=BG_CARD)
        table.pack(pady=(0, 4))

        noms_groupes = list(groupes.keys())
        tk.Label(
            table, text="", font=(FONT_FAMILY, 10, "bold"), bg=color, fg="white", width=14
        ).grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        for c, nom in enumerate(noms_groupes, start=1):
            tk.Label(
                table, text=nom, font=(FONT_FAMILY, 10, "bold"), bg=color, fg="white",
                width=14, padx=4, pady=6
            ).grid(row=0, column=c, sticky="nsew", padx=1, pady=1)

        for r, pronom in enumerate(PRONOMS, start=1):
            bg_row = "#EFE7D0" if r % 2 == 0 else BG_CARD
            tk.Label(
                table, text=pronom, font=(FONT_FAMILY, 10, "bold"), bg=bg_row, fg=COL_TEXT,
                width=14, padx=4, pady=5
            ).grid(row=r, column=0, sticky="nsew", padx=1, pady=1)
            for c, nom in enumerate(noms_groupes, start=1):
                forme = groupes[nom][r - 1]
                tk.Label(
                    table, text=forme, font=(FONT_FAMILY, 10), bg=bg_row, fg=COL_TEXT,
                    width=14, padx=4, pady=5
                ).grid(row=r, column=c, sticky="nsew", padx=1, pady=1)

    def _table_irreguliers(self, parent, irreguliers, color):
        table = tk.Frame(parent, bg=BG_CARD)
        table.pack()

        headers = ["Infinitif"] + PRONOMS
        for c, h in enumerate(headers):
            tk.Label(
                table, text=h, font=(FONT_FAMILY, 9, "bold"), bg=color, fg="white",
                width=12 if c == 0 else 10, padx=3, pady=6
            ).grid(row=0, column=c, sticky="nsew", padx=1, pady=1)

        for r, (infinitif, formes) in enumerate(irreguliers, start=1):
            bg_row = "#EFE7D0" if r % 2 == 0 else BG_CARD
            tk.Label(
                table, text=infinitif, font=(FONT_FAMILY, 9, "bold"), bg=bg_row, fg=COL_TEXT,
                width=12, padx=3, pady=4
            ).grid(row=r, column=0, sticky="nsew", padx=1, pady=1)
            for c, forme in enumerate(formes, start=1):
                tk.Label(
                    table, text=forme, font=(FONT_FAMILY, 9), bg=bg_row, fg=COL_TEXT,
                    width=10, padx=3, pady=4
                ).grid(row=r, column=c, sticky="nsew", padx=1, pady=1)


    # ==================================================================
    # PAGE : TRADUCTION
    # ==================================================================

    def _build_traduction_page(self, parent):
        topbar = tk.Frame(parent, bg=BG_APP)
        topbar.pack(fill="x")
        tk.Button(
            topbar, text="🏠 Menu", font=(FONT_FAMILY, 11, "bold"),
            bg="#D8CDA9", fg=COL_TEXT, relief="flat", bd=0, padx=12, pady=6,
            cursor="hand2", command=self._go_to_menu
        ).pack(side="left", padx=16, pady=10)

        header = tk.Frame(parent, bg=TRAD_COLOR, height=110)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text=f"{TRAD_EMOJI} TRADUCTION", font=(FONT_FAMILY, 26, "bold"),
            fg="white", bg=TRAD_COLOR
        ).pack(pady=(20, 0))
        tk.Label(
            header, text="Traduis la phrase en espagnol",
            font=(FONT_FAMILY, 12, "italic"), fg="white", bg=TRAD_COLOR
        ).pack()

        # Filtre de temps (comme dans le Jeu, mais propre à cet onglet)
        settings = tk.Frame(parent, bg=BG_SETTINGS, highlightbackground=BORDER_SETTINGS, highlightthickness=1)
        settings.pack(fill="x", padx=20, pady=(14, 0))
        row = tk.Frame(settings, bg=BG_SETTINGS)
        row.pack(fill="x", padx=10, pady=10)
        tk.Label(
            row, text="📚 Temps à réviser :", font=(FONT_FAMILY, 12, "bold"),
            bg=BG_SETTINGS, fg=COL_BROWN_DARK
        ).pack(side="left", padx=(0, 10))

        self.trad_temps_filter = None
        self.trad_temps_buttons = {}
        choix_temps = [("🔀 Tous les temps", None)] + [
            (f"{TENSE_EMOJI[t]} {t.capitalize()}", t) for t in TEMPS
        ]
        for label, value in choix_temps:
            btn = tk.Button(
                row, text=label, font=(FONT_FAMILY, 11, "bold"),
                relief="flat", bd=0, padx=10, pady=6, cursor="hand2",
                command=lambda v=value: self._set_trad_temps_filter(v)
            )
            btn.pack(side="left", padx=4)
            self.trad_temps_buttons[value] = btn
        self._refresh_trad_temps_buttons()

        # Score
        score_bar = tk.Frame(parent, bg=BG_APP)
        score_bar.pack(fill="x", padx=20, pady=(10, 6))
        self.score_trad_label = tk.Label(
            score_bar, text="🏆 Score : 0/0", font=(FONT_FAMILY, 15, "bold"), bg=BG_APP, fg=COL_TEXT
        )
        self.score_trad_label.pack(side="left")

        # Zone de la phrase
        outer = tk.Frame(parent, bg=BG_APP)
        outer.pack(fill="both", expand=True, padx=20, pady=10)
        self.trad_card = tk.Frame(
            outer, bg=BG_CARD, highlightbackground=TRAD_COLOR, highlightthickness=3
        )
        self.trad_card.pack(fill="both", expand=True)

        self.trad_result_label = tk.Label(
            parent, text="", font=(FONT_FAMILY, 14, "bold"), bg=BG_APP,
            wraplength=760, justify="left"
        )
        self.trad_result_label.pack(fill="x", padx=24, pady=(0, 6))

        # Pied de page
        footer = tk.Frame(parent, bg=BG_APP)
        footer.pack(fill="x", padx=20, pady=16)
        ttk.Button(
            footer, text="🚪 Quitter", style="Quit.TButton", command=self.quitter
        ).pack(side="left")
        self.trad_valider_btn = ttk.Button(
            footer, text="✅ Valider  (Entrée)", style="traduction.TButton",
            command=self._on_enter
        )
        self.trad_valider_btn.pack(side="right")

    def _set_trad_temps_filter(self, valeur):
        self.trad_temps_filter = valeur
        self._refresh_trad_temps_buttons()

    def _refresh_trad_temps_buttons(self):
        for valeur, btn in self.trad_temps_buttons.items():
            actif = valeur == self.trad_temps_filter
            couleur = TENSE_COLORS[valeur] if valeur else COL_BROWN_DARK
            if actif:
                btn.config(bg=couleur, fg="white")
            else:
                btn.config(bg="#FFFFFF", fg=COL_BROWN_DARK)

    def nouvelle_phrase(self):
        self.trad_en_correction = False
        self.trad_result_label.config(text="")

        self.trad_temps = (
            self.trad_temps_filter if self.trad_temps_filter is not None else random.choice(TEMPS)
        )
        fr, es = random.choice(TRANSLATION_SENTENCES[self.trad_temps])
        self.trad_phrase_fr = fr
        self.trad_phrase_es = es

        for w in self.trad_card.winfo_children():
            w.destroy()

        tk.Label(
            self.trad_card,
            text=f"{TENSE_EMOJI[self.trad_temps]} Temps demandé : {self.trad_temps}",
            font=(FONT_FAMILY, 11, "italic"), bg=BG_CARD, fg=COL_MUTED
        ).pack(pady=(24, 10))

        tk.Label(
            self.trad_card, text=self.trad_phrase_fr, font=(FONT_FAMILY, 19, "bold"),
            bg=BG_CARD, fg=COL_TEXT, wraplength=680, justify="center"
        ).pack(pady=(0, 20), padx=20)

        self.trad_entry = ttk.Entry(self.trad_card, font=(FONT_FAMILY, 15), width=50, justify="center")
        self.trad_entry.pack(pady=6, ipady=6)
        self.trad_entry.focus_set()

    def _corriger_traduction(self):
        self.trad_en_correction = True
        self.total_trad += 1

        reponse = self.trad_entry.get()
        ok = normalize_sentence(reponse) == normalize_sentence(self.trad_phrase_es)
        self.trad_entry.config(state="disabled")

        if ok:
            self.score_trad += 1
            msg = random.choice(CORRECT_MESSAGES)
            self.trad_result_label.config(text=msg, fg=COL_OK)
        else:
            msg = random.choice(WRONG_MESSAGES)
            self.trad_result_label.config(
                text=f"{msg} Traduction attendue : {self.trad_phrase_es}", fg=COL_KO
            )

        self.score_trad_label.config(text=f"🏆 Score : {self.score_trad}/{self.total_trad}")
        self.trad_valider_btn.config(text="▶ Phrase suivante  (Entrée)")


if __name__ == "__main__":
    app = ConjugaisonApp()
    app.mainloop()
