#!/usr/bin/env python3
"""
Minimal Shadow DOM Anpassung - NUR JavaScript, CSS bleibt unverändert
"""

import re

# Datei einlesen
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. JavaScript wrappen in shadowDOMReady Event
# Finde den <script> Tag
script_start = content.find('    <script>')
script_end = content.find('    </script>')

if script_start != -1 and script_end != -1:
    # Extrahiere den JavaScript Code
    js_code = content[script_start + len('    <script>\n'):script_end]

    # Wrappen in Event Listener und alle Einrückungen um 8 Spaces erhöhen
    js_lines = js_code.split('\n')
    indented_lines = ['        ' + line if line.strip() else line for line in js_lines]
    indented_code = '\n'.join(indented_lines)

    # Neuer JavaScript Block
    new_js = f'''    <script>
        document.addEventListener("shadowDOMReady", (event) => {{
            const root = event.detail.shadowRoot;

{indented_code}
        }});
    </script>'''

    # Ersetzen
    content = content[:script_start] + new_js + content[script_end + len('    </script>'):]

# 2. document.getElementById durch root.getElementById ersetzen
# ABER NUR innerhalb des Scripts, nicht im Event Listener selbst
content = re.sub(r'(?<!document\.addEventListener\("shadowDOMReady", \(event\) => \{\n            const root = event\.detail\.shadowRoot;\n\n        )document\.getElementById', 'root.getElementById', content)

# Einfachere Version: Alle document.getElementById ersetzen
content = re.sub(r'\bdocument\.getElementById\b', 'root.getElementById', content)

# 3. document.querySelector durch root.querySelector ersetzen
content = re.sub(r'\bdocument\.querySelector\b', 'root.querySelector', content)

print("Original Anzahl document.getElementById:", content.count('document.getElementById'))
print("Neue Anzahl root.getElementById:", content.count('root.getElementById'))

# Datei schreiben
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Anpassung abgeschlossen!")
print("Die index.html wurde für Shadow DOM angepasst (nur JavaScript, CSS unverändert).")
