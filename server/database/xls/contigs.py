from openpyxl.reader.excel import load_workbook

## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! DO ZMIANY PO TYM JAK DOSTANE DOBRE DANE !!!!!!!!!!!!!!!!!!!!!!

def getCeleraContigs():
    xls_file = load_workbook("src\\laczenie060410.xlsx")
    print "Szukam..."
    for sheet in xls_file.worksheets:
        print "Arkusz: ", sheet.title
        if sheet.title != "finalne":
            continue
        # Arkusz finalne
        csv_file_name = "csv\\contigs_celera.csv"
        print "Tworze plik: %s, zawierajacy informacje o contigach celera..." % csv_file_name
        csv_file = open(csv_file_name, "wt")
        # Ktore kolumny nas interesuja?
        first_row = sheet.rows[0]
        for i, cell in enumerate(first_row):
            if "celera_ST" in cell.value:
                start = i
                continue
            if "celera_EN" in cell.value:
                stop = i
            if "cel_ctg_len" in cell.value:
                len = i
        print "Indeks ID: ", id_col, "; indeks dlugosci: ", len_col
        scaffolds_id = []
        for row in sheet.rows[1:]:
            scaffold = []
            # ID
            value = row[id_col].value
            if value in scaffolds_id:   # Mamy juz go!
                continue
            scaffolds_id.append(value)  # Odchaczamy, ze mamy
            if value is None:
                value = ''
            if not isinstance(value, unicode):
                value = unicode(value)
            value = value.encode('utf8')
            scaffold.append(value)
            # DLUGOSC
            value = row[len_col].value
            if value is None:
                value = ''
            if not isinstance(value, unicode):
                value = unicode(value)
            value = value.encode('utf8')
            scaffold.append(value)
            # CHROMOSOM
            value = row[chr_col].value
            if value is None:
                value = ''
            if not isinstance(value, unicode):
                value = unicode(value)
            value = value.encode('utf8')
            scaffold.append(value)
            # Zapisanie do CSV
            csv_file.write('\t'.join(scaffold))
            csv_file.write('\n')
        csv_file.close()

getCeleraContigs()
