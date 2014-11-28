/**
 * @file: Calc_py.cpp
 *
 * @author: Piotr Roz, Pawel Zielinski
 *
 * @date: 28.12.2012
 *
 * @description: Plik zawierajacy opakowanie kodu w C++, tak aby mozliwe byloby wykorzystanie go z poziomu kodu Pythona
 */

#include <boost/python.hpp>
#include <boost/python/class.hpp>
#include <boost/python/class_fwd.hpp>
#include <vector>
#include <string>

#include "Blast.hpp"
#include "Alignment.hpp"

using namespace std;

typedef std::vector<int> IntVect;

/**
 * Funckje potrzebne, aby moc w pelni operowac na obiekcie std::vector z poziomu kodu Pythona
 */
template<typename V>
struct item
{
	typedef std::vector<V, std::allocator<V> > Vec;

    static const V get(const Vec & x, int i)
    {
        if(i < 0)
			i += x.size();
        if(i >= 0 && i < x.size())
        	return x[i];
    }

    static void set(Vec & x, int i, const V & v)
    {
        if(i < 0)
			i += x.size();
        if(i >= 0 && i < x.size())
			x[i] = v;
    }

    static void del(Vec & x, int i)
    {
        if(i < 0)
			i += x.size();
        if(i >= 0 && i < x.size())
        {
			typename Vec::iterator iter;
			iter = x.begin();
			for(int j = 0; j < i; ++j, ++iter);
			x.erase(iter);
		}
    }

    static void add(Vec & x, const V & v)
    {
        x.push_back(v);
    }

    static bool in(const Vec & x, const V & v)
    {
        typename Vec::const_iterator iter;
        iter = x.begin();

		for(; iter != x.end(); ++iter)
			if(*iter == v)
				return true;
		return false;
    }

    static int index(const Vec & x, const V & v )
    {
		int i = 0;
		typename Vec::const_iterator iter = x.begin();
		for(; iter != x.end(); ++iter, ++i)
			if(*iter == v) return i;
		return -1;
    }

    static int count(const Vec & x, const V & v )
    {
		int i = 0;
		typename Vec::const_iterator iter = x.begin();
		for(; iter != x.end(); ++iter)
			if(*iter == v) ++i;
		return i;
    }
};

using namespace boost::python;

/**
 * Definicja modulu calc widocznego z poziomu Pythona
 */
BOOST_PYTHON_MODULE(calc)
{
	/**
	 * Wektor obiektow typu integer
	 */
	class_<IntVect>("IntVect")
		.def("__len__", &IntVect::size)
		.def("clear", &IntVect::clear)
		.def("append", &item<IntVect>::add, with_custodian_and_ward<1,2>())
		.def("__getitem__", &item<IntVect>::get)
		.def("__setitem__", &item<IntVect>::set, with_custodian_and_ward<1,2>())
		.def("__delitem__", &item<IntVect>::del)
		.def("__contains__", &item<IntVect>::in)
		.def("index", &item<IntVect>::index)
		.def("count", &item<IntVect>::count)
		;

	/**
	 * Wektor przyrownan
	 */
	class_<algorithms::Alignments>("Alignments")
		.def("__len__", &algorithms::Alignments::size)
		.def("clear", &algorithms::Alignments::clear)
		.def("append", &item<algorithms::Alignments>::add, with_custodian_and_ward<1,2>())
		.def("__getitem__", &item<algorithms::Alignments>::get)
		.def("__setitem__", &item<algorithms::Alignments>::set, with_custodian_and_ward<1,2>())
		.def("__delitem__", &item<algorithms::Alignments>::del)
		;

	/**
	 * Klasa przyrownania
	 */
	class_<algorithms::Alignment>("Alignment", init<int, int, int, int, int>())
		.def("getDropOff", &algorithms::Alignment::getDropOff)
		.def("getScore", &algorithms::Alignment::getScore)
		.def("getSame", &algorithms::Alignment::getSame)
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
