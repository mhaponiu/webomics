#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <utility> // std::pair
#include <tuple>

#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <boost/algorithm/minmax_element.hpp>

#include "../Similarity.hpp"

namespace algorithms
{
	typedef std::tuple<std::string, std::string> StringTuple;
	typedef std::vector<CellSW> CellsVector;
	typedef std::vector<std::tuple<int, int> > RouteVector;

	class SW
	{
		public:
			/**
			 * Konstruktor domyslny
			 */
			SW();

			/**
			 * Konstruktor
			 */
			SW(int w_match, int w_mismatch, int open, int extend);

			/**
			 *
			 */
			int computeFast(std::string text, std::string pattern);

			/**
			 * Funkcja obliczajaca podobienstwo wzorca pattern oraz tekstu text
			 * @param text: Tekst, do ktorego porównywany jest wzorzec
			 * @param pattern: Wzorzec
			 * @return: Obiekt typu Similarity
			 */
			Similarity compute(std::string text, std::string pattern);

			/**
			 * Funkcja rysujaca macierz dopasowan
			 * @param matrix: Macierz, która ma zostać narysowana
			 */
			void printMatrix(RatingsMatrix matrix);

			/**
			 * Funkcja rysujaca macierz dopasowan z etykietami
			 * @param matrix: Macierz, która ma zostać narysowana
			 * @param text: Tekst
			 * @param pattern: Wzorzec
			 */
			void printMatrix(RatingsMatrix matrix, std::string text, std::string pattern);

			/**
			 *
			 */
			RouteVector backtrack(Similarity similarity);

			/**
			 *
			 */
			void printSimilarity(Similarity similarity, RouteVector route);

			/**
			 *
			 */
			StringTuple getSimilarityStrings(Similarity similarity, RouteVector route);

			// ---------------------------------------------------------------------------------
			// GETTERY i SETTERY
			// ---------------------------------------------------------------------------------

			/**
			 *
			 */
			Similarity getSimilarity() const;

			/**
			 *
			 */
			void setSimilarity(Similarity h);


			/**
			 *
			 */
			int getMatch() const;

			/**
			 *
			 */
			void setMatch(int match);

			/**
			 *
			 */
			int getMismatch() const;

			/**
			 *
			 */
			void setMismatch(int mismatch);

			/**
			 *
			 */
			int getOpen() const;

			/**
			 *
			 */
			void setOpen(int open);

			/**
			 *
			 */
			int getExtend() const;

			/**
			 *
			 */
			void setExtend(int extend);

		protected:
			// ---------------------------------------------------------------------------------
			// Zmienne chronione klasy (parametry algorytmu oraz przechowujace informacje
			// o podobieństwie porównywanych sekwencji)
			// ---------------------------------------------------------------------------------

			/**
			 * Obiekt przechowujacy informacje o podobieństwie dwóch tekstów
			 */
			Similarity similarity;

			/**
			 * Koszt prawidłowego dopasowania
			 */
			int w_match;

			/**
			 * Koszt błędnego dopasowania
			 */
			int w_mismatch;

			/**
			 * Koszt otworzenia dziury
			 */
			int w_open;

			/**
			 * Koszt rozszerzenia dziury
			 */
			int w_extend;

			// ---------------------------------------------------------------------------------
			// Funkcje pomocnicze
			// ---------------------------------------------------------------------------------

			/**
			 * Funkcja inicjujaca macierz dopasowań
			 * @param m: Ilosc znakow tekstu text
			 * @param n: Ilosc znakow wzorca pattern
			 * @return: Macierz dopasowań
			 */
			RatingsMatrix buildMatrix(unsigned long int m, unsigned long int n);

			/**
			 *
			 */
			CellSW getMaxElem(CellsVector value_position_vector);
	};

}
