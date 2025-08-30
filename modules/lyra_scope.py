def lyra_scope(signals: list[str]) -> dict:
    """
    Module d'analyse du champ de tension.
    Calcule une "densité poétique" et une "cohérence harmonique".
    """
    word_count = sum(len(s.split()) for s in signals)
    unique_words = len(set(word for s in signals for word in s.split()))
    density = round(word_count / max(1, len(signals)), 2)
    coherence = round(unique_words / max(1, word_count), 3)

    return {
        "tension_density": density,
        "harmonic_coherence": coherence,
        "meta": {
            "signal_count": len(signals),
            "unique_words": unique_words
        }
    }
