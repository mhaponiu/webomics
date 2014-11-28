#pragma once

#include <vector>

#include "SW.hpp"
#include "../Similarity.hpp"
#include "../SimilaritySW_py.hpp"

namespace algorithms
{
	class SW_py
	{
		public:
			/**
			 * Konstruktor domyslny
			 */
			SW_py();

			/**
			 * Konstruktor
			 */
			SW_py(int w_match, int w_mismatch, int w_open, int w_extend);

			/**
			 * Destruktor
			 */
			~SW_py();

			/**
			 *
			 */
			int fastInitAndCompute(int w_match, int w_mismatch, int w_open, int w_extend, std::string text, std::string pattern);

			/**
			 *
			 */
			SimilaritySW_py fastComputeWithStringsResult(int w_match, int w_mismatch, int w_open, int w_extend, std::string text, std::string pattern);

			/**
			 * Funkcja obliczajaca podobienstwo wzorca pattern oraz tekstu text
			 * @param text: Tekst, do ktorego por�wnywany jest wzorzec
			 * @param pattern: Wzorzec
			 * @return: Max wartos� oceny podobie�stwa
			 */
			int compute(std::string text, std::string pattern);

			/**
			 *
			 */
			SimilaritySW_py backtrack();

			/**
			 *
			 */
			SimilaritySW_py getSimilarity();

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
			int getGapOpen() const;

			/**
			 *
			 */
			void setGapOpen(int open);

			/**
			 *
			 */
			int getGapExtend() const;

			/**
			 *
			 */
			void setGapExtend(int extend);

			// Funkcje dla Pythona

			/**
			 *
			 */
			void set_similarity(SimilaritySW_py similarity);

			/**
			 *
			 */
			SimilaritySW_py get_similarity() const;

		private:
			/**
			 * Wskaznik na obiekt klasy algorytmu
			 */
			SW * sw;

			/**
			 * Miara podobienstwa porownywanych tekstow
			 */
			SimilaritySW_py * similarity;
	};

}
