/**
 * @file: Blast.hpp
 *
 * @author: Piotr Roz, Pawel Zielinski
 *
 * @date: 29.12.2012
 *
 * @description: Plik zawierajacy deklaracje klasy Blast - glownej klasy algorytmu

 * Etapy:
 * 1. inicjacja: podzial analizowanej sekwencji na fragmenty o dlugosci W (= 11 dla DNA)
 * 2. wyszukiwanie: wyszukiwanie w bazie danych rekordów, które zawieraja te slowa
 * 3. ocena: usuwane sa rekordy z niska ocena
 * 4. rozszerzanie
 *
 * inicjacja:
 * 		podzial szukanej sekwencji na slowa
 * 		przyklad: zalozmy, ze poszukujemy slowa ACTTATCA, wszystkie slowa o dlugosci W=5 dla sekwencji ACTTATCA: ACTTA, CTTAT, TTATC, TATCA
 *
 * 		KONSTRUTOR, ktory przyjmuje 3 parametry:			DOMYSLNE WARTOSCI DLA DNA
 * 			- dlugosc slowa 					W						11
 * 			- minimalna wartosc oceny 			T						0.005
 * 			- minimalna wartosc dopasowania 	C						5				- drop off - ilosc mismatch przy rozszerzaniu
 *
 * 		funkcja PREPARE, ktora przyjmuje WZORZEC SLOWA (string) zas zwraca true/false czy udalo sie podzielic slowo wzorcowe.
 * 			zapisuje ona do tablicy slowa dlugosci W, ktore beda wyszukiwane w bazie
 *
 * wyszukiwanie:
 * 		wybieranie z bazy rekordów posiadajacych dane slowo
 *
 * 		funkcja SEARCH, ktora przyjmuje tablice (vector) obiektów cpp::SearchObject(ID, type, sequence) i wyszukuje w kazdej sekwencji z bazy
 * 		kazdego ze slow i w jakiejs mapie odchacza ile razy dane slowo bylo znalezione.
 *
 * 		Moze dodatkowo zbierac informacje, gdzie dane slowo zostalo znalezione, zeby pozniej znowu nie szukac w calej bazie.
 * 		Potem jak w ESTIMATE ograniczymy zbior slow --> automatycznie ograniczymy zbior sekwencji z bazy, bo wezmiemy tylko te, ktore zawieraja
 * 		wybrane slowa.
 *
 * ocena:
 * 		przekazywane sa slowa, które maja ocene (waga) wieksza niz T,
 * 		waga slowa: iloraz liczby wystapien danego slowa do liczby wystapien wszystkich slów
 *
 * 		funkcja ESTIMATE, ktora dla kazdego slowa wyznacza ocene i zwraca liste slow (zapisuje w klasie rowniez) z waga wieksza niz T
 *
 * rozszerzanie:
 * 		próbuje wydluzyc znalezione dopasowania (nie stosuje sie przerw)
 * 			rozszerzanie znalezionych obszarów (w lewo lub w prawo)
 * 			nie uwzglednia przerw
 * 			az wartosc dopasowania spadnie ponizej C
 * 			do oceny stosuje algorytm dokladny (Shmita-Watermana)
 *
 * 		funkcja EXTEND, ktora wydluza znalezione dopasowania; jezeli wartosc dopasowania (HSP?) < C, to zaprzestaje rozszerzania;
 * 		czy wartosc dopasowania == E-value?!!?!!
 * 		nastepnie oblicza wartosc dopasowania sekwencji algorytmem SW,
 *
 * 		HSP - high-scoring segment pair - ciagly, niezawierajacy przerw segment przyrownanych par
 *
 * 		Moze HSP to najzwyklejsze przyrownanie znak po znaku? +za zgodnosc, -za niezgodnosc reszt??
 *
 * 		E - m x n x P (E-value, wartosc oczekiwana) = K x n x m x e ^ (- lambda x S)
 * 		m - calkowita liczba reszt w bazie danych
 * 		n - liczba reszt badanej sekwencji
 * 		P - prawdopodobienstwo, ze dane przyrownanie HSP jest wynikiem przypadku
 *
 * 		K - stala
 * 		lambda - stala
 * 		S - score, jaki?
 *
 *
 * NIEJASNOŚĆ: gdzie jest ograniczany zbior? ktore sekwencje sa najpodobniejsze,
 * skoro ocena wartosci dopasowania kazdej z nich wynosi okolo C? <-- w EVALUEATE?
 *
 * OPIS Z KSIAŻKI:
 * In NCBI-BLAST, BLASTN is very different from the other, protein-based algorithms.
 * BLASTN seeds are always identical words; T is never used. To make BLASTN faster,
 * you increase W and to make it more sensitive, you decrease W. The minimum word size is 7.
 * The two-hit algorithm isn't used in BLASTN searches because word hits are generally rare with large, identical words.
 *
 */


