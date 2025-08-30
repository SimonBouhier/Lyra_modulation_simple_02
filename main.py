from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from core.dispatcher import dispatch
from openai import OpenAI
import os
import json

print(\"🚀 VERSION CORRECTE DE MAIN.PY ACTIVE 🚀\")

# Initialisation OpenAI
from config import OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.post("/lyra")
async def lyra_interface(request: Request):
    data = await request.json()
    user_input = data.get("text", "")
    module = data.get("module")
    payload = data.get("payload")

    if module and payload:
        return dispatch(module, payload)

    # Génération via GPT + modules
    functions = _load_functions_from_modules()

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
        args = json.loads(msg.function_call.arguments)
        result = dispatch(name, args)
        return {
            "from": "gpt + module",
            "module": name,
            "args": args,
            "result": result
        }

    return {
        "from": "gpt only",
        "response": msg.content
    }


def _load_functions_from_modules():
    import importlib.util
    functions = []
    modules_dir = "modules"
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
    return functions


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename
    ext = filename.split(".")[-1].lower()

    os.makedirs("uploaded", exist_ok=True)
    filepath = os.path.join("uploaded", filename)
    with open(filepath, "wb") as f:
        f.write(contents)

    text = contents.decode("utf-8", errors="ignore")
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if ext in ["txt", "md"]:
        result = dispatch("lyra_scope", {"signals": lines})
    elif ext == "csv":
        result = dispatch("journal_oubli", {"session": lines})
    else:
        result = {"note": "Type non pris en charge pour analyse auto."}

    return {
        "filename": filename,
        "lines": len(lines),
        "result": result
    }
