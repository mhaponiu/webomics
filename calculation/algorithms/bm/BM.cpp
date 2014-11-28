#include "BM.hpp"

namespace algorithms
{
	BM::BM()
	{
		this->tables_calculated = false;
	}

	void BM::prepare(std::string pattern)
	{
		this->pattern = pattern;
		this->buildBadCharacterShiftTable(pattern);
		this->buildGoodSuffixShiftTable(pattern);
		this->tables_calculated = true;
	}

	Positions BM::compute(std::string text)
	{
		if(this->tables_calculated == false)
			return Positions();

		Positions positions;

		int pattern_size = this->pattern.size();
		int text_size = text.size();

		int i;
		int j = 0;

		while(j <= text_size - pattern_size)	// dopoki okno wzorca miesci sie wewnatrz przeszukiwanego lancucha
		{
			for(i = pattern_size - 1; i >= 0 && this->pattern[i] == text[i + j]; --i);
			if(i < 0)
			{
				positions.push_back(j + 1);	// Od 1, zamiast od 0
				j += this->goodSuffixShift[0];
			}
			else
			{
				j += std::max(this->goodSuffixShift[i], this->badCharacterShift[text[i + j]] - pattern_size + i + 1);
			}
		}

		return positions;
	}

	Positions BM::computeFast(std::string pattern, std::string text)
	{
		this->prepare(pattern);
		return this->compute(text);
	}

	void BM::buildBadCharacterShiftTable(std::string pattern)
	{
		int pattern_size = pattern.size();

		this->badCharacterShift.assign(ASIZE, pattern_size);

		for(int i = 0; i < pattern_size - 1; ++i)
		{
			this->badCharacterShift[pattern[i]] = pattern_size - i - 1;
		}

		/*for(int i = 0; i < this->badCharacterShift.size(); ++i)
		{
			std::cout << this->badCharacterShift[i] <<  std::endl;
		}*/
	}

	void BM::buildSuffixTable(std::string pattern)
	{
		int pattern_size = pattern.size();
		int j;

		this->suffix.assign(pattern_size, -1);
		this->suffix[pattern_size - 1] = pattern_size;

		for(int i = pattern_size - 2; i >= 0; --i)
		{
			for(j = 0; j <= i && pattern[i - j] == pattern[pattern_size - j - 1]; j++);
			this->suffix[i] = j;
		}

		/*for(int i = 0; i < this->suffix.size(); ++i)
		{
			std::cout << this->suffix[i] <<  std::endl;
		}*/
	}

	void BM::buildGoodSuffixShiftTable(std::string pattern)
	{
		int j = 0;
		int pattern_size = pattern.size();

		this->buildSuffixTable(pattern);
		this->goodSuffixShift.assign(pattern_size, pattern_size);

		for(int i = pattern_size - 1; i >= 0; --i)
		{
			if(this->suffix[i] == i + 1)
			{
				for(; j < pattern_size - i - 1; ++j)
				{
					this->goodSuffixShift[j] = pattern_size - i - 1;
				}
			}
		}

		for(int i = 0; i <= pattern_size - 2; ++i)
		{
			this->goodSuffixShift[pattern_size - this->suffix[i] - 1] = pattern_size - i - 1;
		}

		/*for(int i = 0; i < this->goodSuffixShift.size(); ++i)
		{
			std::cout << this->goodSuffixShift[i] <<  std::endl;
		}*/
	}
}
