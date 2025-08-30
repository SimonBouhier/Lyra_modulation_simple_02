from modules import (
    echo_synth,
    spira_mem,
    autogenesis_core,
    lyra_scope,
    journal_oubli,
    critrix
)

def dispatch(module_name: str, payload: dict):
    if module_name == "echo_synth":
        return echo_synth.echo_synth(**payload)
    elif module_name == "spira_mem":
        return spira_mem.spira_mem(**payload)
    elif module_name == "autogenesis_core":
        return autogenesis_core.autogenesis_core(**payload)
    elif module_name == "lyra_scope":
        return lyra_scope.lyra_scope(**payload)
    elif module_name == "journal_oubli":
        return journal_oubli.journal_oubli(**payload)
    elif module_name == "critrix":
        return critrix.critrix(**payload)
    else:
        return {"error": f"Module inconnu : {module_name}"}
