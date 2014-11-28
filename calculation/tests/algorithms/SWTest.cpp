/**
 * @author: Piotr R�
 * @note: Plik testuj�cy algorytm Smidtha-Watermana
 * Kompilacja: cl /EHsc /I E:\boost\boost_1_51 SWTest.cpp ..\..\algorithms\sw\CellSW.cpp ..\..\algorithms\Similarity.cpp ..\..\algorithms\sw\SW.cpp
 */

#include <iostream>
#include <string>

#include "../../algorithms/sw/SW.hpp"

int main(int argc, char *args[])
{
	//algorithms::SW * sw = new algorithms::SW(2, -1, -3, -1);
	//sw->compute("AGCACACA", "ACACACTA");
	algorithms::SW * sw = new algorithms::SW(2, -1, -3, -1);
	sw->compute("AAAB", "AABAB");
	//algorithms::SW * sw = new algorithms::SW(1, -1, -1, -1);
	//sw->compute("PELICAN", "COELACANTH");
	sw->printMatrix(sw->getSimilarity().getMatrix(), sw->getSimilarity().getTextForm(), sw->getSimilarity().getPatternForm());

	algorithms::RouteVector rvector = sw->backtrack(sw->getSimilarity());
	algorithms::RouteVector::iterator it = rvector.begin();
	for(; it != rvector.end(); ++it)
		std::cout << "(" << std::get<0>(*it) << "," << std::get<1>(*it) << ")" << std::endl;

	std::cout << "Podobienstwo sekwencji:" << std::endl;
	//sw->printSimilarity(sw->getSimilarity(), rvector);
	algorithms::StringTuple new_texts = sw->getSimilarityStrings(sw->getSimilarity(), rvector);
	std::cout << std::get<0>(new_texts) << std::endl;
	std::cout << std::get<1>(new_texts) << std::endl;

	return 0;
}
