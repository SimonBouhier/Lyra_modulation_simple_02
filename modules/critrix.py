def critrix(stimulus: float, threshold: float = 0.7) -> dict:
    """
    Déclenche une friction si la tension dépasse un seuil.
    """
    triggered = stimulus > threshold
    return {
        "friction_triggered": triggered,
        "stimulus": stimulus,
        "threshold": threshold,
        "meta": {
            "rupture_level": max(0.0, stimulus - threshold) if triggered else 0.0
        }
    }
