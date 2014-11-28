from pyamf.remoting.gateway.django import DjangoGateway
import pyamf

from server.algorithm.interfBM import findBM, findProgressBM, getTextResultBM
from server.algorithm.interfKMP import findKMP, findProgressKMP, getTextResultKMP
from server.algorithm.interfSW import searchSW, _searchSW, searchProgressSW, getTextsResultSW
from server.algorithm.interfBlast import findProgressBLAST, runBLAST, _runBLAST
from server.algorithm.interfBlastSW import findProgressBLAST_SW, runBLAST_SW, _runBLAST_SW
from server.chromosome.interf import getChromosomes, getChromosomeByID, getAssembByID, getAssembName, getAssembs, getAssembsDict, updateAssembs, getAssembsFromOrganism, getAssembsDictFromOrganism, deleteChromosome
from server.scaffold.interf import buildScaffoldTree, getScaffoldsFromTree, getChromosomeID, getScaffoldPosition, getScaffold, deleteScaffold, getScaffoldsCount
from server.scaffold.undefined.interf import getScaffolds, getMaxLength, getMinID, getMaxID
from server.scaffold.models import ScaffoldWrap
from server.scaffold.models import UndefinedScaffoldWrap
from server.utils.remoteAccess import RemoteManager
from server.contig.models import Contig, ContigWrap
from server.contig.interf import buildContigTree, getContigFromTree, getContig, getScaffByContID, getContigs, getContigsDict, deleteCongit
from server.marker.models import Marker, MarkerWrap
from server.marker.interf import buildMarkerContigTree, getMarkerFromContigTree, getMarkersOnContig, buildMarkerScaffoldTree, getMarkerFromScaffoldTree, getMarkersOnScaffold, getMarker, getMarkersDictOnCont, getMarkersDictOnScaff
from server.import_export.interf import importScaffolds, importContigs
from server.organism.interf import getOrganisms, addOrganism, deleteOrganism

from server.services import echo, getServerTime, getLogFile, startClient

pyamf.register_class(ScaffoldWrap, 'com.vos.ScaffoldVO')
pyamf.register_class(UndefinedScaffoldWrap, 'com.vos.UndefinedScafoldVO')
pyamf.register_class(ContigWrap, 'com.vos.ContigVO')
pyamf.register_class(MarkerWrap, 'com.vos.MarkerVO')

remote_manager = RemoteManager()

services = {
    'main.echo': echo,
    'main.start' : startClient,
    'main.serverTime': getServerTime,
    'main.getLogFile': getLogFile,
    'algorithm.searchSW' : searchSW,
    'algorithm._searchSW' : _searchSW,
    'algorithm.searchProgressSW' : searchProgressSW,
    'algorithm.getTextsResultSW' : getTextsResultSW,
    'algorithm.findBM' : findBM,
    'algorithm.findProgressBM' : findProgressBM,
    'algorithm.getTextResultBM' : getTextResultBM,
    'algorithm.findKMP' : findKMP,
    'algorithm.findProgressKMP' : findProgressKMP,
    'algorithm.getTextResultKMP' : getTextResultKMP,
    'algorithm.runBLAST' : runBLAST,
    'algorithm._runBLAST' : _runBLAST,
    'algorithm.findProgressBLAST' : findProgressBLAST,
    'algorithm.runBLAST_SW' : runBLAST_SW,
    'algorithm._runBLAST_SW' : _runBLAST_SW,
    'algorithm.findProgressBLAST_SW' : findProgressBLAST_SW,
    'chromosome.getAll' : getChromosomes,
    'chromosome.getChromosomeByID' : getChromosomeByID,
    'chromosome.getAssembByID' : getAssembByID,
    'chromosome.getAssembName' : getAssembName,
    'chromosome.getAssembs' : getAssembs,
    'chromosome.getAssembsFromOrganism' : getAssembsFromOrganism,
    'chromosome.getAssembsDictFromOrganism' : getAssembsDictFromOrganism,
    'chromosome.getAssembsDict' : getAssembsDict,
    'chromosome.updateAssembs' : updateAssembs,
    'chromosome.delete' : deleteChromosome,
    'contig.buildTree' : buildContigTree,
    'contig.getFromTree' : getContigFromTree,
    'contig.get' : getContig,
    'contig.getScaffold' : getScaffByContID,
    'contig.getContigs' : getContigs,
    'contig.getContigsDict' : getContigsDict,
    'contig.delete' : deleteCongit,
    'import.importScaffolds' : importScaffolds,
    'import.importContigs' : importContigs,
    'marker.buildContigTree' : buildMarkerContigTree,
    'marker.getFromContigTree' : getMarkerFromContigTree,
    'marker.getMarkersOnContig' : getMarkersOnContig,
    'marker.buildScaffoldTree' : buildMarkerScaffoldTree,
    'marker.getFromScaffoldTree' : getMarkerFromScaffoldTree,
    'marker.getMarkersOnScaffold' : getMarkersOnScaffold,
    'marker.get' : getMarker,
    'marker.getMarkersDictOnCont' : getMarkersDictOnCont,
    'marker.getMarkersDictOnScaff' : getMarkersDictOnScaff,
    'organism.getOrganisms' : getOrganisms,
    'organism.addOrganism' : addOrganism,
    'organism.delete' : deleteOrganism,
    'scaffold.buildTree' : buildScaffoldTree,
    'scaffold.getFromTree' : getScaffoldsFromTree,
    'scaffold.getChromosomeID' : getChromosomeID,
    'scaffold.getScaffoldPosition' : getScaffoldPosition,
    'scaffold.getScaffold' : getScaffold,
    'scaffold.delete' : deleteScaffold,
    'scaffold.count' : getScaffoldsCount,
    'scaffold.undefined.getScaffolds' : getScaffolds,
    'scaffold.undefined.getMinID' : getMinID,
    'scaffold.undefined.getMaxID' : getMaxID,
    'scaffold.undefined.getMaxLength' : getMaxLength,
    'remote.get': remote_manager.get
}

my_gateway = DjangoGateway(services, expose_request = False, debug = True)
