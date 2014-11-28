/**
 * @author: Piotr Róż, Paweł Zieliński
 * @note: Plik testujący klasę BLAST - metoda extend - specyficzny przypadek
 * Kompilacja: cl /EHsc /I E:\boost\boost_1_51 test_extend.cpp ..\Blast.cpp ..\Word.cpp ..\Alignment.cpp
 */

#include <iostream>
#include <string>

#include "../Blast.hpp"

int main(int argc, char *args[])
{
	algorithms::BLAST * blast = new algorithms::BLAST(11, 0.05, 5);

	bool result = blast->prepare("ACCGGUAGAGCAC"); //13

	std::cout << "\nWynik PREPARE: " << result << std::endl << std::endl;

	blast->addSequence("0","GGCAUACCGGUAGAGCCAACGCAGUGUGAC");
	blast->addSequence("1","AGACCGGUAGAGCACGGCACACCGGUAGAGCAC");
	blast->addSequence("1","GACCGGUAGAGCACC");

//	result = blast->search();
//
//	std::cout << "\nWynik SEARCH: " << result << "\n" << std::endl;
//
//	result = blast->estimate();
//
//	std::cout << "\nWynik ESTIMATE: " << result << "\n" << std::endl;
//
//	//blast->printWords();
//
//	result = blast->extend();
//
//	std::cout << "\nWynik EXTEND: " << result << "\n" << std::endl;
//
//	result = blast->evaluate();
//
//	std::cout << "\nWynik EVALUATE: " << result << "\n" << std::endl;
//
//	algorithms::Alignments aligns = blast->getAligns(10);
//	blast->printAlignsFrom(aligns);

	//blast->printAligns();

	algorithms::Alignments aligns = blast->run(5);
	std::cout << blast->getAlignString(aligns) << std::endl;
	//blast->printAlignsFrom(aligns);

	return 0;
}
