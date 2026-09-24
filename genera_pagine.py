#!/usr/bin/env python3
"""Genera le pagine-importo: "quanto fatturare per guadagnare X euro al mese".

Usa gli stessi numeri ufficiali del tool (coefficiente 67% per l'informatico,
INPS 26,07%, imposta sostitutiva 15% o 5%). Ogni pagina risponde SUBITO, con il
conto in chiaro, e rimanda al calcolatore per i valori personali.

Uso: python3 genera_pagine.py
"""
import json
import os

QUI = os.path.dirname(os.path.abspath(__file__))
CARTELLA = os.path.join(QUI, "quanto-fatturare")
SITO = "https://agenticcis.github.io/quanto-resta-in-tasca"

# Valori ufficiali (fonti in fondo a ogni pagina)
COEFF = 0.67          # ATECO 62.02.00 consulenza IT — Allegato 4 L.190/2014
INPS = 0.2607         # INPS circolare 8/2026, professionisti
IMPOSTA = 0.15        # L.190/2014 art.1 c.64
IMPOSTA_STARTUP = 0.05  # L.190/2014 art.1 c.65

IMPORTI = [1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000, 5000]


def k_da(coeff, inps, imposta):
    return 1 - coeff * inps - coeff * (1 - inps) * imposta


def calcola(netto_mese, imposta):
    """Quanto va fatturato per portare a casa netto_mese al mese."""
    coeff, inps = COEFF, INPS
    k = k_da(coeff, inps, imposta)
    netto_anno = netto_mese * 12
    fatt_anno = netto_anno / k
    reddito = fatt_anno * coeff
    contributi = reddito * inps
    base = reddito - contributi
    tasse = base * imposta
    return {
        "netto_mese": netto_mese,
        "netto_anno": netto_anno,
        "fatt_anno": fatt_anno,
        "fatt_mese": fatt_anno / 12,
        "reddito": reddito,
        "contributi": contributi,
        "tasse": tasse,
    }


def eur(x):
    return f"{x:,.0f}".replace(",", ".") + " €"


