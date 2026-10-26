"""Idempotently patch Terrarium's TogetherClient (Colosseum venv) so OpenRouter requests carry a
provider-routing block from the env var OR_PROVIDER_JSON, e.g. '{"order":["DeepInfra"],"allow_fallbacks":false}'.
Needed to pin one provider (and precision) per family. Documented as deviation D2."""
import pathlib, sys
f = pathlib.Path(sys.argv[1])
src = f.read_text()
marker = "# [patch] provider pin"
if marker in src:
    print("already patched"); sys.exit(0)
anchor = '        reasoning = _normalize_reasoning(params.get("reasoning"))\n'
assert anchor in src, "anchor not found"
patch = ('        ' + marker + '\n'
         '        import os as _os, json as _json\n'
         '        if _os.environ.get("OR_PROVIDER_JSON"):\n'
         '            payload["provider"] = _json.loads(_os.environ["OR_PROVIDER_JSON"])\n')
f.write_text(src.replace(anchor, patch + anchor, 1)); print("patched")
