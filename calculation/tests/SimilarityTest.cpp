/**
 * @author: Piotr Ró¿
 * @note: Plik testuj¹cy klasê Similarity
 * Kompilacja: cl /EHsc /I E:\boost\boost_1_51 SimilarityTest.cpp ..\algorithms\Similarity.cpp
 */

#include <iostream>
#include <string>

#include "../algorithms/Similarity.hpp"

int main(int argc, char *args[])
{
	algorithms::Similarity * similarity = new algorithms::Similarity();
	similarity->setValuesSW(7, 1, 8);

	std::cout << similarity->getValue() << std::endl;
	std::cout << similarity->getPoistionI() << std::endl;
	std::cout << similarity->getPositionJ() << std::endl;

	return 0;
}
