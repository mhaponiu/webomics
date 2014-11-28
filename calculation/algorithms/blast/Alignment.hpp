/**
 * @file: Alignment.hpp
 *
 * @author: Piotr Roz, Pawel Zielinski
 *
 * @date: 28.12.2012
 *
 * @description: Plik zawierajacy deklaracje klasy Alignment przechowujacej informacje o procesie przyrownywania dwoch sekwencji
 */

#pragma once

#include <iostream>
#include <vector>
#include <string>

namespace algorithms
{
	/**
	 * Klasa przechowujaca informacje o procesie przyrownania wzorca pattern (lub jego fragmentu) do slowa sequence (lub jego fragmentu).
	 */
	class Alignment
	{
		public:
			// ---------------------------------------------------------------------------------
			// Metody publiczne klasy
			// ---------------------------------------------------------------------------------

			/**
			 * Konstruktor
			 *
			 * @param seq_id: wartosc ID sekwencji z bazy danych
			 *
			 * @param seq_start: indeks poczatku podsekwencji w oryginalej sekwencji z bazy danych
			 *
			 * @param seq_end: indeks konca podsekwencji w oryginalnej sekwencji z bazy danych
			 *
			 * @param pat_start: indeks poczatku podsekwencji w rozpatrywanym wzorcu
			 *
			 * @param pat_end: indeks konca podsekwencji w rozpatrywanym wzorcu
			 */
			Alignment(std::string seq_id, int seq_start, int seq_end, int pat_start, int pat_end);

			/**
			 * Zwrocenie parametru okreslajacego maksymalne odchylenie wartosci oznaczajacej wartosc punktacji dopasowania
			 * od pozycji maksymalnej
			 *
			 * @return: aktualne maksymalne odchylenie wartosci oznaczajacej wartosc punktacji dopasowania od pozycji maksymalnej
			 */
			int getDropOff();

			/**
			 * Ustawinie wartosci parametru okreslajacego maksymalne odchylenie wartosci oznaczajacej wartosc punktacji dopasowania
			 * od pozycji maksymalnej
			 *
			 * @param dropOff: maksymalne odchylenie wartosci oznaczajacej wartosc punktacji dopasowania od pozycji maksymalnej
			 */
			void setDropOff(int dropOff);

			/**
			 * Zwiekszenie o jednosc parametru okreslajacego maksymalne odchylenie wartosci oznaczajacej wartosc punktacji dopasowania
			 * od pozycji maksymalnej
			 *
			 * @return: aktualne maksymalne odchylenie wartosci oznaczajacej wartosc punktacji dopasowania od pozycji maksymalnej
			 */
			int incDropOff();

			/**
			 * Zmniejszenie o jednosc parametru okreslajacego maksymalne odchylenie wartosci oznaczajacej wartosc punktacji dopasowania
			 * od pozycji maksymalnej
			 *
			 * @return: aktualne maksymalne odchylenie wartosci oznaczajacej wartosc punktacji dopasowania od pozycji maksymalnej
			 */
			int decDropOff();

			/**
			 * Zwrocenie wartosci parametru okreslajacego aktualna wartosc punktacji dopasowania porownywanych sekwencji
			 *
			 * @return: parametr okreslajacy aktualna wartosc punktacji dopasowania porownywanych sekwencji
			 */
			int getScore();

			/**
			 *	Ustawienie wartosci parametru okreslajacego aktualna wartosc punktacji dopasowania porownywanych sekwencji
			 *
			 *	@param score: aktualna wartosc punktacji dopasowania porownywanych sekwencji
			 */
			void setScore(int score);

			/**
			 * Zwiekszenie o jednosc aktualnej wartosci punktacji dopasowania porownywanych sekwencji
			 *
			 * @return: aktualna wartosc punktacji dopasowania porownywanych sekwencji
			 */
			int incScore();

