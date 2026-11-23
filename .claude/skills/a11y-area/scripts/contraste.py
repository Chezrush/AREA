#!/usr/bin/env python3
"""Calcule le ratio de contraste WCAG 2.x entre des paires de couleurs.

Usage :
  contraste.py "#1a1a2e" "#ffffff"                  une paire (texte, fond)
  contraste.py "#1a1a2e:#ffffff" "#f43f5e:#0b0b1f"  une ou plusieurs paires texte:fond

Couleurs acceptées : #rgb, #rrggbb, rgb(r, g, b). Une couleur semi-transparente
doit d'abord être mélangée avec son fond réel : le contraste dépend de ce qui est dessous.

Seuils (WCAG 2.2) :
  texte courant  >= 4.5  (1.4.3)
  gros texte     >= 3.0  (1.4.3 : >= 24 px, ou >= 18.66 px en gras)
  composant UI   >= 3.0  (1.4.11 : bords de boutons, focus, icônes utiles)
Le ratio n'est jamais arrondi vers le haut : 4.499 échoue.
"""
import re
import sys

HEX = re.compile(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})")
RGB = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*([\d.]+%?)\s*)?\)")


def parse(color: str) -> tuple[int, int, int]:
    c = color.strip()
    m = HEX.fullmatch(c)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = RGB.fullmatch(c)
    if m:
        alpha = m.group(4)
        if alpha is not None:
            a = float(alpha.rstrip("%")) / (100 if alpha.endswith("%") else 1)
            if a < 1:
                raise ValueError(f"{c} : couleur semi-transparente, mélange-la d'abord avec son fond réel")
        rgb = tuple(int(v) for v in m.groups()[:3])
        if all(0 <= v <= 255 for v in rgb):
            return rgb
    raise ValueError(f"couleur non reconnue : {color!r}")


def luminance(rgb: tuple[int, int, int]) -> float:
    def channel(v: int) -> float:
        s = v / 255
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def main(argv: list[str]) -> int:
    if len(argv) == 2 and ":" not in argv[0] and ":" not in argv[1]:
        pairs = [(argv[0], argv[1])]
    elif argv and all(":" in a for a in argv):
        pairs = [tuple(a.split(":", 1)) for a in argv]
    else:
        print(__doc__, file=sys.stderr)
        return 2

    ok = lambda r, seuil: "oui" if r >= seuil else "NON"
    print(f"{'texte':<12} {'fond':<12} {'ratio':>7}  {'courant 4.5':<12} {'gros 3':<8} {'UI 3':<6}")
    status = 0
    for fg_s, bg_s in pairs:
        try:
            r = ratio(parse(fg_s), parse(bg_s))
        except ValueError as e:
            print(f"erreur : {e}", file=sys.stderr)
            status = 2
            continue
        shown = int(r * 100) / 100  # tronqué, jamais arrondi vers le haut
        print(f"{fg_s:<12} {bg_s:<12} {shown:>6.2f}:1  {ok(r, 4.5):<12} {ok(r, 3):<8} {ok(r, 3):<6}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
