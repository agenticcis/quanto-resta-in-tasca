import json

# Elenco dei codici ATECO 2007 più comuni per freelance/professionisti/artigiani.
# Il coefficiente NON è scritto qui: viene derivato dal codice con la tabella
# ufficiale (aliquote_ateco.json), così esiste una sola fonte di verità.
CODICI = [
    # --- Informatica, software, consulenza IT (divisione 62 e dintorni -> 67%) ---
    ("62.01.00", "Produzione di software non connesso all'edizione"),
    ("62.02.00", "Consulenza nel settore delle tecnologie dell'informatica"),
    ("62.03.00", "Gestione di strutture e apparecchiature informatiche"),
    ("62.09.09", "Altre attività dei servizi connessi alle tecnologie dell'informatica"),
    ("63.11.00", "Elaborazione dati, hosting e attività connesse"),
    ("63.12.00", "Portali web"),
    ("58.21.00", "Edizione di giochi per computer"),
    ("58.29.00", "Altre edizioni di software"),
    ("61.10.00", "Telecomunicazioni via cavo, senza fili e satellitari (operatore)"),
    ("61.90.00", "Altre attività di telecomunicazione"),
    ("59.11.00", "Attività di produzione cinematografica, video e programmi TV"),
    ("63.99.00", "Altre attività dei servizi di informazione"),

    # --- Professioni e consulenza (divisioni 69-75 -> 78%) ---
    ("69.10.10", "Attività degli studi legali"),
    ("69.20.00", "Attività degli studi commercialisti e dei revisori contabili"),
    ("70.21.00", "Pubbliche relazioni e comunicazione"),
    ("70.22.09", "Consulenza imprenditoriale e amministrativo-gestionale"),
    ("71.11.00", "Attività degli studi di architettura"),
    ("71.12.10", "Servizi di ingegneria integrata"),
    ("71.12.20", "Servizi di ingegneria"),
    ("73.11.02", "Conduzione di campagne di marketing e pubblicitarie"),
    ("73.12.00", "Attività delle concessionarie e degli agenti pubblicitari"),
    ("74.10.21", "Attività dei disegnatori grafici di pagine web"),
    ("74.10.29", "Altre attività dei disegnatori grafici"),
    ("74.20.19", "Altre attività di riprese fotografiche"),
    ("74.30.00", "Traduzione e interpretariato"),
    ("74.90.99", "Altre attività professionali (consulenza tecnica, ecc.)"),
    ("72.19.09", "Altre attività di ricerca e sviluppo sperimentale"),

    # --- Istruzione e sanità (divisioni 85-88 -> 78%) ---
    ("85.59.20", "Corsi di formazione e aggiornamento professionale"),
    ("85.59.30", "Altre attività di istruzione e formazione"),
    ("85.60.09", "Altre attività di supporto all'istruzione"),
    ("86.90.30", "Attività di psicologi e psicoterapeuti"),
    ("86.90.99", "Altre attività paramediche e sanitarie"),

    # --- Finanza e assicurazioni (divisioni 64-66 -> 78%) ---
    ("66.19.99", "Altre attività dei servizi finanziari"),
    ("66.22.00", "Attività di agenti e broker assicurativi"),

    # --- Costruzioni e immobiliare (divisioni 41-43, 68 -> 86%) ---
    ("41.20.00", "Costruzione di edifici residenziali e non residenziali"),
    ("43.21.01", "Installazione di impianti elettrici"),
    ("43.22.01", "Installazione di impianti idraulici, di riscaldamento e di condizionamento"),
    ("43.32.01", "Lavori di falegnameria e installazione di infissi"),
    ("43.91.00", "Lavori di copertura di tetti"),
    ("68.10.00", "Compravendita di beni immobili propri"),
    ("68.20.01", "Locazione immobiliare di beni propri"),
    ("68.31.00", "Intermediazione immobiliare"),

    # --- Commercio (divisioni 45, 46.x, 47.x -> 40%) ---
    ("45.20.00", "Manutenzione e riparazione di autoveicoli"),
    ("46.49.00", "Commercio all'ingrosso di altri prodotti"),
    ("47.11.10", "Ipermercati"),
    ("47.19.10", "Grandi magazzini"),
    ("47.41.00", "Commercio al dettaglio di computer, software e attrezzature per ufficio"),
    ("47.42.00", "Commercio al dettaglio di apparecchiature per le telecomunicazioni"),
    ("47.71.10", "Commercio al dettaglio di abbigliamento"),
    ("47.91.10", "Commercio al dettaglio per corrispondenza o via internet (e-commerce)"),
    ("47.99.00", "Altro commercio al dettaglio al di fuori di negozi, banchi e mercati"),

    # --- Intermediari del commercio (46.1 -> 62%) ---
    ("46.11.00", "Intermediari del commercio di materie prime agricole"),
    ("46.19.00", "Intermediari del commercio di vari prodotti"),

    # --- Commercio ambulante (47.81 -> 40%, 47.82/47.89 -> 54%) ---
    ("47.81.01", "Commercio ambulante di prodotti alimentari e bevande"),
    ("47.82.01", "Commercio ambulante di altri prodotti"),

    # --- Alloggio e ristorazione (divisioni 55-56 -> 40%) ---
    ("55.10.00", "Alberghi e strutture simili"),
    ("55.20.51", "Affittacamere per brevi soggiorni, bed and breakfast"),
    ("56.10.11", "Ristorazione con somministrazione"),
    ("56.21.00", "Fornitura di pasti preparati (catering)"),
    ("56.30.00", "Bar e altri esercizi simili senza cucina"),

    # --- Altre attività (regola generale -> 67%) ---
    ("96.02.00", "Servizi dei saloni di barbiere e di parrucchiere"),
    ("96.09.09", "Altre attività di servizi per la persona"),
    ("93.13.09", "Servizi di palestre e attività sportive"),
    ("81.21.00", "Pulizia generale di edifici"),
    ("79.11.00", "Attività di agenzie di viaggio"),
    ("95.11.00", "Riparazione di computer e periferiche"),
]

dati = {
    "_fonte": "Allegato 4 alla Legge 190/2014 (regime forfettario) - tabella ufficiale dei coefficienti di redditività",
    "_url": "https://www.agenziaentrate.gov.it/portale/documents/20143/241208/allegato%2B4.pdf/d69be7fc-b18a-3c73-bd2e-b0f3c1970218",
    "_verificato_il": "2026-09-24",
    "_nota": ("Elenco dei codici ATECO piu' comuni, non esaustivo. Il coefficiente non e' scritto qui: "
              "viene calcolato dal codice con la tabella ufficiale (aliquote_ateco.json). "
              "Si puo' digitare qualsiasi codice ATECO, anche non presente in questo elenco."),
    "codici": [{"c": c, "d": d} for c, d in CODICI],
}
with open("ateco_lista.json", "w", encoding="utf-8") as f:
    json.dump(dati, f, ensure_ascii=False, indent=2)
print("ateco_lista.json creato con", len(CODICI), "codici")
