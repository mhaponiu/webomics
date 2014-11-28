#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

#include "../Utils.hpp"

namespace algorithms
{
	class KMP
	{
		public:
			/**
			 * Konstruktor
			 */
			KMP() {}

			/**
			 * Funkcja oblicza tabele pomocnicza dla wzoraca
			 * @param pattern: Wzorzec, ktory jest wyszukiwany
			 * @return: 0 wszystko w porzadku, 1 w przeciwnym wypadku
			 */
			int calculateTable(std::string pattern);

			/**
			 * Funkcja wyszukujaca wzorzec pattern w tekscie text
			 * @param text: Tekst, w ktorych wyszukiwany jest wzorzec
			 * @return: Wektor pozycji, na ktorych wzorzec pattern znajduje sie w tekscie text
			 */
			Positions compute(std::string text);

			/**
			 * Funkcja wyszukujaca wzorzec pattern w tekscie text
			 * @param pattern: Wzorzec, ktory jest wyszukiwany
			 * @param text: Tekst, w ktorych wyszukiwany jest wzorzec
			 * @return: Wektor pozycji, na ktorych wzorzec pattern znajduje sie w tekscie text
			 */
			Positions computeFast(std::string pattern, std::string text);


		private:
			/**
			 * Tablica pomocnicza danego wzorca
			 */
			std::vector<int> P;

			/**
			 * Zmienna okreslajaca czy tablica pomocnicza zostala policzona
			 */
			bool table_calculated;

			/**
			 * Wzorzec pattern
			 */
			std::string pattern;
	};

}
