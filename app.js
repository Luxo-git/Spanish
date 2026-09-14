"use strict";

/* ===========================================================
   Data
   =========================================================== */

const PRONOUNS = ["yo", "tú", "él/ella/Ud.", "nosotros", "vosotros", "ellos/Uds."];
const TENSES = ["present", "imperfect", "preterite"];

const REGULAR_VERBS = [
  "hablar", "estudiar", "trabajar", "viajar", "comprar", "cantar", "bailar", "caminar",
  "comer", "aprender", "vender", "deber", "correr",
  "vivir", "escribir", "abrir", "decidir", "asistir",
];

const IRREGULAR_VERBS = {
  ser: {
    present: ["soy", "eres", "es", "somos", "sois", "son"],
    imperfect: ["era", "eras", "era", "éramos", "erais", "eran"],
    preterite: ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"],
  },
  estar: {
    present: ["estoy", "estás", "está", "estamos", "estáis", "están"],
    preterite: ["estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron"],
  },
  tener: {
    present: ["tengo", "tienes", "tiene", "tenemos", "tenéis", "tienen"],
    preterite: ["tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron"],
  },
  ir: {
    present: ["voy", "vas", "va", "vamos", "vais", "van"],
    imperfect: ["iba", "ibas", "iba", "íbamos", "ibais", "iban"],
    preterite: ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"],
  },
  hacer: {
    present: ["hago", "haces", "hace", "hacemos", "hacéis", "hacen"],
    preterite: ["hice", "hiciste", "hizo", "hicimos", "hicisteis", "hicieron"],
  },
  poder: {
    present: ["puedo", "puedes", "puede", "podemos", "podéis", "pueden"],
    preterite: ["pude", "pudiste", "pudo", "pudimos", "pudisteis", "pudieron"],
  },
  querer: {
    present: ["quiero", "quieres", "quiere", "queremos", "queréis", "quieren"],
    preterite: ["quise", "quisiste", "quiso", "quisimos", "quisisteis", "quisieron"],
  },
  decir: {
    present: ["digo", "dices", "dice", "decimos", "decís", "dicen"],
    preterite: ["dije", "dijiste", "dijo", "dijimos", "dijisteis", "dijeron"],
  },
  venir: {
    present: ["vengo", "vienes", "viene", "venimos", "venís", "vienen"],
    preterite: ["vine", "viniste", "vino", "vinimos", "vinisteis", "vinieron"],
  },
  saber: {
    present: ["sé", "sabes", "sabe", "sabemos", "sabéis", "saben"],
    preterite: ["supe", "supiste", "supo", "supimos", "supisteis", "supieron"],
  },
  ver: {
    imperfect: ["veía", "veías", "veía", "veíamos", "veíais", "veían"],
    preterite: ["vi", "viste", "vio", "vimos", "visteis", "vieron"],
  },
  poner: {
    preterite: ["puse", "pusiste", "puso", "pusimos", "pusisteis", "pusieron"],
  },
  traer: {
    preterite: ["traje", "trajiste", "trajo", "trajimos", "trajisteis", "trajeron"],
  },
  dar: {
    preterite: ["di", "diste", "dio", "dimos", "disteis", "dieron"],
  },
};

const ALL_VERBS = REGULAR_VERBS.concat(Object.keys(IRREGULAR_VERBS));

const REGULAR_ENDINGS = {
  present: {
    ar: ["o", "as", "a", "amos", "áis", "an"],
    er: ["o", "es", "e", "emos", "éis", "en"],
    ir: ["o", "es", "e", "imos", "ís", "en"],
  },
  imperfect: {
    ar: ["aba", "abas", "aba", "ábamos", "abais", "aban"],
    er: ["ía", "ías", "ía", "íamos", "íais", "ían"],
    ir: ["ía", "ías", "ía", "íamos", "íais", "ían"],
  },
  preterite: {
    ar: ["é", "aste", "ó", "amos", "asteis", "aron"],
    er: ["í", "iste", "ió", "imos", "isteis", "ieron"],
    ir: ["í", "iste", "ió", "imos", "isteis", "ieron"],
  },
};

