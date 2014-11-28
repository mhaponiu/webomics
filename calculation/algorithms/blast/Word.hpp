/**
 * @file: Word.hpp
 *
 * @author: Piotr Roz, Pawel Zielinski
 *
 * @date: 28.12.2012
 *
 * @description: Plik zawierajacy deklaracje klasy Word przechowujacej informacje o fragmencie wzorca, z ktorym skojarzone sa obiekty
 * klasy Alignment - kolejne przyrownania
 */

#pragma once

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

#include "Alignment.hpp"

namespace algorithms
{
	/**
	 * Klasa przechowujaca informacje o fragmencie wzorca, ktory przyrownywany jest do kolejnych sekwencji z bazy danych
	 */
	class Word
	{
		public:
			// ---------------------------------------------------------------------------------
			// Metody publiczne klasy
			// ---------------------------------------------------------------------------------

			/**
			 * Konstruktor
			 *
			 * @param ID: ID danego slowa - fragmentu wzorca
			 *
			 * @param pat_start: indeks poczatku podsekwencji w rozpatrywanym wzorcu - indeks poczatku danego slowa
			 *
			 * @param pat_end: indeks konca podsekwencji w rozpatrywanym wzorcu - indeks poczatku danego slowa
			 */
			Word(int ID, int pat_start, int pat_end);

			/**
			 * Zwrocenie wartosci parametru okreslajacego ID danego slowa
			 *
			 * @return: ID danego slowa
			 */
			int getID();

			/**
			 * Zwiekszenie o jednosc wartosci parametru okreslajacego ilosc wystapien danego slowa w sekwencjach w bazie danych
			 */
			void incCount();

			/**
			 * Ustawienie wartosci parametru okreslajacego ilosc wystapien danego slowa w sekwencjach w bazie danych
			 *
			 * @param count: ilosc wystapien danego slowa w sekwencjach w bazie danych
			 */
			void setCount(int count);

			/**
			 * Zwrocenie wartosci parametru okreslajacego ilosc wystapien danego slowa w sekwencjach w bazie danych
			 *
			 * @return: ilosc wystapien danego slowa w sekwencjach w bazie danych
			 */
			int getCount();

			/**
			 * Ustawienie wartosci parametru okreslajacego istotnosc danego slowa na proces przyrownania i wyboru najbardziej dopasowanych sekwencji
			 *
			 * @param rate: istotnosc danego slowa na proces przyrownania i wyboru najbardziej dopasowanych sekwencji
			 */
			void setRate(double rate);

			/**
			 * Zwrocenie wartosci parametru okreslajacego istotnosc danego slowa na proces przyrownania i wyboru najbardziej dopasowanych sekwencji
			 *
			 * @return: istotnosc danego slowa na proces przyrownania i wyboru najbardziej dopasowanych sekwencji
			 */
			double getRate();

			/**
			 * Dodanie przyrownania danego slowa do kolejnej sekwencji z bazy danych
			 *
			 * @param seq_id: wartosc ID sekwencji z bazy danych
			 *
			 * @param seq_start: indeks poczatku podsekwencji w oryginalej sekwencji z bazy danych
			 *
			 * @param seq_end: indeks konca podsekwencji w oryginalnej sekwencji z bazy danych
			 *
			 * @param pat_start: indeks poczatku slowa w rozpatrywanym wzorcu
			 *
			 * @param pat_end: indeks konca slowa w rozpatrywanym wzorcu
			 */
			void addAlign(std::string seq_id, int seq_start, int seq_end, int pat_start, int pat_end);

			/**
			 * Zwrocenie parametru okreslajacego wektor przyrownan danego slowa do kolejnych sekwencji z bazy danych
			 *
			 * @return: wektor przyrownan danego slowa do kolejnych sekwencji z bazy danych
			 */
			Alignments getAligns();

			/**
			 * Ustawienie parametru okreslajacego wektor przyrownan danego slowa do kolejnych sekwencji z bazy danych
			 *
			 * @param aligns: wektor przyrownan danego slowa do kolejnych sekwencji z bazy danych
			 */
			void setAligns(Alignments aligns);

			/**
			 * Zwrocenie wartosci parametru okreslajacego indeks konca slowa we wzorcu
			 *
			 * @return: indeks konca slowa we wzorcu
			 */
			int getPatEnd();

			/**
			 * Ustawienie wartosci parametru okreslajacego indeks konca slowa we wzorcu
			 *
			 * @param patEnd: indeks konca slowa we wzorcu
			 */
			void setPatEnd(int patEnd);

			/**
			 * Zwiekszenie o jednosc wartosci parametru okreslajacego indeks konca slowa we wzorcu
			 *
			 * @return: indeks konca slowa we wzorcu
			 */
			int incPatEnd();

			/**
			 * Zwrocenie wartosci parametru okreslajacego indeks poczatku slowa we wzorcu
			 *
			 * @return: indeks poczatku slowa we wzorcu
			 */
			int getPatStart();

			/**
			 * Ustawienie wartosci parametru okreslajacego indeks poczatku slowa we wzorcu
			 *
			 * @param patStart: indeks poczatku slowa we wzorcu
			 */
			void setPatStart(int patStart);

			/**
			 * Zmniejszenie o jednosc wartosci parametru okreslajacego indeks poczatku slowa we wzorcu
			 *
			 * @return: indeks poczatku slowa we wzorcu
			 */
			int decPatStart();

			/**
			 * Zwrocenie informacji czy sekwencja o zadanym ID znajduje sie w wektorze przyrownan do danego slowa
			 *
			 * @param seq_id: ID poszukiwanej sekwencji
			 *
			 * @return: prawda w przypadku obecnosci poszukiwanej sekwencji, falsz w przecinym wypadku
			 */
			bool findSeqID(std::string);

			/**
			 * Zwrocenie informacji o ilosci przyrownan do danego slowa
			 *
			 * @return: ilosc przyrownan do danego slowa
			 */
			int getAlignCount();

		protected:
			// ---------------------------------------------------------------------------------
			// Zmienne chronione klasy
			// ---------------------------------------------------------------------------------

			/**
			 * ID danego slowa - fragmentu wzorca
			 */
			int ID_;

			/**
			 * Indeks poczatku podsekwencji w rozpatrywanym wzorcu - indeks poczatku danego slowa
			 */
			int pat_start_;

			/**
			 * Indeks konca podsekwencji w rozpatrywanym wzorcu - indeks konca danego slowa
			 */
			int pat_end_;

			/**
			 * Ilosc wystapien danego slowa w sekwencjach w bazie danych
			 */
			int count_;

			/**
			 * Istotnosc danego slowa na proces przyrownania i wyboru najbardziej dopasowanych sekwencji
			 */
			double rate_;

			/**
			 * Wektor przyrownan danego slowa do kolejnych sekwencji z bazy danych
			 */
			std::vector<Alignment> aligns_;
	};

	/**
	 * Wektor slow
	 */
	typedef std::vector<Word> Words;
}
