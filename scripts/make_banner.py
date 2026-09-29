"""Genera assets/banner-{dark,light}.svg: splash con el logo JH y una terminal que escribe tres comandos."""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(bg="#0d1117", border="#30363d", bar="#161b22", title="#9198a1",
                 prompt="#3fb950", cmd="#e6edf3", out="#c9d1d9", accent="#58a6ff", muted="#9198a1",
                 g1="#58a6ff", g2="#bc8cff", g3="#ff7b72", shadow="#6e7681"),
    "light": dict(bg="#ffffff", border="#d0d7de", bar="#f6f8fa", title="#59636e",
                  prompt="#1a7f37", cmd="#1f2328", out="#31363c", accent="#0969da", muted="#59636e",
                  g1="#0969da", g2="#8250df", g3="#cf222e", shadow="#8c959f"),
}

W, FS, CW = 860, 17, 10.2          # ancho, tamaño de fuente, ancho de carácter (0.6em)
X0, PROMPT = 26, "~ $ "
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
TYPE = 0.07                         # segundos por carácter

# Logo "JH" en la fuente ANSI Shadow: █ son celdas llenas, el resto es la sombra en doble línea.
LOGO = [
    "     ██╗██╗  ██╗",
    "     ██║██║  ██║",
    "     ██║███████║",
    "██   ██║██╔══██║",
    "╚█████╔╝██║  ██║",
    " ╚════╝ ╚═╝  ╚═╝",
]
LW, LH = 12, 22                     # tamaño de cada celda del logo
LX, LY = X0, 56

SPLASH = [
    ("✻ Welcome to Javier's terminal", "cmd"),
    ("Tips for getting started: whoami, cat stack.txt, uptime", "muted"),
    ("cwd: ~/github/JavierxHernandez", "muted"),
]

# (comando, [(texto, rol)]) — rol: accent | out | muted
SCRIPT = [
    ("whoami", [[("Javier Hernández", "accent"), (" — Systems Engineer · full-stack developer", "out")]]),
    ("cat stack.txt", [[("Laravel · TypeScript · Python · Docker · AWS · GCP", "out")]]),
    ("uptime", [[("up 7+ years", "accent"), (", building web products", "out")]]),
]


def logo_shapes():
    """Celdas llenas para █ y trazos dobles para la sombra (═ ║ ╔ ╗ ╚ ╝)."""
    d = LW * 0.18
    blocks, lines = [], []
    for r, row in enumerate(LOGO):
        for col, ch in enumerate(row):
            x, y = LX + col * LW, LY + r * LH
            cx, cy, R, B = x + LW / 2, y + LH / 2, x + LW, y + LH
            if ch == "█":
                blocks.append(f'<rect x="{x}" y="{y}" width="{LW + 0.4}" height="{LH + 0.4}"/>')
            elif ch == "═":
                lines += [f"M{x},{cy - d}H{R}", f"M{x},{cy + d}H{R}"]
            elif ch == "║":
                lines += [f"M{cx - d},{y}V{B}", f"M{cx + d},{y}V{B}"]
            elif ch == "╗":
                lines += [f"M{x},{cy - d}H{cx + d}V{B}", f"M{x},{cy + d}H{cx - d}V{B}"]
            elif ch == "╔":
                lines += [f"M{R},{cy - d}H{cx - d}V{B}", f"M{R},{cy + d}H{cx + d}V{B}"]
            elif ch == "╝":
                lines += [f"M{x},{cy + d}H{cx + d}V{y}", f"M{x},{cy - d}H{cx - d}V{y}"]
            elif ch == "╚":
                lines += [f"M{R},{cy + d}H{cx - d}V{y}", f"M{R},{cy - d}H{cx + d}V{y}"]
    return "".join(blocks), "".join(lines)


