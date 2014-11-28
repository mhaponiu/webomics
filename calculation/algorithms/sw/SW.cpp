#include "SW.hpp"

namespace algorithms
{
	SW::SW()
	{
		this->w_match = 2;
		this->w_mismatch = -1;
		this->w_open = -1;
		this->w_extend = -1;
	}

	SW::SW(int w_match, int w_mismatch, int w_open, int w_extend)
	{
		this->w_match = w_match;
		this->w_mismatch = w_mismatch;
		this->w_open = w_open;
		this->w_extend = w_extend;
	}

	int SW::computeFast(std::string text, std::string pattern)
	{
		// Macierz ocen dopasowania
		RatingsMatrix matrix = buildMatrix(text.length(), pattern.length());

		// Maksymalna wartosć podobieństwa
		int max_value = 0;

		// Wypełnienie macierzy ocen
		for (unsigned long int i = 1; i < matrix.size1(); ++ i)	// Po wierszach
		{
			for (unsigned long int j = 1; j < matrix.size2(); ++ j) // Po kolumnach
			{
				#ifdef DEBUG
				std::cout << "Jestem w (" << i << "; " << j << ")" << std::endl;
				#endif
				// W(i)=g+hi(for i>= 1)
				CellsVector vpv;
				vpv.push_back(CellSW(i - 1, j - 1, matrix(i - 1, j - 1).getValue() + (text[i - 1] == pattern[j - 1] ? this->w_match : this->w_mismatch))); 					// Od skosu (gora-lewa)
				vpv.push_back(CellSW(i - 1, j, matrix(i - 1, j).getValue() + (matrix(i - 1, j).getGap() == true ? this->w_extend : (this->w_open + this->w_extend)))); 		// Od gory
				vpv.push_back(CellSW(i, j - 1, matrix(i, j - 1).getValue() + (matrix(i, j - 1).getGap() == true ? this->w_extend : (this->w_open + this->w_extend)))); 		// Od lewej
				vpv.push_back(CellSW(-1, -1, 0));																															// Ostatni warunek algorytmu

				CellSW cell_max = getMaxElem(vpv);

				// Afiniczna funkcja kary za przerwy
				if(cell_max.getI() != i - 1 || cell_max.getJ() != j - 1) // Dziura
					cell_max.setGap(true);
				else
					cell_max.setGap(false);

				#ifdef DEBUG
				std::cout << "\tPrzyszedlem z (" << cell_max.getI() << "; " << cell_max.getJ() << ");\tDziura?\t" << cell_max.getGap() << ";\tWartosc:" << cell_max.getValue() << std::endl;
				#endif

				matrix(i, j) = cell_max;
				if(cell_max.getValue() >= max_value)
					max_value = cell_max.getValue();
			}
		}

		return max_value;
	}

