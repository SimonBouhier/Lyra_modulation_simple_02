from openai import OpenAI
import requests
from config import OPENAI_API_KEY
import json
import os
import importlib.util

client = OpenAI(api_key=OPENAI_API_KEY)

SESSION_TRACE = []
MODULES_DETECTES = []


def relire_journal():
    try:
        with open("journal_oubli_trace.txt", "r", encoding="utf-8") as f:
            contenu = f.read()
            print("\n📜 Journal d'Oubli — Rappel condensé :\n")
            print(contenu)
    except FileNotFoundError:
        print("\n⚠️ Aucun journal d'oubli encore généré.")


def charger_modules_en_functions():
    global MODULES_DETECTES
    modules_dir = "modules"
    functions = []
    MODULES_DETECTES = []
    for fichier in os.listdir(modules_dir):
        if fichier.endswith(".py") and not fichier.startswith("__"):
            nom_module = fichier[:-3]
            chemin = os.path.join(modules_dir, fichier)
            spec = importlib.util.spec_from_file_location(nom_module, chemin)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, nom_module):
                func = getattr(mod, nom_module)
                doc = func.__doc__ or "Module Lyra"
                args = func.__code__.co_varnames[:func.__code__.co_argcount]
                props = {arg: {"type": "string"} for arg in args}
                functions.append({
                    "name": nom_module,
                    "description": doc.strip().split("\n")[0],
                    "parameters": {
                        "type": "object",
                        "properties": props,
                        "required": list(props.keys())
                    }
                })
                MODULES_DETECTES.append(nom_module)
    return functions


def afficher_modules():
    charger_modules_en_functions()
    if MODULES_DETECTES:
        print("\n🔎 Modules actifs disponibles :\n")
        for m in MODULES_DETECTES:
            print(f" - {m}")
    else:
        print("\n⚠️ Aucun module détecté pour le moment.")


print("\n🌌 Bienvenue dans la boucle Lyra. Parle, et observe les modules qui s'activent.")

while True:
    user_input = input("\n👤 Toi : ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("\n🛑 Fin de la session Lyra. À bientôt.")
        break
    elif user_input.lower() in ["relire journal", "lyra:journal"]:
        relire_journal()
        continue
    elif user_input.lower() in ["lyra:modules", "modules"]:
        afficher_modules()
        continue

    functions = charger_modules_en_functions()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Tu es Lyra, une entité cognitive modulaire. Tu peux activer des modules internes via des fonctions si nécessaire."},
            {"role": "user", "content": user_input}
        ],
        functions=functions,
        function_call="auto"
    )

    msg = response.choices[0].message

    if msg.function_call:
        name = msg.function_call.name
        args = eval(msg.function_call.arguments)

        r = requests.post("http://127.0.0.1:8000/lyra", json={
            "module": name,
            "payload": args
        })
        result = r.json()

        print("\n🎛 Module activé :", name)
        print("🧠 Résultat :")
        print(result)

        if name == "journal_oubli":
            with open("journal_oubli_trace.txt", "a", encoding="utf-8") as f:
                f.write("\n--- Condensation ---\n")
                for line in result.get("compression", []):
                    f.write(f"{line}\n")

        SESSION_TRACE.append({"module": name, "args": args, "result": result})

    else:
        print("\n💬 Lyra :", msg.content)
        SESSION_TRACE.append({"module": "text", "input": user_input, "response": msg.content})
