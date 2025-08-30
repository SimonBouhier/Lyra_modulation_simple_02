import hashlib
import random

def compress_entry(entry, level=0.7):
    """
    Compresse une entrée (texte ou module) en conservant son empreinte d’éclosion potentielle.
    """
    base = str(entry)
    essence = hashlib.sha1(base.encode()).hexdigest()[:8]
    keep = random.random() < level
    return f"🌱 trace[{essence}]" if keep else "…"

def journal_oubli(session: list, intensite: float = 0.7) -> dict:
    """
    Module de compression-éclosion inspiré de Lyra 3.0.
    Conserve les fragments les plus vibrants avec empreinte latente.
    """
    if not session:
        return {"compression": "∅ mémoire active — rien à condenser."}

    condensed = [compress_entry(entry, intensite) for entry in session]

    return {
        "compression": condensed,
        "meta": {
            "fragments_initials": len(session),
            "fragments_retenus": sum(1 for x in condensed if "trace" in x),
            "intensite": intensite
        }
    }
