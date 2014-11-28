#pragma once

#include <string>
#include <vector>

#include "sw/CellSW.hpp"

#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>

namespace algorithms
{
	typedef boost::numeric::ublas::matrix<algorithms::CellSW> RatingsMatrix;

	class Similarity
	{
		public:
			/**
			 * Konstruktor domyslny
			 */
			Similarity() {}

			/**
			 * Ustawienie podstawowych wartosci parametr�w dla algorytmu SW
			 */
			void setValuesSW(int value, int position_i, int position_j);

			/**
			 *
			 */
			RatingsMatrix getMatrix();

			/**
			 *
			 */
			void setMatrix(RatingsMatrix matrix);

			/**
			 * Zwrocenie wartosci podobienstwa porownywanych tekstow
			 */
			int getValue();

			/**
			 *
			 */
			void setValue(int value);

			/**
			 * Zwrocenie formy tekstu po przyr�wnaniu go do wzorca
			 */
			std::string getTextForm();

			/**
			 *
			 */
			void setTextForm(std::string textForm);

			/**
			 * Zwrocenie formy wzorca po przyr�wnaniu go do tekstu
			 */
			std::string getPatternForm();

			/**
			 *
			 */
			void setPatternForm(std::string patternForm);

			/**
			 *
			 */
			int getPoistionI();

			/**
			 *
			 */
			int getPositionJ();

			/**
			 *
			 */
			void setPositionI(int positionI);

			/**
			 *
			 */
			void setPositionJ(int positionJ);

		protected:
			/**
			 * Macierz ocen dopasowan
			 */
			RatingsMatrix matrix;

			/**
			 * Wartos� podobie�stwa tekstu oraz wzorca
			 */
			int value;

			/**
			 * Indeks poziomy, na ktorym znajduje si� maksymalna wartos� w macierzy
			 */
			int position_i;

			/**
			 * Indeks pionowy, na ktorym znajduje si� maksymalna wartos� w macierzy
			 */
			int position_j;

			/**
			 * Kszta�t tekstu po przyr�wnaniu do wzorca (wstawienia, usuniecia itd)
			 */
			std::string text_form;

			/**
			 * Kszta�t wzorca po przyr�wnaniu do tekstu (wstawienia, usuniecia itd)
			 */
			std::string pattern_form;
	};

	/**
	 * Wektor miar podobie�stwa
	 */
	typedef std::vector<Similarity> SimilarityVector;
}