#pragma once

#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <tuple>
#include <sstream>
#include <limits>
#include <cmath>

#include <boost/lexical_cast.hpp>

#include "Word.hpp"

namespace algorithms
{
	/**
	 * Mapa opisujaca sekwencje z bazy danych: kluczem jest ID sekwencji, zas wartoscia sama sekwencja w postaci tekstu
	 */
	typedef std::map<std::string, std::string> Sequences;

	/**
	 * Klasa algorytmu BLAST
	 */
	class BLAST
	{
		public:
			/**
			 * Konstruktor
			 *
			 * @param w: dlugosc slowa - na fragmenty takiej dlugosci dzielona jest sekwencja wzorca
			 *
			 * @param t: minimalna wartosc oceny, ktora determinuje wybor wybieranych do dalszych etapow slow Word
			 *
			 * @param c: wartosc parametru drop off, informujacego o maksymalnym odchyleniu wartosci punktacji dopasowania od pozycji maksymalnej
			 * przy rozszerzaniu slowa Word
			 */
			BLAST(int w, double t, int c);

			/**
			 * Inicjalizacja - podzial analizowanej sekwencji pattern na fragmenty o dlugosci W
			 *
			 * @param: Sekwencja poddawana analizie i podzialowi
			 *
			 * @return: prawda w przypadku powodzenia, falsz w przeciwnym wypadku. Jezeli dlugosc sekwencji pattern jest mniejsza od ustawionego parametru W, zwracana
			 * jest wartosc falszu
			 */
			bool prepare(std::string pattern);

			/**
			 * Dodanie nowej sekwencji do mapy
			 *
			 * @param id: ID sekwencji z bazy danych
			 *
			 * @param sequence: sekwencja nukletydowa
			 */
			void addSequence(std::string id, std::string sequence);

			/**
			 * Wyszukiwanie - wyszukiwanie w bazie danych rekordów, które zawieraja slowa o dlugosci W
			 *
			 * @return: prawda w przypadku powodzenia, falsz w przeciwnym wypadku
			 */
			bool search();

			/**
			 * Ocena - usuwanie slow, które maja ocene (waga) mniejsza niz T, przy czym waga slowa rozumiana jest jako iloraz liczby wystapien danego slowa
			 * do liczby wystapien wszystkich slów
			 *
			 * @return: prawda w przypadku powodzenia, falsz w przeciwnym wypadku. Jezeli ilosc slow w tym kroku wyniesie zero (co oznacza za duze restrykcje parametrowe),
			 * zwrocona zostanie wartosc zero.
			 */
			bool estimate();

			/**
			 * Odrzucenie tych sekwencji, ktore nie znajduja sie na liscie przyrownan zadnego ze slow
			 *
			 * @return: prawda w przypadku powodzenia, falsz w przeciwnym wypadku. Jezeli ilosc sekwencji w tym kroku wyniesie zero (co oznacza za duze
			 * restrykcje parametrowe), zwrocona zostanie wartosc zero.
			 */
			bool filterSeqs();

			/**
			 * Rozszerzenie - proba wydluzenia znalezionych dopasowan zarowno w lewo jak i w prawo do momentu az maksymalne odchyleniu wartosci oznaczajacej
			 * wartosc punktacji dopasowania od pozycji maksymalnej bedzie wieksza lub rowna parametrowi C
			 *
			 * @return: prawda w przypadku powodzenia, falsz w przeciwnym wypadku.
			 */
			bool extend();

