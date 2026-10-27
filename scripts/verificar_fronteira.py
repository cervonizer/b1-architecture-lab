"""Verifica imports e referências qualificadas da fatia Ranking; não substitui análise de bytecode."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1] / "src/main/java/com/exemplo/usuario/ranking"
violacoes = []
for arquivo in sorted(root.rglob("*.java")):
    texto = arquivo.read_text()
    texto = re.sub(r"/\*.*?\*/|//[^\n]*", "", texto, flags=re.S)
    for nome in re.findall(r"com\.exemplo\.usuario\.[\w.*]+", texto):
        partes = nome.split(".")
        if len(partes) > 4 and partes[3] != "ranking" and partes[4] != "api":
            violacoes.append(f"{arquivo.name}: {nome}")
if violacoes:
    print("FALHA: Ranking acessa detalhes de outro modulo:")
    print("\n".join(violacoes))
    sys.exit(1)
print("OK: Ranking referencia outros modulos somente por api publica.")