def render(t):
    c = THEMES[t]
    logo_w, logo_h = len(LOGO[0]) * LW, len(LOGO) * LH
    blocks, shadow = logo_shapes()

    # Splash: el logo se revela de izquierda a derecha y el texto aparece al lado.
    splash = [
        f'<g clip-path="url(#reveal)">'
        f'<path d="{shadow}" stroke="{c["shadow"]}" stroke-width="1.2" fill="none"/>'
        f'<g fill="url(#grad)">{blocks}</g></g>'
    ]
    tx, ty = LX + logo_w + 34, LY + 30
    for k, (txt, role) in enumerate(SPLASH):
        size = 16 if k == 0 else 14
        splash.append(f'<text x="{tx}" y="{ty + k * 28}" fill="{c[role]}" font-size="{size}" opacity="0">{escape(txt)}'
                      f'<set attributeName="opacity" to="1" begin="{0.8 + k * 0.15:.2f}s" fill="freeze"/></text>')

    parts, clips = [], []
    y, clock = LY + logo_h + 58, 1.7
    for i, (cmd, outputs) in enumerate(SCRIPT):
        n = len(cmd)
        cx = X0 + len(PROMPT) * CW
        steps = ";".join(f"{k * CW:.1f}" for k in range(n + 1))
        clips.append(
            f'<clipPath id="c{i}"><rect x="{cx}" y="{y - FS}" height="{FS + 8}" width="0">'
            f'<animate attributeName="width" values="{steps}" calcMode="discrete" '
            f'begin="{clock:.2f}s" dur="{n * TYPE:.2f}s" fill="freeze"/></rect></clipPath>')
        parts.append(
            f'<g opacity="0"><set attributeName="opacity" to="1" begin="{clock - 0.25:.2f}s" fill="freeze"/>'
            f'<text x="{X0}" y="{y}" fill="{c["prompt"]}" textLength="{3 * CW}" lengthAdjust="spacingAndGlyphs">~ $</text>'
            f'<text x="{cx}" y="{y}" fill="{c["cmd"]}" clip-path="url(#c{i})" '
            f'textLength="{n * CW}" lengthAdjust="spacingAndGlyphs">{escape(cmd)}</text></g>')
        clock += n * TYPE + 0.35
        for line in outputs:
            y += 30
            spans = "".join(f'<tspan fill="{c[role]}">{escape(txt)}</tspan>' for txt, role in line)
            parts.append(f'<text x="{X0}" y="{y}" opacity="0">{spans}'
                         f'<set attributeName="opacity" to="1" begin="{clock:.2f}s" fill="freeze"/></text>')
        clock += 0.55
        y += 42
    # último prompt con cursor parpadeando
    parts.append(
        f'<g opacity="0"><set attributeName="opacity" to="1" begin="{clock - 0.25:.2f}s" fill="freeze"/>'
        f'<text x="{X0}" y="{y}" fill="{c["prompt"]}" textLength="{3 * CW}" lengthAdjust="spacingAndGlyphs">~ $</text>'
        f'<rect x="{X0 + len(PROMPT) * CW}" y="{y - FS + 3}" width="{CW}" height="{FS + 2}" fill="{c["cmd"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>'
        f'</rect></g>')
    H = y + 26
    sep_y = LY + logo_h + 22
    dots = "".join(f'<circle cx="{22 + k * 20}" cy="18" r="6" fill="{col}"/>'
                   for k, col in enumerate(["#ff5f57", "#febc2e", "#28c840"]))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="JH. whoami: Javier Hernández, Systems Engineer and full-stack developer">
<defs>
<linearGradient id="grad" gradientUnits="userSpaceOnUse" x1="{LX}" y1="0" x2="{LX + logo_w}" y2="0" spreadMethod="reflect">
<stop offset="0" stop-color="{c["g1"]}"/><stop offset="0.55" stop-color="{c["g2"]}"/><stop offset="1" stop-color="{c["g3"]}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="0 0;{logo_w} 0;0 0" dur="8s" repeatCount="indefinite"/>
</linearGradient>
<clipPath id="reveal"><rect x="{LX - 2}" y="{LY - 2}" height="{logo_h + 4}" width="0">
<animate attributeName="width" from="0" to="{logo_w + 4}" begin="0.1s" dur="0.6s" fill="freeze"/></rect></clipPath>
{''.join(clips)}<clipPath id="win"><rect width="{W}" height="{H}" rx="10"/></clipPath></defs>
<g clip-path="url(#win)">
<rect width="{W}" height="{H}" fill="{c["bg"]}"/>
<rect width="{W}" height="36" fill="{c["bar"]}"/><line x1="0" y1="36" x2="{W}" y2="36" stroke="{c["border"]}"/>
{dots}
<text x="{W / 2}" y="23" text-anchor="middle" fill="{c["title"]}" font-family="{FONT}" font-size="13">javier@dev: ~</text>
<g font-family="{FONT}">{''.join(splash)}</g>
<line x1="{X0}" y1="{sep_y}" x2="{W - X0}" y2="{sep_y}" stroke="{c["border"]}" stroke-dasharray="3 4"/>
<g font-family="{FONT}" font-size="{FS}">{''.join(parts)}</g>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="10" fill="none" stroke="{c["border"]}"/>
</svg>
"""


for t in THEMES:
    (OUT / f"banner-{t}.svg").write_text(render(t), encoding="utf-8")
    print("ok", t)
