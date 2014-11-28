/**
 * @author: Piotr R�
 * @note: Plik testuj�cy algorytm Knutha-Morrisa-Pratta
 * Kompilacja: cl /EHsc /I E:\boost\boost_1_51 KMPTest.cpp ..\..\algorithms\kmp\KMP.cpp
 */

#include <iostream>
#include <string>
#include <vector>

#include "../../algorithms/kmp/KMP.hpp"

using namespace std;

int main(int argc, char *args[])
{
	string text;
	string pattern;

	text = "BABABAABBBBBBBBBBBAAAAABAABAAAABBBBBBABAABABBBABABABBAABABBAAAAAABAAABBABBABBBBA";
	pattern = "BBABA";

	cout << endl << "Twoj wzorzec: " << pattern << endl << "Twoj tekst: " << text << endl;

	algorithms::KMP * kmp = new algorithms::KMP();
	int status = kmp->calculateTable(pattern);
	vector<int> positions = kmp->compute(text);

	cout << endl << "Indeksy poczatku wzorca w tekscie:" << endl;
	vector<int>::iterator it = positions.begin();
	for(; it != positions.end(); ++it)
		cout << *it << ",";
	cout << endl;

	return 0;
}