def pagina(imp, dati, dati5):
    titolo = f"Quanto fatturare per guadagnare {eur(imp)} al mese (forfettario)"
    descr = (f"Per portare a casa {eur(imp)} netti al mese in regime forfettario "
             f"devi fatturare circa {eur(dati['fatt_anno'])} all'anno. Ecco il conto completo, "
             f"passo per passo, con le aliquote ufficiali 2026.")
    slug = f"{imp}-euro-al-mese.html"
    nota5 = ""
    if dati5["fatt_anno"] > 85000:
        nota5 = ("<p class='avviso'>⚠️ <b>Attenzione:</b> con l'imposta al 5% servirebbero "
                 f"{eur(dati5['fatt_anno'])} di fatturato, oltre il limite di 85.000 € del "
                 "regime forfettario.</p>")
    elif dati5["fatt_anno"] != dati["fatt_anno"]:
        nota5 = (f"<p class='nota'>Nei <b>primi 5 anni</b> (se hai i requisiti della nuova "
                 f"attività) l'imposta è al 5% invece che al 15%: in quel caso bastano "
                 f"<b>{eur(dati5['fatt_anno'])}</b> all'anno ({eur(dati5['fatt_mese'])} al mese).</p>")

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo}</title>
<meta name="description" content="{descr}">
<link rel="canonical" href="{SITO}/quanto-fatturare/{slug}">
<meta property="og:title" content="{titolo}">
<meta property="og:description" content="{descr}">
<meta property="og:type" content="article">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{
 "@type":"Question","name":"Quanto devo fatturare per guadagnare {eur(imp)} al mese in regime forfettario?",
 "acceptedAnswer":{{"@type":"Answer","text":"Circa {eur(dati['fatt_anno'])} all'anno ({eur(dati['fatt_mese'])} al mese). Il conto: fatturato x coefficiente 67% = reddito imponibile di {eur(dati['reddito'])}; contributi INPS 26,07% = {eur(dati['contributi'])}; imposta sostitutiva 15% = {eur(dati['tasse'])}; netto = {eur(dati['netto_anno'])} all'anno."}}
}}]}}
</script>
<style>
 :root{{--bg:#0b0f14;--card:#131a22;--line:#212b36;--txt:#e6edf3;--dim:#9fb0c0;--acc:#4aa8ff;--acc2:#7bd88f}}
 *{{box-sizing:border-box}}
 body{{margin:0;background:var(--bg);color:var(--txt);font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
 .wrap{{max-width:760px;margin:0 auto;padding:22px 16px}}
 a{{color:var(--acc)}}
 h1{{font-size:26px;line-height:1.25;margin:10px 0 6px}}
 h2{{font-size:15px;text-transform:uppercase;letter-spacing:.6px;color:var(--dim);margin:26px 0 10px}}
 .card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;margin:16px 0}}
 .risposta{{font-size:20px;line-height:1.5}}
 .risposta b{{color:var(--acc2)}}
 .riga{{display:flex;justify-content:space-between;border-bottom:1px dashed var(--line);padding:9px 0}}
 .riga:last-child{{border-bottom:0}}
 .riga.tot{{font-weight:700;font-size:17px;border-top:1px solid var(--line);margin-top:6px;padding-top:12px}}
 .nota{{color:var(--dim);font-size:14px}}
 .avviso{{color:#ffd479;font-size:14px}}
 .wrap a.bottone{{display:inline-block;background:var(--acc);color:#04121f;font-weight:700;
   text-decoration:none;padding:12px 18px;border-radius:10px;margin-top:6px}}
 footer{{color:var(--dim);font-size:13px;border-top:1px solid var(--line);margin-top:30px;padding-top:14px}}
 ul{{padding-left:18px}} li{{margin:5px 0}}
</style>
</head>
<body>
<div class="wrap">
<p><a href="../">← Torna al calcolatore</a></p>
<h1>Quanto fatturare per guadagnare {eur(imp)} al mese (regime forfettario)</h1>

<div class="card">
  <p class="risposta">Devi fatturare circa <b>{eur(dati['fatt_anno'])}</b> all'anno,
  cioè <b>{eur(dati['fatt_mese'])}</b> al mese.</p>
  <p class="nota">Per portare a casa {eur(imp)} netti al mese ({eur(dati['netto_anno'])} all'anno),
  con il coefficiente del settore informatico (67%) e le aliquote 2026.</p>
</div>

<h2>Il conto, passo per passo</h2>
<div class="card">
  <div class="riga"><span>Fatturato necessario</span><span>{eur(dati['fatt_anno'])}</span></div>
  <div class="riga"><span>Reddito imponibile (× 67%)</span><span>{eur(dati['reddito'])}</span></div>
  <div class="riga"><span>Contributi INPS (26,07%)</span><span>− {eur(dati['contributi'])}</span></div>
  <div class="riga"><span>Imposta sostitutiva (15%)</span><span>− {eur(dati['tasse'])}</span></div>
  <div class="riga tot"><span>Netto in tasca</span><span>{eur(dati['netto_anno'])}</span></div>
</div>
{nota5}

<div class="card">
  <p><b>Non è il tuo caso?</b> Calcola con i tuoi numeri: codice ATECO, obiettivo di netto,
  cliente italiano o estero.</p>
  <a class="bottone" href="../">Apri il calcolatore gratuito →</a>
</div>

<h2>Perché il coefficiente conta</h2>
<p>Il regime forfettario non tassa tutto il fatturato: si applica un <b>coefficiente di
redditività</b> che dipende dal codice ATECO. Per il settore informatico (divisione 62) è
<b>67%</b>, non 78%: il 78% vale per avvocati, ingegneri e altre professioni. Sbagliare questo
numero cambia il risultato di migliaia di euro all'anno.</p>

<h2>Altre cifre utili</h2>
<ul>
{''.join(f'<li><a href="{i}-euro-al-mese.html">{eur(i)} al mese</a></li>' for i in IMPORTI if i != imp)}
</ul>

<h2>Fonti</h2>
<ul class="nota">
  <li>Coefficienti di redditività: Allegato 4, Legge 190/2014 —
    <a href="https://www.agenziaentrate.gov.it/portale/documents/20143/241208/allegato%2B4.pdf/d69be7fc-b18a-3c73-bd2e-b0f3c1970218" rel="noopener" target="_blank">PDF Agenzia delle Entrate</a></li>
  <li>Contributi INPS Gestione Separata 26,07% — circolare INPS n. 8 del 03/02/2026</li>
  <li>Imposta sostitutiva 15% / 5% — Legge 190/2014, art. 1, commi 64 e 65</li>
</ul>

<footer>
  <b>RestaNetto</b> — strumento di orientamento, non consulenza fiscale. I calcoli sono stime
  basate sulle aliquote ufficiali 2026; casi particolari (altre casse, agevolazioni, regimi
  transitori) possono cambiare il risultato. Per decisioni reali verifica con un commercialista.
</footer>
</div>
</body>
</html>
"""


def main():
    os.makedirs(CARTELLA, exist_ok=True)
    indice = []
    for imp in IMPORTI:
        dati = calcola(imp, IMPOSTA)
        dati5 = calcola(imp, IMPOSTA_STARTUP)
        percorso = os.path.join(CARTELLA, f"{imp}-euro-al-mese.html")
        with open(percorso, "w", encoding="utf-8") as f:
            f.write(pagina(imp, dati, dati5))
        indice.append((imp, dati))
        print(f"  {imp:>5} €/mese -> fatturare {dati['fatt_anno']:>10,.0f} €/anno  "
              f"({dati['fatt_mese']:,.0f} €/mese)")

    # indice delle pagine
    righe = "\n".join(
        f'    <li><a href="{i}-euro-al-mese.html">Quanto fatturare per {eur(i)} al mese</a> '
        f'<span class="nota">→ {eur(d["fatt_anno"])} all\'anno</span></li>'
        for i, d in indice)
    with open(os.path.join(CARTELLA, "index.html"), "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quanto devo fatturare per guadagnare X al mese (forfettario)</title>
<meta name="description" content="Quanto fatturare in regime forfettario per portare a casa 1.000, 1.500, 2.000, 2.500, 3.000 euro al mese. Conti in chiaro con le aliquote ufficiali 2026.">
<link rel="canonical" href="{SITO}/quanto-fatturare/">
<style>
 :root{{--bg:#0b0f14;--card:#131a22;--line:#212b36;--txt:#e6edf3;--dim:#9fb0c0;--acc:#4aa8ff}}
 body{{margin:0;background:var(--bg);color:var(--txt);font:16px/1.6 system-ui,sans-serif}}
 .wrap{{max-width:760px;margin:0 auto;padding:22px 16px}}
 a{{color:var(--acc)}} h1{{font-size:26px}} h2{{font-size:15px;color:var(--dim);text-transform:uppercase}}
 .card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;margin:16px 0}}
 ul{{line-height:2.1;padding-left:18px}} .nota{{color:var(--dim);font-size:13px}}
</style></head><body><div class="wrap">
<p><a href="../">← Calcolatore RestaNetto</a></p>
<h1>Quanto devo fatturare per guadagnare X al mese?</h1>
<p class="nota">Regime forfettario, aliquote ufficiali 2026, coefficiente 67% (settore informatico).
Ogni pagina mostra il conto completo.</p>
<div class="card"><ul>
{righe}
</ul></div>
<p class="nota">Non trovi la tua cifra? <a href="../">Usa il calcolatore</a> e inserisci il tuo obiettivo.</p>
</div></body></html>
""")
    print(f"\nCreate {len(IMPORTI)+1} pagine in {CARTELLA}")


if __name__ == "__main__":
    main()