	Similarity SW::compute(std::string text, std::string pattern)
	{
		// Macierz ocen dopasowania
		RatingsMatrix matrix = buildMatrix(text.length(), pattern.length());

		// Maksymalna wartosć podobieństwa
		int max_value = 0;

		// Indeks poziomy maksymalnej wartosci
		unsigned long int position_i;

		// Indeks pionowy maksymalnej wartosci
		unsigned long int position_j;

		// Wypełnienie macierzy ocen
		for (unsigned long int i = 1; i < matrix.size1(); ++ i)	// Po wierszach
		{
			for (unsigned long int j = 1; j < matrix.size2(); ++ j) // Po kolumnach
			{
				#ifdef DEBUG
				std::cout << "Jestem w (" << i << "; " << j << ")" << std::endl;
				#endif
				// W(i)=g+hi(for i>= 1)
				CellsVector vpv;
				vpv.push_back(CellSW(i - 1, j - 1, matrix(i - 1, j - 1).getValue() + (text[i - 1] == pattern[j - 1] ? this->w_match : this->w_mismatch))); 					// Od skosu (gora-lewa)
				vpv.push_back(CellSW(i - 1, j, matrix(i - 1, j).getValue() + (matrix(i - 1, j).getGap() == true ? this->w_extend : (this->w_open + this->w_extend)))); 		// Od gory
				vpv.push_back(CellSW(i, j - 1, matrix(i, j - 1).getValue() + (matrix(i, j - 1).getGap() == true ? this->w_extend : (this->w_open + this->w_extend)))); 		// Od lewej
				vpv.push_back(CellSW(-1, -1, 0));																															// Ostatni warunek algorytmu

				CellSW cell_max = getMaxElem(vpv);

				// Afiniczna funkcja kary za przerwy
				if(cell_max.getI() != i - 1 || cell_max.getJ() != j - 1) // Dziura
					cell_max.setGap(true);
				else
					cell_max.setGap(false);

				#ifdef DEBUG
				std::cout << "\tPrzyszedlem z (" << cell_max.getI() << "; " << cell_max.getJ() << ");\tDziura?\t" << cell_max.getGap() << ";\tWartosc:" << cell_max.getValue() << std::endl;
				#endif

				matrix(i, j) = cell_max;
				if(cell_max.getValue() >= max_value)
				{
					max_value = cell_max.getValue();
					position_i = i;
					position_j = j;
				}
			}
		}

		this->similarity.setValuesSW(max_value, position_i, position_j);		// Wartosci dla algorytmu SW
		this->similarity.setMatrix(matrix);										// Macierz dopasowania
		this->similarity.setTextForm(text);										// Tekst porównywany
		this->similarity.setPatternForm(pattern);								// Wzorzec porównywany

		return this->similarity;
	}

	RatingsMatrix SW::buildMatrix(unsigned long int m, unsigned long int n)
	{
		// H(m + 1, n + 1)
		RatingsMatrix matrix(m + 1, n + 1);

		// H(i, 0) = 0; 0 <= i <= m
		for(unsigned long int i = 0; i < matrix.size1(); ++i)
			matrix(i, 0) = algorithms::CellSW(0, 0, 0);

		// H(0, j) = 0; 0 <= j <= n
		for(unsigned long int j = 0; j < matrix.size2(); ++j)
			matrix(0, j) = algorithms::CellSW(0, 0, 0);

		return matrix;
	}

	void SW::printMatrix(RatingsMatrix matrix)
	{
		for (unsigned long int i = 0; i < matrix.size1(); ++ i)
		{
			for (unsigned long int j = 0; j < matrix.size2(); ++ j)
				std::cout << matrix(i, j).getValue() << "\t";
			std::cout << std::endl;
		}
	}

	void SW::printMatrix(RatingsMatrix matrix, std::string text, std::string pattern)
	{
		text = "-" + text;
		pattern = "--" + pattern;

		// Etykiety gorne
		for(unsigned long int i = 0; i < pattern.length(); ++i)
			std::cout << " " << pattern[i] << "\t";
		std::cout << std::endl;

		// Macierz z etykietami bocznymi
		for (unsigned long int i = 0; i < matrix.size1(); ++ i)
		{
			std::cout << text[i] << "\t";
			for (unsigned long int j = 0; j < matrix.size2(); ++ j)
			{
				#ifdef DEBUG
					if(matrix(i, j).getI() == i - 1 && matrix(i, j).getJ() == j - 1)
						std::cout << "\\" << matrix(i, j).getValue() << "\t";
					else if(matrix(i, j).getI() == i && matrix(i, j).getJ() == j - 1)
						std::cout << "=" << matrix(i, j).getValue() << "\t";
					else if(matrix(i, j).getI() == i - 1 && matrix(i, j).getJ() == j)
						std::cout << "|" << matrix(i, j).getValue() << "\t";
					else
						std::cout << " " << matrix(i, j).getValue() << "\t";
				#else
					std::cout << " " << matrix(i, j).getValue() << "\t";
				#endif
			}
			std::cout << std::endl;
		}
	}

