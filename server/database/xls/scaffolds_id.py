import sys

from openpyxl.reader.excel import load_workbook

def getScaffoldsIDs():
    xls_file = load_workbook("src\\laczenie.xlsx")
    print "Szukam..."
    for sheet in xls_file.worksheets:
        print "Arkusz: ", sheet.title
        if sheet.title in ['chr1_a', 'chr2_a', 'chr3_a', 'chr4_a', 'chr5_a', 'chr6_a', 'chr7_a']:
            csv_file_name = "csv\\scaffolds_celera_id.csv"
            print "Tworze plik: %s, zawierajacy informacje o ID scaffoldow celery..." % csv_file_name
            csv_file = open(csv_file_name, "at")

            # Ktore kolumny nas interesuja?
            first_row = sheet.rows[0]
            scaff_id = -1
            for i, cell in enumerate(first_row):
                # Odczytanie ID scaffoldu
                if "scf_celera" in cell.value:
                    scaff_id = i
                    continue
            if scaff_id == -1:
                print "Nie znaleziono kolumny 'scf_celera'!"
                sys.exit(1)

            scaffolds_found = []
            for row in sheet.rows[1:]:
                scaffold = []

                # ID
                value = row[scaff_id].value
                if value in scaffolds_found:   # Mamy juz go!
                    continue

                scaffolds_found.append(value)  # Odchaczamy, ze mamy
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

getScaffoldsIDs()
