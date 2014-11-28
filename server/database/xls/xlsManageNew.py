import sys
import os
import pickle

from openpyxl.reader.excel import load_workbook

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
xlsx_src_path = os.path.join(this_module_path, "src")
pickle_path = os.path.join(this_module_path, "pickle")

new_data_file_path = os.path.join(xlsx_src_path, "new_data.xlsx")

class MarkerArachne:
    chr_id_         =   -1
    marker_         =   ""
    pos_cm_         =   -1.0
    contig_id_      =   -1
    contig_start_   =   -1
    contig_stop_    =   -1
    scaff_id_       =   -1
    scaff_start_    =   -1
    scaff_stop_     =   -1
    
    def __init__(self, chr_id, marker, pos_cm, contig_id, contig_start, contig_stop, scaff_id, scaff_start, scaff_stop):
        self.chr_id_         =   chr_id
        self.marker_         =   marker
        self.pos_cm_         =   pos_cm
        self.contig_id_      =   contig_id
        self.contig_start_   =   contig_start
        self.contig_stop_    =   contig_stop
        self.scaff_id_       =   scaff_id
        self.scaff_start_    =   scaff_start
        self.scaff_stop_     =   scaff_stop