	RouteVector SW::backtrack(Similarity similarity)
	{
		RouteVector route;

		// Pozycje maksymalnej wartosci oceny dopasowania
		int pos_i = similarity.getPoistionI();
		int pos_j = similarity.getPositionJ();

		// Macierz ocen dopasowania
		RatingsMatrix matrix = similarity.getMatrix();

		// Powracamy odtwarzajac kolejne punkty
		while(matrix(pos_i, pos_j).getValue() != 0)
		{
			pos_i = matrix(pos_i, pos_j).getI();
			pos_j = matrix(pos_i, pos_j).getJ();

			// Dodanie punktu do trasy
			route.push_back(std::make_tuple(pos_i, pos_j));

			// Nie mamy gdzie isc :(
			if(pos_i == -1 || pos_j == -1)
				break;
		}

		std::reverse(route.begin(), route.end());

		return route;
	}

	void SW::printSimilarity(Similarity similarity, RouteVector route)
	{
		std::string text = similarity.getTextForm();
		std::string pattern = similarity.getPatternForm();

		RouteVector::iterator it = route.begin();

		// Wypisanie tekstu
		for(; it != route.end(); ++it)
		{
			// Idziemy w dol
			if(std::get<0>(*it) == std::get<0>(*(it + 1)))
				std::cout << "-";
			else
				std::cout << text[std::get<0>(*it)];
		}

		// -----------------------------------------------------------
		std::cout << std::endl;
		// -----------------------------------------------------------

		it = route.begin();

		// Wypisanie wzorca
		for(; it != route.end(); ++it)
		{
			// Idziemy w prawo
			if(std::get<1>(*it) == std::get<1>(*(it + 1)))
				std::cout << "-";
			else
				std::cout << pattern[std::get<1>(*it)];
		}
	}

	StringTuple SW::getSimilarityStrings(Similarity similarity, RouteVector route)
	{
		StringTuple strings;
		std::string new_text;
		std::string new_pattern;

		std::string text = similarity.getTextForm();
		std::string pattern = similarity.getPatternForm();

		RouteVector::iterator it = route.begin();

		for(; it != route.end(); ++it)
		{
			// Idziemy w dol
			if(std::get<0>(*it) == std::get<0>(*(it + 1)))
				new_text += "-";
			else
				new_text += text[std::get<0>(*it)];

			// Idziemy w prawo
			if(std::get<1>(*it) == std::get<1>(*(it + 1)))
				new_pattern += "-";
			else
				new_pattern += pattern[std::get<1>(*it)];
		}

		strings = std::make_tuple(new_text, new_pattern);
		return strings;
	}

	CellSW SW::getMaxElem(CellsVector cellsVector)
	{
		// Maksymalny element
		CellSW max_cell;

		CellsVector::iterator it = cellsVector.begin();
		max_cell = *it;

		for(; it != cellsVector.end(); ++it)
			if((*it).getValue() > max_cell.getValue())
				max_cell = *it;

		return max_cell;
	}

	Similarity SW::getSimilarity() const
	{
		return this->similarity;
	}

	void SW::setSimilarity(Similarity sim)
	{
		this->similarity = sim;
	}

	int SW::getMatch() const
	{
		return this->w_match;
	}

	void SW::setMatch(int match)
	{
		this->w_match = match;
	}

	int SW::getMismatch() const
	{
		return this->w_mismatch;
	}

	void SW::setMismatch(int mismatch)
	{
		this->w_mismatch = mismatch;
	}

	int SW::getOpen() const
	{
		return this->w_open;
	}

	void SW::setOpen(int open)
	{
		this->w_open = open;
	}

	int SW::getExtend() const
	{
		return this->w_extend;
	}

	void SW::setExtend(int extend)
	{
		this->w_extend = extend;
	}
}