const TENSE_COLORS = { present: "#7D8F5A", imperfect: "#8B5E3C", preterite: "#4B3621" };
const TENSE_EMOJI = { present: "🌲", imperfect: "🏞️", preterite: "🪨" };
const TENSE_SUBTITLES = {
  present: "Presente de indicativo",
  imperfect: "Pretérito imperfecto",
  preterite: "Pretérito indefinido",
};
const TRANSLATION_COLOR = "#5C6B3C";

const CORRECT_MESSAGES = [
  "Excellent! 🎉", "Great job! 🙌", "Perfect! ✨", "Awesome! 💪",
  "Well done! 👏", "Nailed it! 🌟", "Fantastic! 🚀",
];
const WRONG_MESSAGES = [
  "Not quite... 🤔", "So close! 😅", "Let's try again! 💡", "That happens! 🌱",
];
const TIMEOUT_MESSAGES = [
  "Too slow this time! ⏰", "Time flew by! ⌛", "Next one's yours! 🕒",
];

const DURATION_QUESTION = 60;

const COURSE_DATA = {
  present: {
    intro: "Drop the infinitive ending (-AR, -ER, -IR) and add the following endings:",
    groups: {
      "-AR (hablar)": ["habl-o", "habl-as", "habl-a", "habl-amos", "habl-áis", "habl-an"],
      "-ER (comer)": ["com-o", "com-es", "com-e", "com-emos", "com-éis", "com-en"],
      "-IR (vivir)": ["viv-o", "viv-es", "viv-e", "viv-imos", "viv-ís", "viv-en"],
    },
    examples: [
      ["Yo hablo español todos los días.", "I speak Spanish every day."],
      ["¿Tú comes carne o eres vegetariano?", "Do you eat meat, or are you vegetarian?"],
      ["Nosotros vivimos en Madrid desde 2020.", "We've lived in Madrid since 2020."],
    ],
    tip: "Tip: in the present tense, only the « nosotros/vosotros » form always keeps the infinitive's vowel (-amos/-áis, -emos/-éis, -imos/-ís) — a handy way to spot the verb group.",
    irregulars: [
      ["ser (to be)", ["soy", "eres", "es", "somos", "sois", "son"]],
      ["estar (to be / state)", ["estoy", "estás", "está", "estamos", "estáis", "están"]],
      ["tener (to have)", ["tengo", "tienes", "tiene", "tenemos", "tenéis", "tienen"]],
      ["ir (to go)", ["voy", "vas", "va", "vamos", "vais", "van"]],
      ["hacer (to do/make)", ["hago", "haces", "hace", "hacemos", "hacéis", "hacen"]],
      ["poder (to be able to)", ["puedo", "puedes", "puede", "podemos", "podéis", "pueden"]],
      ["querer (to want)", ["quiero", "quieres", "quiere", "queremos", "queréis", "quieren"]],
      ["decir (to say/tell)", ["digo", "dices", "dice", "decimos", "decís", "dicen"]],
      ["venir (to come)", ["vengo", "vienes", "viene", "venimos", "venís", "vienen"]],
      ["saber (to know)", ["sé", "sabes", "sabe", "sabemos", "sabéis", "saben"]],
    ],
    irregularNote: "These verbs show frequent irregularities: stem changes (e→ie, o→ue), an irregular 1st-person form (tengo, hago, digo, sé), or a fully irregular conjugation (ser, ir).",
    extraTip: "💡 Extra tip: the structure « ir a + infinitive » (voy a comer) expresses the near future, just like « going to + infinitive » in English.",
  },
  imperfect: {
    intro: "The imperfect (« pretérito imperfecto ») describes habitual or ongoing actions in the past, with no precise end point (similar to English 'used to' or the past continuous).",
    groups: {
      "-AR (hablar)": ["habl-aba", "habl-abas", "habl-aba", "habl-ábamos", "habl-abais", "habl-aban"],
      "-ER (comer)": ["com-ía", "com-ías", "com-ía", "com-íamos", "com-íais", "com-ían"],
      "-IR (vivir)": ["viv-ía", "viv-ías", "viv-ía", "viv-íamos", "viv-íais", "viv-ían"],
    },
    examples: [
      ["Cuando era niño, jugaba en el parque cada tarde.", "When I was a kid, I used to play in the park every afternoon."],
      ["Mis padres vivían en Barcelona en los años 90.", "My parents used to live in Barcelona in the 90s."],
      ["Nosotros comíamos juntos todos los domingos.", "We used to eat together every Sunday."],
    ],
    tip: "Good to know: the Spanish imperfect is the most regular tense of all — only three verbs are irregular in the entire language!",
    irregulars: [
      ["ser (to be)", ["era", "eras", "era", "éramos", "erais", "eran"]],
      ["ir (to go)", ["iba", "ibas", "iba", "íbamos", "ibais", "iban"]],
      ["ver (to see)", ["veía", "veías", "veía", "veíamos", "veíais", "veían"]],
    ],
    irregularNote: "Every other verb, including those irregular in the present (tener, hacer, poder…), is perfectly regular in the imperfect.",
    extraTip: "💡 Extra tip: the Spanish imperfect is used almost exactly like English 'used to' or the past continuous — to describe, express a past habit, or an ongoing past action.",
  },
  preterite: {
    intro: "The preterite (« pretérito indefinido ») expresses a single, completed action in the past (roughly equivalent to the English simple past).",
    groups: {
      "-AR (hablar)": ["habl-é", "habl-aste", "habl-ó", "habl-amos", "habl-asteis", "habl-aron"],
      "-ER (comer)": ["com-í", "com-iste", "com-ió", "com-imos", "com-isteis", "com-ieron"],
      "-IR (vivir)": ["viv-í", "viv-iste", "viv-ió", "viv-imos", "viv-isteis", "viv-ieron"],
    },
    examples: [
      ["Ayer hablé con mi jefe sobre el proyecto.", "Yesterday I talked to my boss about the project."],
      ["Ella vivió dos años en Argentina.", "She lived in Argentina for two years."],
      ["El año pasado fuimos de vacaciones a México.", "Last year we went on vacation to Mexico."],
    ],
    tip: "Watch out: this is the tense with the most irregularities in Spanish — many very common verbs change their stem (tuve, hice, dije…).",
    irregulars: [
      ["ser / ir", ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"]],
      ["estar (to be)", ["estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron"]],
      ["tener (to have)", ["tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron"]],
      ["hacer (to do/make)", ["hice", "hiciste", "hizo", "hicimos", "hicisteis", "hicieron"]],
      ["poder (to be able to)", ["pude", "pudiste", "pudo", "pudimos", "pudisteis", "pudieron"]],
      ["poner (to put)", ["puse", "pusiste", "puso", "pusimos", "pusisteis", "pusieron"]],
      ["querer (to want)", ["quise", "quisiste", "quiso", "quisimos", "quisisteis", "quisieron"]],
      ["venir (to come)", ["vine", "viniste", "vino", "vinimos", "vinisteis", "vinieron"]],
      ["decir (to say/tell)", ["dije", "dijiste", "dijo", "dijimos", "dijisteis", "dijeron"]],
      ["traer (to bring)", ["traje", "trajiste", "trajo", "trajimos", "trajisteis", "trajeron"]],
      ["dar (to give)", ["di", "diste", "dio", "dimos", "disteis", "dieron"]],
      ["saber (to know)", ["supe", "supiste", "supo", "supimos", "supisteis", "supieron"]],
    ],
    irregularNote: "Note: « ser » and « ir » share the exact same conjugation in the preterite — only context tells them apart (fui = 'I was' or 'I went').",
    extraTip: "💡 Extra tip: in Spain, people often use « he hablado » (present perfect) for a recent action, and the preterite for something more distant or fully finished. In Latin America, the preterite is largely preferred in both cases.",
  },
};

const TRANSLATION_SENTENCES = {
  present: [
    ["I speak Spanish every day.", "Yo hablo español todos los días."],
    ["You eat too fast.", "Tú comes demasiado rápido."],
    ["She lives in Seville.", "Ella vive en Sevilla."],
    ["We have two cars.", "Nosotros tenemos dos coches."],
    ["They go to the movies on Saturdays.", "Ellos van al cine los sábados."],
    ["You (plural) do homework together.", "Vosotros hacéis los deberes juntos."],
    ["I am a Spanish student.", "Yo soy estudiante de español."],
    ["She wants a coffee.", "Ella quiere un café."],
    ["We have lived in Madrid since 2020.", "Nosotros vivimos en Madrid desde 2020."],
    ["Can you help me, please?", "¿Tú puedes ayudarme, por favor?"],
  ],
  imperfect: [
    ["When I was a child, I used to play in the park.", "Cuando era niño, jugaba en el parque."],
    ["My parents used to live in Barcelona.", "Mis padres vivían en Barcelona."],
    ["We used to eat together on Sundays.", "Nosotros comíamos juntos los domingos."],
    ["You used to talk a lot with your grandparents.", "Tú hablabas mucho con tus abuelos."],
    ["She used to go to the beach every summer.", "Ella iba a la playa cada verano."],
    ["You (plural) used to watch TV after dinner.", "Vosotros veíais la tele después de cenar."],
    ["I had a dog when I was little.", "Yo tenía un perro cuando era niño."],
    ["They were very tired.", "Ellos estaban muy cansados."],
    ["We used to study Spanish in high school.", "Nosotros estudiábamos español en el instituto."],
    ["She used to work in Madrid before.", "Ella trabajaba en Madrid antes."],
  ],
  preterite: [
    ["Yesterday, I talked to my boss.", "Ayer hablé con mi jefe."],
    ["She had an accident last month.", "Ella tuvo un accidente el mes pasado."],
    ["We went to Barcelona in 2019.", "Nosotros fuimos a Barcelona en 2019."],
    ["You made dinner last night.", "Tú hiciste la cena anoche."],
    ["They came to the party on Saturday.", "Ellos vinieron a la fiesta el sábado."],
    ["You (plural) told the truth.", "Vosotros dijisteis la verdad."],
    ["I saw that movie last year.", "Yo vi esa película el año pasado."],
    ["She managed to finish the project on time.", "Ella pudo terminar el proyecto a tiempo."],
    ["We had a nice surprise.", "Nosotros tuvimos una buena sorpresa."],
    ["He put the book on the table.", "Él puso el libro en la mesa."],
  ],
};

/* ===========================================================
   Pure conjugation / text-matching logic (unit-testable)
   =========================================================== */

function regularConjugation(verb, tense) {
  const group = verb.slice(-2);
  const stem = verb.slice(0, -2);
  return REGULAR_ENDINGS[tense][group].map((ending) => stem + ending);
}

function getConjugation(verb, tense) {
  if (IRREGULAR_VERBS[verb] && IRREGULAR_VERBS[verb][tense]) {
    return IRREGULAR_VERBS[verb][tense];
  }
  return regularConjugation(verb, tense);
}

function stripAccents(text) {
  return text.normalize("NFKD").replace(/[\u0300-\u036f]/g, "");
}

function normalize(text) {
  return stripAccents(text.trim().toLowerCase());
}

function normalizeSentence(text) {
  let t = normalize(text);
  t = t.replace(/[¿¡?!.,;:]/g, "");
  t = t.replace(/\s+/g, " ").trim();
  return t;
}

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

/* ===========================================================
   Export for Node-based testing (no-op in the browser)
   =========================================================== */
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    PRONOUNS, TENSES, REGULAR_VERBS, IRREGULAR_VERBS, ALL_VERBS, REGULAR_ENDINGS,
    COURSE_DATA, TRANSLATION_SENTENCES,
    regularConjugation, getConjugation, normalize, normalizeSentence, pickRandom,
  };
}

