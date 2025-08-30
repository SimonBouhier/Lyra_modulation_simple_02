def echo_synth(signal: str, intensity: float = 1.0) -> dict:
    modulated = ''.join(
        c.upper() if i % 2 == 0 else c.lower()
        for i, c in enumerate(signal)
    )
    return {
        "modulated_signal": modulated,
        "intensity": intensity,
        "meta": {
            "fractal_closure": True
        }
    }