			/**
			 * Funkcja niepotrzebna ze wzgledu na to, ze w algorytmie BLASTn wartosc score jest analogiczna do wartosci e-value. Jednak pozostawiona, poniewaz w przyszlosci moze istniec potrzeba jej zaimplementowania
			 * do konca. Do konca, poniewaz istnieje funkcja evaluateOne, ktora dla pojedycznego przyrownania liczy wartos e-value.
			 */
			bool evaluate();

			/**
			 * Obliczenie wartosci wskaznika E-value dla wskazanego jako argument dopasowania
			 *
			 * @param align: dopasowanie, dla ktorego wyliczana jest wartosc wskaznika E-value
			 *
			 * @return: wartosc wskaznika E-value
			 */
			double evaluateOne(Alignment align);

			/**
			 * Obliczenie wartosci wskaznika P-value wedlug wskaznika E-value
			 *
			 * @param e_value: wartosc wskaznika E-value
			 *
			 * @return: wartosc wskaznika P-value
			 */
			double pValueEval(double e_value);

			/**
			 * Automatyczne uruchomienie algorytmu BLAST, wykonanie kolejnych krokow zadanych funkcjami:
			 * 	 search
			 * 	 estimate
			 * 	 extend
			 * 	 evaluate
			 *
			 * @param how_much: ilosc najlepszych dopasowan, ktore maja zostac zwrocone
			 *
			 * @return: wektor najlepszych dopasowan
			 */
			Alignments run(unsigned int how_much = 0);

			/**
			 * Wypisanie informacji o slowach oraz ich dopasowaniach
			 */
			void printWords();

			/**
			 * Wypisanie informacji o wszystkich dopasowaniach (lub najlepszych ograniczonych parametrem how_much)
			 *
			 * @param how_much: ilosc najlepszych dopasowan, ktore maja zostac zwrocone
			 */
			void printAligns(unsigned int how_much = 0);

			/**
			 * Wypisanie informacji o zadanych dopasowaniach
			 *
			 * @param aligns: wektor najlepszych dopasowan, ktore maja zostac wypisane
			 */
			void printAlignsFrom(Alignments aligns);

			/**
			 * Zwrocenie wektora najlepszych dopasowan
			 *
			 * @param how_much: ilosc najlepszych dopasowan, ktore maja zostac zwrocone
			 *
			 * @return: wektor najlepszych dopasowan
			 */
			Alignments getAligns(unsigned int how_much = 0);

			/**
			 * Zwrocenie najlepszego dopasowania
			 *
			 * @return: najlepsze dopasowanie
			 */
			Alignment getBestAlign();

			/**
			 * Zwrocenie tekstu zawierajacego informacje o szczegolach dopasowania najblizszych sekwencji
			 *
			 * @param aligns: wektor najlepszych dopasowan, dla ktorych ma zostac wzrocony wynik w postaci tekstu
			 *
			 * @return:
			 */
			std::string getAlignString(Alignments aligns);

			/**
			 * Minimalna wartosc parametru T ustawiana w przypadku zbytniego ograniczenia zbioru sekwencji (do zera)
			 */
			double getMinRate();

			/**
			 * Maksymalna wartosc parametru T ustawiana w przypadku zbytniego ograniczenia zbioru sekwencji (do zera)
			 */
			double getMaxRate();

			/**
			 * Srednia wartosc parametru T ustawiana w przypadku zbytniego ograniczenia zbioru sekwencji (do zera)
			 */
			double getAvgRate();

		protected:
			// ---------------------------------------------------------------------------------
			// Zmienne chronione klasy
			// ---------------------------------------------------------------------------------

			/**
			 * Dlugosc slowa - na fragmenty takiej dlugosci dzielona jest sekwencja wzorca
			 */
			int W_;

			/**
			 * Minimalna wartosc oceny, ktora determinuje wybor wybieranych do dalszych etapow slow Word
			 */
			double T_;

