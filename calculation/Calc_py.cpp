/**
 * Opakowanie kodu C++ dla Pythona
 * @author: Piotr Roz
 * Kompilacja:
 * cl /EHsc /MD /D "WIN32" /D "_WIN32_WINNT#0x501" /D "_CONSOLE" /D "CALC_EXPORTS" /D "_USRDLL" /D "_WINDLL" /D "_WINDOWS" /W4 /IE:\Python27\include /IE:\boost\boost_1_51 Calc_py.cpp /link /dll /LIBPATH:E:\Python27\libs /LIBPATH:E:\boost\boost_1_51\lib /OUT:calc.pyd
 */

#include "algorithms/sw/SW_py.hpp"
#include "algorithms/SimilaritySW_py.hpp"
#include "algorithms/kmp/KMP.hpp"
#include "algorithms/bm/BM.hpp"
#include "algorithms/blast/Alignment.hpp"
#include "algorithms/blast/Blast.hpp"
#include "algorithms/Utils.hpp"

#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

using namespace boost::python;

BOOST_PYTHON_MODULE(calc)
{
	// =============================== KLASY POMOCNICZE ====================================

	// -------------------------------- SIMILARITY SW --------------------------------------
	class_<algorithms::SimilaritySW_py>("SimilaritySW", init<>())
		.def(init<int, std::string, std::string, int, int>())
		.def("getValue", &algorithms::SimilaritySW_py::getValue)
		.def("getText", &algorithms::SimilaritySW_py::getText)
		.def("getPattern", &algorithms::SimilaritySW_py::getPattern)
		.def("getPositionI", &algorithms::SimilaritySW_py::getPositionI)
		.def("getPositionJ", &algorithms::SimilaritySW_py::getPositionJ)
	;

	class_<algorithms::Positions>("Positions")
		.def(vector_indexing_suite<algorithms::Positions>())
	;

	// ================================== ALGORYTMY ========================================

	// --------------------------------- ALGORYTM SW ---------------------------------------
	class_<algorithms::SW_py>("SW", init<>())
		.def(init<int, int, int, int>())
		.def("fastInitAndCompute", &algorithms::SW_py::fastInitAndCompute)
		.def("fastComputeWithStringsResult", &algorithms::SW_py::fastComputeWithStringsResult)
		.def("compute", &algorithms::SW_py::compute)
		.def("backtrack", &algorithms::SW_py::backtrack)
		.def("getSimilarity", &algorithms::SW_py::getSimilarity)
		.add_property("similarity",
			&algorithms::SW_py::get_similarity,
			&algorithms::SW_py::set_similarity)
	;

	// --------------------------------- ALGORYTM KMP --------------------------------------
	class_<algorithms::KMP>("KMP", init<>())
		.def("calculateTable", &algorithms::KMP::calculateTable)
		.def("compute", &algorithms::KMP::compute)
		.def("computeFast", &algorithms::KMP::computeFast)
	;

	// --------------------------------- ALGORYTM BM ---------------------------------------
	class_<algorithms::BM>("BM", init<>())
		.def("prepare", &algorithms::BM::prepare)
		.def("compute", &algorithms::BM::compute)
		.def("computeFast", &algorithms::BM::computeFast)
	;

	// -------------------------------- ALGORYTM BLAST -------------------------------------

	/**
	 * Wektor przyrownan
	 */
	class_<algorithms::Alignments>("Alignments")
			.def(vector_indexing_suite<algorithms::Alignments>())
	;

	/**
	 * Klasa przyrownania
	 */
	class_<algorithms::Alignment>("Alignment", init<std::string, int, int, int, int>())
		.def("getDropOff", &algorithms::Alignment::getDropOff)
		.def("getScore", &algorithms::Alignment::getScore)
		.def("getSame", &algorithms::Alignment::getSame)
		.def("getGaps", &algorithms::Alignment::getGaps)
		.def("getSeqEnd", &algorithms::Alignment::getSeqEnd)
		.def("getSeqStart", &algorithms::Alignment::getSeqStart)
		.def("getPatEnd", &algorithms::Alignment::getPatEnd)
		.def("getPatStart", &algorithms::Alignment::getPatStart)
		.def("getSequenceId", &algorithms::Alignment::getSequenceId)
		.def("getAlignLength", &algorithms::Alignment::getAlignLength)
	;

	/**
	 * Klasa algorytmu BLAST
	 */
	class_<algorithms::BLAST>("Blast", init<int, double, int>())
		.def("prepare", &algorithms::BLAST::prepare)
		.def("addSequence", &algorithms::BLAST::addSequence)
		.def("search", &algorithms::BLAST::search)
		.def("estimate", &algorithms::BLAST::estimate)
		.def("extend", &algorithms::BLAST::extend)
		.def("evaluate", &algorithms::BLAST::evaluate)
		.def("run", &algorithms::BLAST::run)
		.def("printWords", &algorithms::BLAST::printWords)
		.def("printAligns", &algorithms::BLAST::printAligns)
		.def("printAlignsFrom", &algorithms::BLAST::printAlignsFrom)
		.def("getAligns", &algorithms::BLAST::getAligns)
		.def("getBestAlign", &algorithms::BLAST::getBestAlign)
		.def("getAlignString", &algorithms::BLAST::getAlignString)
		.def("getMinRate", &algorithms::BLAST::getMinRate)
		.def("getMaxRate", &algorithms::BLAST::getMaxRate)
		.def("getAvgRate", &algorithms::BLAST::getAvgRate)
	;
}
