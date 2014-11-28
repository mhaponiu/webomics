/**
 * Klasa wrapera dla kodu Pythona przechowuj�ca informacje o wyniku dzia�a algorytmu SW
 * @author: Piotr R�
 */

#pragma once

#include <string>
#include <vector>

namespace algorithms
{
	class SimilaritySW_py
	{
		public:
			/**
			 * Konstruktor domyslny
			 */
			SimilaritySW_py();

			/**
			 * Konstruktor
			 */
			SimilaritySW_py(int value, std::string text_form, std::string pattern_form, int position_i, int position_j);

			/**
			 *
			 */
			int getValue();

			/**
			 *
			 */
			std::string getText();

			/**
			 *
			 */
			std::string getPattern();

			/**
			 *
			 */
			int getPositionI();

			/**
			 *
			 */
			int getPositionJ();

		private:
			/**
			 * Wartos� podobie�stwa tekstu oraz wzorca
			 */
			int value;

			/**
			 * Kszta�t tekstu po przyr�wnaniu do wzorca (wstawienia, usuniecia itd)
			 */
			std::string text_form;

			/**
			 * Kszta�t wzorca po przyr�wnaniu do tekstu (wstawienia, usuniecia itd)
			 */
			std::string pattern_form;

			int position_i;

			int position_j;
	};
}