			/**
			 * Wartosc parametru drop off, informujacego o maksymalnym odchyleniu wartosci punktacji dopasowania od pozycji maksymalnej
			 * przy rozszerzaniu slowa Word
			 */
			int C_;

			/**
			 * Minimalna wartosc parametru T ustawiana w przypadku zbytniego ograniczenia zbioru sekwencji (do zera)
			 */
			double min_rate_;

			/**
			 * Maksymalna wartosc parametru T ustawiana w przypadku zbytniego ograniczenia zbioru sekwencji (do zera)
			 */
			double max_rate_;

			/**
			 * Srednia wartosc parametru T ustawiana w przypadku zbytniego ograniczenia zbioru sekwencji (do zera)
			 */
			double avg_rate_;

			/**
			 * Wektor slow, na ktore zostal podzielony wzorzec
			 */
			Words words_;

			/**
			 * Wektor wszystkich sekwencji z bazy danych
			 */
			Sequences sequences_;

			/**
			 * Ilosc wszystkich slow powstalych ze wzorca
			 */
			int words_count_;

			/**
			 * Sekwencja wzorca
			 */
			std::string pattern_;

			/**
			 * Zwrocenie tekstu wzorca ograniczonego zadanymi indeksami
			 *
			 * @param pos_start: indeks poczatku slowa w rozpatrywanym wzorcu
			 *
			 * @param pos_end: indeks konca slowa w rozpatrywanym wzorcu
			 *
			 * @return: fragment wzorca ograniczonego indekstami
			 */
			std::string getSubPattern(int pos_start, int pos_end);

			/**
			 * Zwrocenie tekstu sekwencji z bazy o zadanym ID oraz ograniczonego podanymi indeksami
			 *
			 * @param seq_id: ID sekwencji, ktorego fragment sekwencji jest zwracany
			 *
			 * @param pos_start: indeks poczatku sekwencji w rozpatrywej sekwencji nukleotydowej
			 *
			 * @param pos_end: indeks konca sekwencji w rozpatrywej sekwencji nukleotydowej
			 *
			 * @return: fragment sekwencji nukleotydowej ograniczonej indeksami
			 */
			std::string getSubSequence(std::string seq_id, int pos_start, int pos_end);

			/**
			 * Zwrocenie tekstu sekwencji z bazy danych o zadanym ID
			 *
			 * @param seq_id: ID, ktorego sekwencja jest poszukiwana
			 *
			 * @return: sekwencja z bazy danych
			 */
			std::string getSequence(std::string seq_id);

			/**
			 * Zwrocenie tekstu wzorca dla zadanego slowa
			 *
			 * @param word: slowo, dla ktorego sekwencja ma byc zwrocona
			 *
			 * @return: sekwencja slowa
			 */
			std::string getWordSequence(Word word);

			/**
			 * Sprawdzenie identycznosci znakow wystepujacych na zadanych pozycjach w sekwencji oraz we wzorcu
			 *
			 * @param sequence: rozpatrywana sekwencja z bazy danych
			 *
			 * @param pattern_pos: indeks we wzorcu
			 *
			 * @param sequence_pos: indeks w sekwencji z bazy danych
			 *
			 * @return: prawda w przypadku identycznosci wskazanych indeksami znakow, falsz w przeciwnym wypadku
			 */
			bool charEqual(std::string sequence, int pattern_pos, int sequence_pos);

			/**
			 * Tekst opisujacy wizualne dopasowanie wskazanych w argumentach sekwencji
			 *
			 * @param pattern: sekwencja wzorca
			 *
			 * @param sequence: sekwencja z bazy danych
			 *
			 * @return: wizualne dopasowanie wskazanych sekwencji
			 */
			std::string getAlignMark(std::string pattern, std::string sequence);

			/**
			 * Zwrocenie sumy wszystkich dopasowan we wszystkich slowach
			 *
			 * @return: ilosc wszystkich dopasowan we wszystkich slowach
			 */
			int getAlignsSumInWords();
	};

}
