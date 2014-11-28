#include "KMP.hpp"

namespace algorithms
{
	int KMP::calculateTable(std::string pattern)
	{
		// Zapamietanie wzorca
		this->pattern = pattern;

		int pattern_len = pattern.length();

		// Obliczenie tablicy pomocniczej
		P.push_back(0);
		P.push_back(0);
		int t = 0;
		for(int i = 2; i <= pattern_len; ++i)
		{
			while((t > 0) && (pattern[t] != pattern[i - 1]))
				t = P[t];
			if(pattern[t] == pattern[i - 1])
				++t;
			P.push_back(t);
		}

		// --- DEBUG
		/*std::cout << "DEBUG:" << std::endl;
		for(int i = 0; i < P.size(); ++i)
		{
			std::cout << "P[" << i << "] = " << P[i] << std::endl;
		}*/
		// --- END DEBUG

		this->table_calculated = true;

		return 0;
	}

	Positions KMP::compute(std::string text)
	{
		if(!this->table_calculated)
			return Positions();

		int text_len = text.length();
		int pattern_len = this->pattern.length();

		// Algorytm KMP
		Positions positions;
		int i = 1;
		int j = 0;
		while(i <= text_len - pattern_len + 1)
		{
			j = P[j];
			while((j < pattern_len) && (this->pattern[j] == text[i + j - 1]))
				++j;
			if(j == pattern_len)
				positions.push_back(i);
			i = i + std::max(1, j - P[j]);
		}

		return positions;
	}

	Positions KMP::computeFast(std::string pattern, std::string text)
	{
		this->calculateTable(pattern);
		return this->compute(text);
	}
}
