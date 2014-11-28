import sys
import os

this_module_path = os.path.abspath (os.path.dirname(sys.modules[__name__].__file__))
server_path = os.path.join(this_module_path, '..', '..')
sys.path.append(server_path)

calc_path = os.path.join(this_module_path, '..', '..', '..', 'calc', 'build')
sys.path.append(calc_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'server.config.settings'

services = {
    'main.echo': "echo",
    'main.start' : "startClient",
    'main.serverTime': "getServerTime",
    'main.getLogFile': "getLogFile",
    'algorithm.searchSW' : "searchSW",
    'algorithm._searchSW' : "_searchSW",
    'algorithm.searchProgressSW' : "searchProgressSW",
    'algorithm.getTextsResultSW' : "getTextsResultSW",
    'algorithm.findKMP' : "findKMP",
    'algorithm.findProgressKMP' : "findProgressKMP",
    'algorithm.getTextResultKMP' : "getTextResultKMP",
    'algorithm.runBLAST' : "runBLAST",
    'algorithm._runBLAST' : "_runBLAST",
    'algorithm.findProgressBLAST' : "findProgressBLAST",
    'algorithm.runBLAST_SW' : "runBLAST_SW",
    'algorithm._runBLAST_SW' : "_runBLAST_SW",
    'algorithm.findProgressBLAST_SW' : "findProgressBLAST_SW",
    'chromosome.getAll' : "getChromosomes",
    'chromosome.getChromosomeByID' : "getChromosomeByID",
    'chromosome.getAssembByID' : "getAssembByID",
    'chromosome.getAssembName' : "getAssembName",
    'chromosome.getAssembs' : "getAssembs",
    'chromosome.getAssembsFromOrganism' : "getAssembsFromOrganism",
    'chromosome.getAssembsDictFromOrganism' : "getAssembsDictFromOrganism",
    'chromosome.getAssembsDict' : "getAssembsDict",
    'chromosome.updateAssembs' : "updateAssembs",
    'chromosome.delete' : "deleteChromosome",
    'contig.buildTree' : "buildContigTree",
    'contig.getFromTree' : "getContigFromTree",
    'contig.get' : "getContig",
    'contig.getScaffold' : "getScaffByContID",
    'contig.getContigs' : "getContigs",
    'contig.getContigsDict' : "getContigsDict",
    'contig.delete' : "deleteCongit",
    'import.importScaffolds' : "importScaffolds",
    'import.importContigs' : "importContigs",
    'marker.buildContigTree' : "buildMarkerContigTree",
    'marker.getFromContigTree' : "getMarkerFromContigTree",
    'marker.getMarkersOnContig' : "getMarkersOnContig",
    'marker.buildScaffoldTree' : "buildMarkerScaffoldTree",
    'marker.getFromScaffoldTree' : "getMarkerFromScaffoldTree",
    'marker.getMarkersOnScaffold' : "getMarkersOnScaffold",
    'marker.get' : "getMarker",
    'marker.getMarkersDictOnCont' : "getMarkersDictOnCont",
    'marker.getMarkersDictOnScaff' : "getMarkersDictOnScaff",
    'organism.getOrganisms' : "getOrganisms",
    'organism.addOrganism' : "addOrganism",
    'organism.delete' : "deleteOrganism",
    'scaffold.buildTree' : "buildScaffoldTree",
    'scaffold.getFromTree' : "getScaffoldsFromTree",
    'scaffold.getChromosomeID' : "getChromosomeID",
    'scaffold.getScaffoldPosition' : "getScaffoldPosition",
    'scaffold.getScaffold' : "getScaffold",
    'scaffold.delete' : "deleteScaffold",
    'scaffold.count' : "getScaffoldsCount",
    'scaffold.undefined.getScaffolds' : "getScaffolds",
    'scaffold.undefined.getMinID' : "getMinID",
    'scaffold.undefined.getMaxID' : "getMaxID",
    'scaffold.undefined.getMaxLength' : "getMaxLength",
    'remote.get': "remote_manager.get"
}

output_file = open(os.path.join("output", "services_table.txt"), "w")

def seqSplit(text):
    return '\seqsplit{' + text + '}'

for service in sorted(services.iterkeys()):
    output_file.write(seqSplit(service.replace('_', '\\_')) + '\t&\t' + seqSplit(services[service].replace('_', '\\_')) + '\t&\t[OPIS]\t\\\ \hline\n')

output_file.close()