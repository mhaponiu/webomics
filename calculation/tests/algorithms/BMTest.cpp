/**
 * @author: Piotr Róż
 * @note: Plik testujacy algorytm Boyera-Moorea
 * Kompilacja: cl /EHsc /I E:\boost\boost_1_51 BMTest.cpp ..\..\algorithms\bm\BM.cpp
 */

#include <iostream>
#include <string>
#include <vector>

#include "../../algorithms/bm/BM.hpp"

using namespace std;

int main(int argc, char *args[])
{
	string text;
	string pattern;

	text = "BABABAABBBBBBBBBBBAAAAABAABAAAABBBBBBABAABABBBABABABBAABABBAAAAAABAAABBABBABBBBA";
	pattern = "BBABA";

	cout << endl << "Twoj wzorzec: " << pattern << endl << "Twoj tekst: " << text << endl;

	algorithms::BM * bm = new algorithms::BM();
	bm->prepare(pattern);
	algorithms::Positions positions = bm->compute(text);

	cout << endl << "Indeksy poczatku wzorca w tekscie:" << endl;
	vector<int>::iterator it = positions.begin();
	for(; it != positions.end(); ++it)
		cout << *it << ",";
	cout << endl;

	return 0;
}
