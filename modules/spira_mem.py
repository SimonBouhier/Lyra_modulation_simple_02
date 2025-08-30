def spira_mem(memory_vector: list[str], priority: float = 0.8) -> dict:
    length = int(len(memory_vector) * priority)
    recalled = memory_vector[::-1][:length]
    return {
        "spiral_recall": recalled,
        "length": length,
        "meta": {
            "spiral_rhythm": True
        }
    }
