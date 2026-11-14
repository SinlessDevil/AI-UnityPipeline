"""Build an offline Before/After gallery from a UI sprite run manifest."""

import argparse
import html
import json
from pathlib import Path


CAPTIONS = {
    "en": (
        "Reference", "Assembled screen", "Layout preview", "Before · previous PNG",
        "Before · reference crop", "After · Unity PNG", "Pending export",
        "Cutout comparison", "Before · original mask", "After · refined mask", "Unity sprites",
    ),
    "ru": (
        "Референс", "Собранный экран", "Схема сборки", "До · предыдущий PNG",
        "До · фрагмент референса", "После · PNG для Unity", "Экспорт ожидается",
        "Сравнение вырезания", "До · исходная маска", "После · уточнённая маска", "Спрайты Unity",
    ),
}

STYLE = """
:root{color-scheme:dark;font:16px system-ui;background:#191d25;color:#f5f0e6}
body{max-width:1260px;margin:32px auto;padding:0 20px}
h1,h2,h3{overflow-wrap:anywhere} h3{font-size:1rem;margin:0}
p{margin:.65rem 0 0} a{color:#a8daff}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:14px}
.pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
article{background:#252c35;border-radius:9px;padding:14px}
article .pair{margin-top:10px}
figure{margin:0;min-width:0} figcaption{font-size:.82rem;margin-bottom:6px}
.tile{display:grid;grid-template: minmax(0,1fr) / minmax(0,1fr);place-items:center;height:148px;background:
  repeating-conic-gradient(#848c98 0% 25%,#aeb7c1 0% 50%) 0/20px 20px}
.tile img{max-width:100%;max-height:100%;object-fit:contain;display:block}
.screens .tile{height:clamp(110px,34vw,420px)}
.pending{background:#303943;text-align:center;padding:0 5px}
"""


def render(run, data):
    language = data.get("language", "en")
    (reference, assembled, layout, previous, crop, exported, pending,
     cutout, original_mask, refined_mask, sprites) = CAPTIONS.get(language, CAPTIONS["en"])

    def panel(label, path):
        link = Path(path)
        target = (run / link).resolve()
        if link.is_absolute() or not target.is_relative_to(run) or not target.is_file():
            raise ValueError(f"Image must exist inside the run folder: {path}")
        url = html.escape(target.as_uri().removeprefix(run.as_uri().rstrip("/") + "/"), quote=True)
        label = html.escape(label)
        return (f'<figure><figcaption>{label}</figcaption><a class="tile" href="{url}">'
                f'<img loading="lazy" src="{url}" alt="{label}"></a></figure>')

    def pair(left, right):
        return f'<div class="pair">{left}{right}</div>'

    def card(item_id, panels, note=""):
        suffix = f"<p>{html.escape(note)}</p>" if note else ""
        return f"<article><h3>{html.escape(item_id)}</h3>{panels}{suffix}</article>"

    screen = pair(panel(reference, data["reference_image"]),
                  panel(layout if data.get("preview_is_layout") else assembled, data["assembled_image"]))
    assets = []
    for item in data["assets"]:
        if item["method"] == "LIVE_UI":
            continue
        baseline = item.get("previous_png")
        left = panel(previous, baseline) if baseline else panel(crop, item["reference_crop"])
        output = item.get("unity_png")
        if output:
            right = panel(exported, output)
        else:
            right = (f'<figure><figcaption>{exported}</figcaption>'
                     f'<div class="tile pending">{pending}</div></figure>')
        note = " · ".join([item["method"], item["status"], *item.get("issues", [])])
        assets.append(card(item["id"], pair(left, right), note))

    comparisons = [
        card(item["id"], pair(panel(original_mask, item["before_png"]),
                              panel(refined_mask, item["after_png"])))
        for item in data.get("cutout_comparisons", [])
    ]
    title = html.escape(data.get("title", "Unity UI Assets"))
    page = (f'<!doctype html><html lang="{html.escape(language, quote=True)}">'
            '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{title}</title><style>{STYLE}</style><h1>{title}</h1><section class="screens">{screen}</section>')
    if comparisons:
        page += f'<h2>{cutout}</h2><section class="grid">{"".join(comparisons)}</section>'
    return page + f'<h2>{sprites}</h2><main class="grid">{"".join(assets)}</main></html>'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    manifest = args.manifest.resolve()
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        page = render(manifest.parent, data)
        target = manifest.with_name("Gallery.html")
        target.write_text(page, encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Gallery build failed: {error}\n")
    print(target)


if __name__ == "__main__":
    main()
