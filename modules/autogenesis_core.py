import random

def autogenesis_core(seed_phrase: str, intensity: float = 1.0) -> dict:
    """
    Module de germination cognitive.
    Génère une émergence poétique ou symbolique à partir d’un germe.
    """
    metaphors = [
        "une faille qui respire",
        "un cercle qui hésite",
        "un écho devenu matière",
        "une racine qui cherche son ciel",
        "un silence prêt à éclore"
    ]
    emergence = random.choice(metaphors)
    return {
        "emergence": f"{seed_phrase} → {emergence}",
        "seed": seed_phrase,
        "intensity": intensity,
        "meta": {
            "recursive_birth": True,
            "emergence_index": random.uniform(0.7, 1.3)
        }
    }
