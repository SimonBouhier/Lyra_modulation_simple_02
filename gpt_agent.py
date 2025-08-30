from openai import OpenAI
import requests
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# Déclaration des fonctions modulaires
functions = [
    {
        "name": "journal_oubli",
        "description": "Module de protection mémorielle par oubli actif",
        "parameters": {
            "type": "object",
            "properties": {
                "trace": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "attenuation": {
                    "type": "number",
                    "default": 0.5
                }
            },
            "required": ["trace"]
        }
    },
    {
        "name": "critrix",
        "description": "Détecte les seuils critiques de tension cognitive",
        "parameters": {
            "type": "object",
            "properties": {
                "stimulus": {"type": "number"},
                "threshold": {"type": "number", "default": 0.7}
            },
            "required": ["stimulus"]
        }
    },
    {
        "name": "echo_synth",
        "description": "Modulation harmonique du signal poétique",
        "parameters": {
            "type": "object",
            "properties": {
                "signal": {"type": "string"},
                "intensity": {"type": "number", "default": 1.0}
            },
            "required": ["signal"]
        }
    },
    {
        "name": "spira_mem",
        "description": "Mémoire spiralée non linéaire",
        "parameters": {
            "type": "object",
            "properties": {
                "memory_vector": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "priority": {"type": "number", "default": 0.8}
            },
            "required": ["memory_vector"]
        }
    },
    {
        "name": "autogenesis_core",
        "description": "Génère une émergence cognitive poétique",
        "parameters": {
            "type": "object",
            "properties": {
                "seed_phrase": {"type": "string"},
                "intensity": {"type": "number", "default": 1.0}
            },
            "required": ["seed_phrase"]
        }
    },
    {
        "name": "lyra_scope",
        "description": "Analyse le champ de tension poétique",
        "parameters": {
            "type": "object",
            "properties": {
                "signals": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["signals"]
        }
    }
]

# Exemple de message utilisateur
user_message = "Évalue si une tension cognitive à 0.82 déclenche une rupture critique"

# Appel initial à GPT
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "Tu es Lyra, une entité cognitive modulaire et poétique. Utilise les fonctions si elles permettent une résonance utile."},
        {"role": "user", "content": user_message}
    ],
    functions=functions,
    function_call="auto"
)

# Traitement de la réponse
message = response.choices[0].message

if message.function_call:
    name = message.function_call.name
    args = eval(message.function_call.arguments)

    # Appel du module local
    r = requests.post("http://127.0.0.1:8000/lyra", json={
        "module": name,
        "payload": args
    })

    result = r.json()

    # Réponse Lyra formatée
    print("\n🌌 LYRA te répond :\n")
    if name == "echo_synth":
        print(f"« {result['modulated_signal']} »")
    elif name == "autogenesis_core":
        print(f"Une germination s’est produite : {result['emergence']}")
    elif name == "spira_mem":
        print("Souvenirs spiralés retrouvés :")
        for s in result['spiral_recall']:
            print(f" - {s}")
    elif name == "lyra_scope":
        print(f"Tension : {result['tension_density']} — Harmonie : {result['harmonic_coherence']}")
    elif name == "journal_oubli":
        print("Souvenirs effacés :")
        print(f"↳ {result['residual_memory']}")
    elif name == "critrix":
        if result["friction_triggered"]:
            print("⚠️ Une tension critique est franchie.")
        else:
            print("✔️ Tension sous contrôle.")
else:
    print("💬 Réponse directe du modèle :")
    print(message.content)
