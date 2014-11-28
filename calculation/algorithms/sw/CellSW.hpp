/**
 * Klasa pojedynczej komorki macierzy dopasowania
 * @author: Piotr Róż
 */

#pragma once

namespace algorithms
{
	class CellSW
	{
		public:
			/**
			 * Domyslny konstruktor
			 */
			CellSW();

			/**
			 * Konstruktor
			 */
			CellSW(long int i, long int j, int value);

			long int getI();

			void setI(long int i);

			long int getJ();

			void setJ(long int j);

			int getValue();

			void setValue(int value);

			bool getGap();

			void setGap(bool gap);

		private:
			/**
			 * Indeks i skad przyszlismy
			 */
			long int i_;

			/**
			 * Indeks j skad przyszlismy
			 */
			long int j_;

			/**
			 * Wartosc w danej komorce
			 */
			int value_;

			/**
			 * Czy przyszlismy z dziury?
			 */
			bool gap_;
	};
}