			/**
			 * Zmniejszenie o jednosc aktualnej wartosci punktacji dopasowania porownywanych sekwencji
			 *
			 * @return: aktualna wartosc punktacji dopasowania porownywanych sekwencji
			 */
			int decScore();

			/**
			 * Zwrocenie wartosci parametru okreslajacego ilosc identycznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 *
			 * @return: ilosc identycznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 */
			int getSame();

			/**
			 * Ustawienie wartosci parametru okreslajacego ilosc identycznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 *
			 * @param same: ilosc identycznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 */
			void setSame(int same);

			/**
			 * Zwiekszenie o jednosc wartosci parametru okreslajacego ilosc identycznych reszt w rozpatrywanych sekwencjach na tych
			 * samych pozycjach
			 *
			 * @return ilosc identycznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 */
			int incSame();

			/**
			 * Zwrocenie wartosci parametru okreslajacego ilosc roznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 *
			 * @return: ilosc roznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 */
			int getGaps();

			/**
			 * Ustawienie wartosci parametru okreslajacego ilosc roznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 *
			 * @param gaps: ilosc roznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 */
			void setGaps(int gaps);

			/**
			 * Zwiekszenie o jednosc wartosci parametru okreslajacego ilosc roznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 *
			 * @return: ilosc roznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 */
			int incGaps();

			/**
			 * Zwrocenie wartosci parametru okreslajacego indeks konca podsekwencji w oryginalej sekwencji z bazy danych
			 *
			 * @return: indeks konca podsekwencji w oryginalej sekwencji z bazy danych
			 */
			int getSeqEnd();

			/**
			 * Ustawienie wartosci parametru okreslajacego indeks konca podsekwencji w oryginalej sekwencji z bazy danych
			 *
			 * @param seqEnd: indeks konca podsekwencji w oryginalej sekwencji z bazy danych
			 */
			void setSeqEnd(int seqEnd);

			/**
			 * Zwiekszenie o jednosc wartosci parametru okreslajacego indeks konca podsekwencji w oryginalej sekwencji z bazy danych
			 *
			 * @return: indeks konca podsekwencji w oryginalej sekwencji z bazy danych
			 */
			int incSeqEnd();

			/**
			 * Zwrocenie wartosci parametru okreslajacego indeks poczatku podsekwencji w oryginalej sekwencji z bazy danych
			 *
			 * @return: indeks poczatku podsekwencji w oryginalej sekwencji z bazy danych
			 */
			int getSeqStart();

			/**
			 * Zwrocenie wartosci parametru okreslajacego indeks poczatku podsekwencji w oryginalej sekwencji z bazy danych
			 *
			 * @param seqStart: indeks poczatku podsekwencji w oryginalej sekwencji z bazy danych
			 */
			void setSeqStart(int seqStart);

			/**
			 * Zmniejszenie o jednosc wartosci parametru okreslajacego indeks poczatku podsekwencji w oryginalej sekwencji z bazy danych
			 *
			 * @return: indeks poczatku podsekwencji w oryginalej sekwencji z bazy danych
			 */
			int decSeqStart();

			/**
			 * Zwrocenie wartosci parametru okreslajacego indeks konca podsekwencji w rozpatrywanym wzorcu
			 *
			 * @return: indeks konca podsekwencji w rozpatrywanym wzorcu
			 */
			int getPatEnd();

			/**
			 * Ustawienie wartosci parametru okreslajacego indeks konca podsekwencji w rozpatrywanym wzorcu
			 *
			 * @param patEnd: indeks konca podsekwencji w rozpatrywanym wzorcu
			 */
			void setPatEnd(int patEnd);

			/**
			 * Zwiekszenie o jednosc wartosci parametru okreslajacego indeks konca podsekwencji w rozpatrywanym wzorcu
			 *
			 * @return: indeks konca podsekwencji w rozpatrywanym wzorcu
			 */
			int incPatEnd();