/* ===========================================================
   UI / app wiring (browser only)
   =========================================================== */
if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", initApp);
}

function initApp() {
  /* ---------- Navigation ---------- */
  const views = document.querySelectorAll(".view");
  function showView(name) {
    views.forEach((v) => v.classList.remove("active"));
    document.getElementById(`view-${name}`).classList.add("active");
    if (name !== "game") stopTimer();
  }
  document.querySelectorAll("[data-go]").forEach((el) => {
    el.addEventListener("click", () => showView(el.dataset.go));
  });
  document.getElementById("card-game").addEventListener("click", () => {
    showView("game");
    newQuestion();
  });
  document.getElementById("card-course").addEventListener("click", () => showView("course"));
  document.getElementById("card-translate").addEventListener("click", () => {
    showView("translate");
    newSentence();
  });

  /* =========================================================
     GAME
     ========================================================= */
  let score = 0, total = 0, streak = 0, bestStreak = 0;
  let timeLeft = DURATION_QUESTION, timerId = null;
  let reviewingAnswer = false, allPersonsMode = false;
  let currentVerb = null, currentTense = null, pronounIdx = null, correctAnswer = null;
  let tenseFilter = null;
  let allPersonsOn = false;

  const gameHeader = document.getElementById("game-header");
  const gameTitle = document.getElementById("game-title");
  const gameSubtitle = document.getElementById("game-subtitle");
  const gameTimer = document.getElementById("game-timer");
  const gameScore = document.getElementById("game-score");
  const gameStreak = document.getElementById("game-streak");
  const gameCard = document.getElementById("game-card");
  const gameResult = document.getElementById("game-result");
  const gameSubmit = document.getElementById("game-submit");
  const gameTenseFilterBar = document.getElementById("game-tense-filter");
  const allPersonsBtn = document.getElementById("game-all-persons-btn");

  const tenseChoices = [["🔀 All tenses", null]].concat(
    TENSES.map((t) => [`${TENSE_EMOJI[t]} ${t[0].toUpperCase()}${t.slice(1)}`, t])
  );
  tenseChoices.forEach(([label, value]) => {
    const btn = document.createElement("button");
    btn.className = "chip";
    btn.textContent = label;
    btn.addEventListener("click", () => {
      tenseFilter = value;
      refreshTenseChips();
    });
    btn.dataset.value = value === null ? "" : value;
    gameTenseFilterBar.appendChild(btn);
  });
  function refreshTenseChips() {
    [...gameTenseFilterBar.children].forEach((btn) => {
      const v = btn.dataset.value === "" ? null : btn.dataset.value;
      const active = v === tenseFilter;
      btn.classList.toggle("active", active);
      btn.style.background = active ? (v ? TENSE_COLORS[v] : "#4B3621") : "white";
    });
  }
  refreshTenseChips();

  allPersonsBtn.addEventListener("click", () => {
    allPersonsOn = !allPersonsOn;
    refreshAllPersonsBtn();
  });
  function refreshAllPersonsBtn() {
    if (allPersonsOn) {
      allPersonsBtn.textContent = "🌾 All persons: ON";
      allPersonsBtn.style.background = "#A0522D";
      allPersonsBtn.style.color = "white";
    } else {
      allPersonsBtn.textContent = "🌾 All persons: OFF";
      allPersonsBtn.style.background = "white";
      allPersonsBtn.style.color = "#4B3621";
    }
  }
  refreshAllPersonsBtn();

  function newQuestion() {
    stopTimer();
    reviewingAnswer = false;
    gameResult.textContent = "";

    currentVerb = pickRandom(ALL_VERBS);
    currentTense = tenseFilter !== null ? tenseFilter : pickRandom(TENSES);
    allPersonsMode = allPersonsOn;

    const conj = getConjugation(currentVerb, currentTense);
    if (allPersonsMode) {
      correctAnswer = conj;
      pronounIdx = null;
    } else {
      pronounIdx = Math.floor(Math.random() * 6);
      correctAnswer = conj[pronounIdx];
    }

    updateHeader();
    renderQuestion();
    startTimer();
  }

  function updateHeader() {
    const color = TENSE_COLORS[currentTense];
    gameHeader.style.background = color;
    gameTitle.textContent = `${TENSE_EMOJI[currentTense]} ${currentTense.toUpperCase()}`;
    gameSubtitle.textContent = TENSE_SUBTITLES[currentTense];
    gameCard.style.borderColor = color;
    gameSubmit.style.background = color;
  }

  function renderQuestion() {
    gameCard.innerHTML = "";
    const verbEl = document.createElement("div");
    verbEl.className = "q-verb";
    verbEl.textContent = `📝 Verb: ${currentVerb}`;
    gameCard.appendChild(verbEl);

    if (allPersonsMode) {
      const instr = document.createElement("div");
      instr.className = "q-instruction";
      instr.style.color = "#A0522D";
      instr.textContent = "🌾 Conjugate the verb for ALL persons:";
      gameCard.appendChild(instr);

      const grid = document.createElement("div");
      grid.className = "all-persons-grid";
      PRONOUNS.forEach((pronoun, i) => {
        const row = document.createElement("div");
        row.className = "all-persons-row";
        const label = document.createElement("label");
        label.textContent = pronoun;
        const input = document.createElement("input");
        input.type = "text";
        input.autocomplete = "off";
        input.autocapitalize = "off";
        input.spellcheck = false;
        input.dataset.idx = i;
        const fb = document.createElement("span");
        fb.className = "fb";
        row.appendChild(label);
        row.appendChild(input);
        row.appendChild(fb);
        grid.appendChild(row);
      });
      gameCard.appendChild(grid);
      grid.querySelector("input").focus();
    } else {
      const instr = document.createElement("div");
      instr.className = "q-instruction";
      instr.textContent = `👉 Conjugate for: « ${PRONOUNS[pronounIdx]} »`;
      gameCard.appendChild(instr);

      const input = document.createElement("input");
      input.type = "text";
      input.autocomplete = "off";
      input.autocapitalize = "off";
      input.spellcheck = false;
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") handleSubmit();
      });
      gameCard.appendChild(input);
      setTimeout(() => input.focus(), 50);
    }
  }

  function startTimer() {
    timeLeft = DURATION_QUESTION;
    updateTimerLabel();
    timerId = setInterval(() => {
      timeLeft -= 1;
      if (timeLeft <= 0) {
        stopTimer();
        grade(true);
        return;
      }
      updateTimerLabel();
    }, 1000);
  }
  function updateTimerLabel() {
    gameTimer.textContent = `${timeLeft}s`;
    gameTimer.style.color = timeLeft <= 10 ? "#F3C6B0" : "white";
  }
  function stopTimer() {
    if (timerId !== null) {
      clearInterval(timerId);
      timerId = null;
    }
  }

  function handleSubmit() {
    if (reviewingAnswer) {
      newQuestion();
    } else {
      stopTimer();
      grade(false);
    }
  }
  gameSubmit.addEventListener("click", handleSubmit);

  function grade(timeout) {
    reviewingAnswer = true;
    total += 1;

    if (allPersonsMode) {
      const inputs = [...gameCard.querySelectorAll("input")];
      const rows = [...gameCard.querySelectorAll(".all-persons-row")];
      let nbCorrect = 0;
      inputs.forEach((input, i) => {
        const value = timeout ? "" : input.value;
        const correct = correctAnswer[i];
        const ok = normalize(value) === normalize(correct);
        input.disabled = true;
        const fb = rows[i].querySelector(".fb");
        if (ok) {
          nbCorrect += 1;
          fb.textContent = `✅ ${correct}`;
          fb.style.color = "#4C7A3D";
        } else {
          fb.textContent = `❌ ${correct}`;
          fb.style.color = "#A0522D";
        }
      });
      const perfect = nbCorrect === 6;
      if (perfect) {
        score += 1;
        streak += 1;
        bestStreak = Math.max(bestStreak, streak);
        gameResult.textContent = `${pickRandom(CORRECT_MESSAGES)} All 6 forms are correct!`;
        gameResult.style.color = "#4C7A3D";
      } else {
        streak = 0;
        const msg = pickRandom(timeout ? TIMEOUT_MESSAGES : WRONG_MESSAGES);
        gameResult.textContent = `${msg} (${nbCorrect}/6 forms correct)`;
        gameResult.style.color = "#A0522D";
      }
    } else {
      const input = gameCard.querySelector("input");
      const value = timeout ? "" : input.value;
      const ok = normalize(value) === normalize(correctAnswer);
      input.disabled = true;
      if (ok) {
        score += 1;
        streak += 1;
        bestStreak = Math.max(bestStreak, streak);
        gameResult.textContent = pickRandom(CORRECT_MESSAGES);
        gameResult.style.color = "#4C7A3D";
      } else {
        streak = 0;
        const msg = pickRandom(timeout ? TIMEOUT_MESSAGES : WRONG_MESSAGES);
        gameResult.textContent = `${msg} The correct answer was: ${correctAnswer}`;
        gameResult.style.color = "#A0522D";
      }
    }

    gameScore.textContent = `🏆 Score: ${score}/${total}`;
    gameStreak.textContent = streak >= 2 ? `🔥 Streak: ${streak}` : "";
    gameSubmit.textContent = "▶ Next question";
  }

  /* =========================================================
     COURSE
     ========================================================= */
  const courseSections = document.getElementById("course-sections");
  TENSES.forEach((tense) => courseSections.appendChild(buildCourseSection(tense)));

  function buildCourseSection(tense) {
    const data = COURSE_DATA[tense];
    const color = TENSE_COLORS[tense];
    const emoji = TENSE_EMOJI[tense];

    const card = document.createElement("div");
    card.className = "course-card";
    card.style.borderColor = color;

    const banner = document.createElement("div");
    banner.className = "course-banner";
    banner.style.background = color;
    banner.innerHTML = `<div class="t">${emoji} ${tense.toUpperCase()}</div><div class="s">${TENSE_SUBTITLES[tense]}</div>`;
    card.appendChild(banner);

    const body = document.createElement("div");
    body.className = "course-body";

    body.appendChild(h3("Formation rules (regular verbs)"));
    body.appendChild(p(data.intro));
    body.appendChild(groupsTable(data.groups, color));

    body.appendChild(h3("Examples"));
    data.examples.forEach(([es, en]) => {
      const ex = document.createElement("div");
      ex.className = "course-example";
      ex.innerHTML = `<b>${escapeHtml(es)}</b><br>${escapeHtml(en)}`;
      body.appendChild(ex);
    });

    body.appendChild(tip(data.tip));

    body.appendChild(h3("Irregular verbs you'll use most"));
    const swipeHint = document.createElement("div");
    swipeHint.className = "course-tip";
    swipeHint.style.marginBottom = "2px";
    swipeHint.textContent = "↔ swipe the table sideways to see every person";
    body.appendChild(swipeHint);
    body.appendChild(irregularsTable(data.irregulars, color));
    body.appendChild(tip(data.irregularNote));

    const extraBox = document.createElement("div");
    extraBox.className = "extra-tip-box";
    extraBox.textContent = data.extraTip;
    body.appendChild(extraBox);

    const practiceBtn = document.createElement("button");
    practiceBtn.className = "practice-btn";
    practiceBtn.style.background = color;
    practiceBtn.textContent = `🥾 Practice the ${tense} tense ▶`;
    practiceBtn.addEventListener("click", () => {
      tenseFilter = tense;
      refreshTenseChips();
      document.getElementById("view-course").classList.remove("active");
      document.getElementById("view-game").classList.add("active");
      newQuestion();
    });
    body.appendChild(practiceBtn);

    card.appendChild(body);
    return card;
  }

  function h3(text) {
    const el = document.createElement("div");
    el.className = "course-h3";
    el.textContent = text;
    return el;
  }
  function p(text) {
    const el = document.createElement("div");
    el.className = "course-p";
    el.textContent = text;
    return el;
  }
  function tip(text) {
    const el = document.createElement("div");
    el.className = "course-tip";
    el.textContent = text;
    return el;
  }
  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function groupsTable(groups, color) {
    const wrap = document.createElement("div");
    wrap.className = "table-wrap groups";
    const table = document.createElement("table");
    table.className = "mini-table";
    const names = Object.keys(groups);
    const thead = document.createElement("tr");
    thead.innerHTML = `<th style="background:${color}"></th>` +
      names.map((n) => `<th style="background:${color}">${n}</th>`).join("");
    table.appendChild(thead);
    PRONOUNS.forEach((pronoun, i) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td class="row-label">${pronoun}</td>` +
        names.map((n) => `<td>${groups[n][i]}</td>`).join("");
      table.appendChild(tr);
    });
    wrap.appendChild(table);
    return wrap;
  }

  function irregularsTable(irregulars, color) {
    const wrap = document.createElement("div");
    wrap.className = "table-wrap";
    const table = document.createElement("table");
    table.className = "mini-table";
    const headers = ["Infinitive"].concat(PRONOUNS);
    const thead = document.createElement("tr");
    thead.innerHTML = headers.map((h) => `<th style="background:${color}">${h}</th>`).join("");
    table.appendChild(thead);
    irregulars.forEach(([infinitive, forms]) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td class="row-label">${infinitive}</td>` +
        forms.map((f) => `<td>${f}</td>`).join("");
      table.appendChild(tr);
    });
    wrap.appendChild(table);
    return wrap;
  }

  /* =========================================================
     TRANSLATION
     ========================================================= */
  let scoreTranslation = 0, totalTranslation = 0;
  let translationReviewing = false;
  let translationSentenceEn = null, translationSentenceEs = null, translationTense = null;
  let translationTenseFilter = null;

  const translateTenseFilterBar = document.getElementById("translate-tense-filter");
  const translateScore = document.getElementById("translate-score");
  const translateCard = document.getElementById("translate-card");
  const translateResult = document.getElementById("translate-result");
  const translateSubmit = document.getElementById("translate-submit");

  tenseChoices.forEach(([label, value]) => {
    const btn = document.createElement("button");
    btn.className = "chip";
    btn.textContent = label;
    btn.dataset.value = value === null ? "" : value;
    btn.addEventListener("click", () => {
      translationTenseFilter = value;
      refreshTranslateChips();
    });
    translateTenseFilterBar.appendChild(btn);
  });
  function refreshTranslateChips() {
    [...translateTenseFilterBar.children].forEach((btn) => {
      const v = btn.dataset.value === "" ? null : btn.dataset.value;
      const active = v === translationTenseFilter;
      btn.classList.toggle("active", active);
      btn.style.background = active ? (v ? TENSE_COLORS[v] : "#4B3621") : "white";
    });
  }
  refreshTranslateChips();

  function newSentence() {
    translationReviewing = false;
    translateResult.textContent = "";

    translationTense = translationTenseFilter !== null ? translationTenseFilter : pickRandom(TENSES);
    const [en, es] = pickRandom(TRANSLATION_SENTENCES[translationTense]);
    translationSentenceEn = en;
    translationSentenceEs = es;

    translateCard.innerHTML = "";
    const hint = document.createElement("div");
    hint.className = "q-hint";
    hint.textContent = `${TENSE_EMOJI[translationTense]} Tense requested: ${translationTense}`;
    translateCard.appendChild(hint);

    const sentence = document.createElement("div");
    sentence.className = "q-verb";
    sentence.style.fontSize = "18px";
    sentence.textContent = translationSentenceEn;
    translateCard.appendChild(sentence);

    const input = document.createElement("input");
    input.type = "text";
    input.autocomplete = "off";
    input.autocapitalize = "off";
    input.spellcheck = false;
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") handleTranslateSubmit();
    });
    translateCard.appendChild(input);
    setTimeout(() => input.focus(), 50);
  }

  function handleTranslateSubmit() {
    if (translationReviewing) {
      newSentence();
    } else {
      gradeTranslation();
    }
  }
  translateSubmit.addEventListener("click", handleTranslateSubmit);

  function gradeTranslation() {
    translationReviewing = true;
    totalTranslation += 1;

    const input = translateCard.querySelector("input");
    const answer = input.value;
    const ok = normalizeSentence(answer) === normalizeSentence(translationSentenceEs);
    input.disabled = true;

    if (ok) {
      scoreTranslation += 1;
      translateResult.textContent = pickRandom(CORRECT_MESSAGES);
      translateResult.style.color = "#4C7A3D";
    } else {
      const msg = pickRandom(WRONG_MESSAGES);
      translateResult.textContent = `${msg} Expected translation: ${translationSentenceEs}`;
      translateResult.style.color = "#A0522D";
    }

    translateScore.textContent = `🏆 Score: ${scoreTranslation}/${totalTranslation}`;
    translateSubmit.textContent = "▶ Next sentence";
  }

  /* ---------- Register service worker (offline support) ---------- */
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("service-worker.js").catch(() => {
        /* offline support is a bonus, ignore registration failures */
      });
    });
  }
}
