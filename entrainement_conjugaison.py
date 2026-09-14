#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entraînement à la conjugaison espagnole
========================================
- Choisit un verbe espagnol au hasard
- Choisit un temps au hasard parmi : présent, imparfait, passé simple
- Choisit une personne au hasard (yo, tú, él/ella/Ud., nosotros, vosotros, ellos/Uds.)
- Tu as 60 secondes pour taper la bonne conjugaison

Lance le script avec :  python3 entrainement_conjugaison.py
Tape 'q' à tout moment pour quitter et voir ton score.
"""

import random
import threading
import queue
import time
import unicodedata

# ---------------------------------------------------------------------------
# Données
# ---------------------------------------------------------------------------

PRONOMS = ["yo", "tú", "él/ella/Ud.", "nosotros", "vosotros", "ellos/Uds."]
TEMPS = ["présent", "imparfait", "passé simple"]

# Verbes réguliers (les 3 groupes -AR / -ER / -IR)
REGULAR_VERBS = [
    "hablar", "estudiar", "trabajar", "viajar", "comprar", "cantar", "bailar", "caminar",
    "comer", "aprender", "vender", "deber", "correr",
    "vivir", "escribir", "abrir", "decidir", "asistir",
]

# Verbes irréguliers : seules les formes qui dérogent à la règle générale
# sont précisées ici. Pour un temps non listé, le verbe suit la règle
# régulière normale (ex : "tener" est régulier à l'imparfait -> tenía...).
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
# Logique de conjugaison
# ---------------------------------------------------------------------------

def regular_conjugation(verbe, temps):
    """Conjugue un verbe régulier (-ar/-er/-ir) au temps donné -> liste de 6 formes."""
    groupe = verbe[-2:]  # "ar", "er" ou "ir"
    radical = verbe[:-2]
    terminaisons = REGULAR_ENDINGS[temps][groupe]
    return [radical + t for t in terminaisons]


def get_conjugation(verbe, temps):
    """Renvoie la liste des 6 formes conjuguées, en tenant compte des irrégularités."""
    if verbe in IRREGULAR_VERBS and temps in IRREGULAR_VERBS[verbe]:
        return IRREGULAR_VERBS[verbe][temps]
    return regular_conjugation(verbe, temps)


def normalize(texte):
    """Minuscules, sans espaces superflus, sans accents (comparaison tolérante)."""
    texte = texte.strip().lower()
    texte = unicodedata.normalize("NFKD", texte)
    return "".join(c for c in texte if not unicodedata.combining(c))


# ---------------------------------------------------------------------------
# Saisie avec chrono de 60 secondes
# ---------------------------------------------------------------------------

def ask_with_timeout(prompt, timeout=60):
    """Pose une question et attend une réponse pendant `timeout` secondes max.
    Renvoie la réponse (str) ou None si le temps est écoulé."""
    q = queue.Queue()

    def lire_entree():
        try:
            reponse = input(prompt)
        except EOFError:
            reponse = None
        q.put(reponse)

    thread = threading.Thread(target=lire_entree, daemon=True)
    thread.start()

    try:
        return q.get(timeout=timeout)
    except queue.Empty:
        return None


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------

def main():
    print("=" * 55)
    print(" ENTRAÎNEMENT À LA CONJUGAISON ESPAGNOLE")
    print(" Présent / Imparfait / Passé simple")
    print("=" * 55)
    print("Tu as 60 secondes par question. Tape 'q' pour quitter.\n")

    score = 0
    total = 0

    try:
        while True:
            verbe = random.choice(ALL_VERBS)
            temps = random.choice(TEMPS)
            idx = random.randint(0, 5)
            pronom = PRONOMS[idx]
            conjugaisons = get_conjugation(verbe, temps)
            bonne_reponse = conjugaisons[idx]

            print(f"[Question {total + 1}]")
            print(f"Verbe : {verbe}   |   Temps : {temps}   |   Personne : {pronom}")

            debut = time.time()
            reponse = ask_with_timeout("Ta réponse (60s) > ", timeout=60)
            duree = time.time() - debut

            if reponse is not None and reponse.strip().lower() == "q":
                break

            total += 1

            if reponse is None:
                print(f"⏰ Temps écoulé ! La bonne réponse était : {bonne_reponse}\n")
            elif normalize(reponse) == normalize(bonne_reponse):
                score += 1
                print(f"✅ Correct ! ({duree:.1f}s)\n")
            else:
                print(f"❌ Faux. La bonne réponse était : {bonne_reponse}\n")

    except KeyboardInterrupt:
        print("\n\nInterrompu par l'utilisateur.")

    print("=" * 55)
    if total > 0:
        pourcentage = 100 * score / total
        print(f" Score final : {score}/{total} ({pourcentage:.0f}%)")
    else:
        print(" Aucune question répondue.")
    print("=" * 55)


if __name__ == "__main__":
    main()