			/**
			 * Zwrocenie wartosci parametru okreslajacego indeks poczatku podsekwencji w rozpatrywanym wzorcu
			 *
			 * @return: indeks poczatku podsekwencji w rozpatrywanym wzorcu
			 */
			int getPatStart();

			/**
			 * Ustawienie wartosci parametru okreslajacego indeks poczatku podsekwencji w rozpatrywanym wzorcu
			 *
			 * @param patStart: indeks poczatku podsekwencji w rozpatrywanym wzorcu
			 */
			void setPatStart(int patStart);

			/**
			 * Zmniejszenie o jednosc wartosci parametru okreslajacego indeks poczatku podsekwencji w rozpatrywanym wzorcu
			 *
			 * @return: indeks poczatku podsekwencji w rozpatrywanym wzorcu
			 */
			int decPatStart();

			/**
			 * Zwrocenie wartosci parametru okreslajacego ID rozpatrywanej sekwencji z bazy danych
			 *
			 * @return: ID rozpatrywanej sekwencji z bazy danych
			 */
			std::string getSequenceId();

			/**
			 * Ustawienie wartosci parametru okreslajacego ID rozpatrywanej sekwencji z bazy danych
			 *
			 * @param sequenceId: ID rozpatrywanej sekwencji z bazy danych
			 */
			void setSequenceId(std::string sequenceId);

			/**
			 * Zwrocenie wartosci parametru okreslajacego aktualna dlugosc dopasowania
			 *
			 * @return aktualna dlugosc dopasowania
			 */
			int getAlignLength();

			/**
			 * Operator mniejszosciowy
			 *
			 * @param a: obiekt klasy Alignment, z ktorym nastepuje porownanie
			 *
			 * @return: prawda, jezeli obiekt jest mniejszy od zadanego argumentem obiektem a, w przecinym wypadku - falsz.
			 */
			bool operator<(const Alignment & a) const;

			/**
			 * Operator wiekszosciowy
			 *
			 * @param a: obiekt klasy Alignment, z ktorym nastepuje porownanie
			 *
			 * @return: prawda, jezeli obiekt jest wiekszy od zadanego argumentem obiektem a, w przecinym wypadku - falsz.
			 */
			bool operator>(const Alignment & a) const;

			/**
			 * Operator przyrownania
			 *
			 * @param a: obiekt klasy Alignment, z ktorym nastepuje porownanie
			 *
			 * @return: prawda, jezeli obiekt jest identyczny z zadanym argumentem obiektem a, w przecinym wypadku - falsz.
			 */
			bool operator==(const Alignment & a) const;

		protected:
			// ---------------------------------------------------------------------------------
			// Zmienne i metody chronione klasy
			// ---------------------------------------------------------------------------------

			/**
			 * ID sekwencji z bazy danych
			 */
			std::string sequence_id_;

			/**
			 * Aktualne maksymalne odchylenie wartosci oznaczajacej wartosc punktacji dopasowania od pozycji maksymalnej
			 */
			int drop_off_;

			/**
			 * Aktualna wartosc punktacji dopasowania porownywanych sekwencji
			 */
			int score_;

			/**
			 * Ilosc identycznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 */
			int same_;

			/**
			 * Ilosc roznych reszt w rozpatrywanych sekwencjach na tych samych pozycjach
			 */
			int gaps_;

			/**
			 * Indeks poczatku podsekwencji w oryginalej sekwencji z bazy danych
			 */
			int seq_start_;

			/**
			 * Indeks konca podsekwencji w oryginalej sekwencji z bazy danych
			 */
			int seq_end_;

			/**
			 * Indeks poczatku podsekwencji w rozpatrywanym wzorcu
			 */
			int pat_start_;

			/**
			 * Indeks konca podsekwencji w rozpatrywanym wzorcu
			 */
			int pat_end_;
	};

	/**
	 * Wektor obiektow klasy Alignment
	 */
	typedef std::vector<Alignment> Alignments;
}
