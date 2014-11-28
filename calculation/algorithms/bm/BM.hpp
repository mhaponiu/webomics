#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

#include "../Utils.hpp"

namespace algorithms
{
	class BM
	{
		public:
			/**
			 * Konstruktor
			 */
			BM();

			/**
			 * Przygotowanie struktur pomocnicznych, zbudowanie odpowiednich tablic
			 * @param pattern: sekwencja wzorca
			 */
			void prepare(std::string pattern);

			/**
			 * Własciwy algorytm wyszukiwania wzorca
			 * @param text: tekst przeszukiwany
			 * @return Wektor pozycji, na których znaleziony został wzorzec
			 */
			Positions compute(std::string text);

			/**
			 * Szybkie, jednoczesne przygotowanie pomocnicznych tablic oraz uruchomienie własciwego algorytmu
			 * @param pattern: sekwencja wzorca
			 * @param text: przeszukiwany tekst
			 * @return Wektor pozycji, na których znaleziony został wzorzec
			 */
			Positions computeFast(std::string pattern, std::string text);

		private:

			/**
			 * Zmienna okreslajaca czy tablice pomocnicze zostaly policzone
			 */
			bool tables_calculated;

			/**
			 * Wzorzec pattern
			 */
			std::string pattern;

			/**
			 * Tablica bad character shift
			 */
			std::vector<int> badCharacterShift;

			/**
			 * Tablica good suffix shift
			 */
			std::vector<int> goodSuffixShift;

			/**
			 * Tablica przyrostków
			 */
			std::vector<int> suffix;

			const static int ASIZE = 255;

			/**
			 * Wypełnienie tablicy bad character shift
			 * @param pattern: Wzorzec
			 */
			void buildBadCharacterShiftTable(std::string pattern);

			/**
			 * Wypełnienie tablicy przyrostków
			 * @param pattern: Wzorzec
			 */
			void buildSuffixTable(std::string pattern);

			/**
			 * Wypełnienie tablicy good suffix shift
			 * @param pattern: Wzorzec
			 */
			void buildGoodSuffixShiftTable(std::string pattern);
	};

}
