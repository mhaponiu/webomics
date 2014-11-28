/**
 * @file: Blast.hpp
 *
 * @author: Piotr Roz, Pawel Zielinski
 *
 * @date: 29.12.2012
 *
 * @description: Plik zawierajacy definicje klasy Blast - glownej klasy algorytmu
 */

#include "Blast.hpp"
#include <omp.h>

namespace algorithms
{
	BLAST::BLAST(int w, double t, int c)
	{
		W_ = w;
		T_ = t;
		C_ = c;

		words_count_ = 0;
		min_rate_ = 0.0;
		max_rate_ = 0.0;
		avg_rate_ = 0.0;
	}

	bool BLAST::prepare(std::string pattern)
	{
		/*
		 * funkcja PREPARE, ktora przyjmuje WZORZEC SLOWA (string) zas zwraca true/false czy udalo sie podzielic slowo wzorcowe.
		zapisuje ona do tablicy slowa dlugosci W, ktore beda wyszukiwane w bazie
		 */

		pattern_ = pattern;

		// Dlugosc slowa
		int pattern_len = pattern.length();

		// Nie mozna podzielic, bo slowo jest za krotkie
		if(pattern_len < W_)
			return false;

		// Budujemy tablice ze slowami
		for(int i = 0; i <= pattern_len - W_; ++i)
		{
			std::string word = pattern.substr(i, W_);

			Word word_obj(i, i, i + word.length() - 1);
			words_.push_back(word_obj);
		}

		return true;
	}

	void BLAST::addSequence(std::string id, std::string sequence)
	{
		sequences_.insert(std::pair<std::string, std::string>(id, sequence));
	}

	bool BLAST::search()
	{
		// Po wszystkich slowach ze wzorca
		for(Words::iterator w = words_.begin(); w != words_.end(); ++w)
		{
			std::string word_seq = getWordSequence((*w));
			// Po wszystkich sekwencjach z bazy
			for(Sequences::iterator s = sequences_.begin(); s != sequences_.end(); ++s)
			{
				// Znajdujemy wszystkie wystapienia slowa W w sekwencji S
				size_t pos = (*s).second.find(word_seq, 0);
				while(pos != std::string::npos)
				{
					// Znalezlismy!
					(*w).incCount();
					// Dodajemy przyrownanie do wyrazu
					(*w).addAlign((*s).first, pos, pos + word_seq.length() - 1, (*w).getPatStart(), (*w).getPatEnd());

					++words_count_;

					// Szukamy dalej...
				    pos = (*s).second.find(word_seq, pos + 1);
				}
			}
		}

		if(words_count_ == 0)
			return false;

		return true;
	}

	bool BLAST::estimate()
	{
		double sum_rate = 0.0;
		double words_size = (double)words_.size();

		// Po wszystkich slowach ze wzorca - liczymy wage kazdego z nich
		for(Words::iterator w = words_.begin(); w != words_.end(); )
		{
			double rate = (double)(*w).getCount() / (double)words_count_;
			sum_rate += rate;
			(*w).setRate(rate);
			if(min_rate_ == 0.0)
				min_rate_ = rate;
			if(rate < min_rate_)
				min_rate_ = rate;
			if(rate > max_rate_)
				max_rate_ = rate;
			// Jezeli nie spelnia warunku to usuwamy!
			if(rate <= T_)
				w = words_.erase(w);
			else
				++w;
		}
		avg_rate_ = sum_rate / words_size;

		if(words_.size() == 0 || getAlignsSumInWords() == 0)
			return false;

		//return filterSeqs();
		return true;
	}

	bool BLAST::filterSeqs()
	{
		for(Sequences::iterator s = sequences_.begin(); s != sequences_.end(); )
		{
			bool found = false;
			// Szukamy danej sekwencji w tablicach kazdego ze slow
			for(Words::iterator w = words_.begin(); w != words_.end(); ++w)
			{
				if((*w).findSeqID((*s).first)) // Znaleziono
				{
					++s;
					found = true;
					break;
				}
			}
			// Jezeli nie ma nigdzie - usuwamy - sekwencja nie jest nam juz potrzebna - zwalniamy pamiec
			if(found == false)
				s = sequences_.erase(s);
		}

		if(sequences_.size() == 0)
			return false;

		return true;
	}

	bool BLAST::extend()
	{
		int i = 1;
		// Po wszystkich slowach ze wzorca
		for(Words::iterator w = words_.begin(); w != words_.end(); ++w)
		{
			Alignments alignments = (*w).getAligns();
			// Po kazdym znalezionym dopasowaniu slowa
			for(Alignments::iterator align = alignments.begin(); align != alignments.end(); ++align)
			{
				bool extend = true;
				std::string sequence = (*(sequences_.find((*align).getSequenceId()))).second;

				bool left_end = false;
				bool right_end = false;

				while(extend)
				{
					// !!! ROZSZERZAMY W LEWO

					// Czy w ogole mozemy rozszerzyc?
					if((*align).getPatStart() != 0 && (*align).getSeqStart() != 0)
					{
						// Sprawdzamy czy nastapil drop off - jezeli tak to uaktualniamy i sprawdzamy czy juz nie przekroczylismy
						int new_word_start = (*align).decPatStart();
						int new_align_start = (*align).decSeqStart();

						bool match = charEqual(sequence, new_word_start, new_align_start);
						int new_drop_off;
						if(match)
						{
							new_drop_off = (*align).decDropOff();
							(*align).incScore();
							(*align).incSame();
						}
						else
						{
							new_drop_off = (*align).incDropOff();
							(*align).decScore();
							(*align).incGaps();
						}

						if(new_drop_off >= C_)
							break;
					}
					else
						left_end = true;

					// !!! ROZSZERZAMY W PRAWO
					// Czy w ogole mozemy rozszerzyc?
					if((*align).getPatEnd() + 1 < pattern_.length() && (*align).getSeqEnd() + 1 < sequence.length())
					{
						// Sprawdzamy czy nastapil drop off - jezeli tak to uaktualniamy i sprawdzamy czy juz nie przekroczylismy
						int new_word_end = (*align).incPatEnd();
						int new_align_end = (*align).incSeqEnd();

						bool match = charEqual(sequence, new_word_end, new_align_end);
						int new_drop_off;
						if(match)
						{
							new_drop_off = (*align).decDropOff();
							(*align).incScore();
							(*align).incSame();
						}
						else
						{
							new_drop_off = (*align).incDropOff();
							(*align).decScore();
							(*align).incGaps();
						}

						if(new_drop_off >= C_)
							break;
					}
					else
						right_end = true;

					if(left_end == true && right_end == true)	// Nie mamy gdzie juz rozszerzac
						break;
				}
			}

			(*w).setAligns(alignments);
		}

		return true;
	}

	bool BLAST::evaluate()
	{
		return true;
	}

	double BLAST::evaluateOne(Alignment align)
	{
		double E_VALUE	= 0.0;
		double K 		= 0.13;
		double Lambda	= 0.318;
		double S		= (double)align.getScore();
		double M		= (double)pattern_.length();
		//double N		= (double)getSequence(align.getSequenceId()).length();
		double N		= (double)align.getAlignLength();

		// Znormalizowany score - bit-score
		double SN = (Lambda * S - log(K)) / log(2.0);

		// Im mniejsza wartosc tym lepiej - 0 oznacza identyczne przyrownanie
		//E_VALUE = K * M * N * exp(-Lambda * SN);
		//E_VALUE = M * N * pow(2.0, SN);
		E_VALUE = K * N * exp(-Lambda * S);

		return E_VALUE;
	}

	double BLAST::pValueEval(double e_value)
	{
		return (1.0 - exp(e_value));
	}

	Alignments BLAST::run(unsigned int how_much)
	{
		if(search() == false)
			return Alignments();

		if(estimate() == false)
			return Alignments();

		if(extend() == false)
			return Alignments();

		if(evaluate() == false)
			return Alignments();

		return getAligns(how_much);
	}

	void BLAST::printWords()
	{
		std::cout << std::endl << "\t\tTABLICA WORDS" << std::endl << std::endl;
		for(Words::iterator w = words_.begin(); w != words_.end(); ++w)
		{
			std::cout << (*w).getID() << "\t-->\t" << getWordSequence((*w)) << "\t-->\t" << (*w).getCount() << "\t-->\t" << (*w).getRate() << "\tAligns: " << (*w).getAlignCount() << std::endl;
			Alignments alignments = (*w).getAligns();
			for(Alignments::iterator align = alignments.begin(); align != alignments.end(); ++align)
			{
				std::cout << "\tSEQ ID = " << (*align).getSequenceId() << "\t-->\t" << (*align).getSeqStart() << "\t-->\t" << (*align).getSeqEnd() << std::endl;
			}
		}
		std::cout << std::endl << std::endl;
	}

	void BLAST::printAligns(unsigned int how_much)
	{
		printAlignsFrom(getAligns(how_much));
	}

	void BLAST::printAlignsFrom(Alignments aligns)
	{
		std::cout << getAlignString(aligns) << std::endl;
	}

	Alignments BLAST::getAligns(unsigned int how_much)
	{
		Alignments aligns;

		for(Words::iterator w = words_.begin(); w != words_.end(); ++w)
		{
			Alignments alignments = (*w).getAligns();
			for(Alignments::iterator align = alignments.begin(); align != alignments.end(); ++align)
			{
				// Wyrzucamy duplikaty
				if(find(aligns.begin(), aligns.end(), (*align)) == aligns.end())
					aligns.push_back(*align);
			}
		}

		std::sort(aligns.begin(), aligns.end(), std::greater<Alignment>());

		if(how_much != 0 && how_much < aligns.size())	// Zwracamy tylko czesc - pierwsze how_much najlepszych wynikow wg score
		{
			return Alignments(&aligns[0], &aligns[how_much]);
		}

		return aligns;
	}

	Alignment BLAST::getBestAlign()
	{
		return getAligns(1).front();
	}

	std::string BLAST::getAlignString(Alignments aligns)
	{
		std::string align_str = "";

		for(Alignments::iterator align = aligns.begin(); align != aligns.end(); ++align)
		{
			std::string score_str = boost::lexical_cast<std::string>((*align).getScore());
			std::string seq_id_str = boost::lexical_cast<std::string>((*align).getSequenceId());
			std::string len_str = boost::lexical_cast<std::string>((*align).getAlignLength());
			std::string percent_same = boost::lexical_cast<std::string>(((double)(*align).getSame() / (double)(*align).getAlignLength()) * 100);
			std::string percent_gaps = boost::lexical_cast<std::string>(((double)(*align).getGaps() / (double)(*align).getAlignLength()) * 100);
			std::string sub_pattern = getSubPattern((*align).getPatStart(), (*align).getPatEnd());
			std::string sub_sequence = getSubSequence((*align).getSequenceId(), (*align).getSeqStart(), (*align).getSeqEnd());
			//double e_value = evaluateOne(*align);
			//std::string e_value_str = boost::lexical_cast<std::string>(e_value);
			//std::string p_value_str = boost::lexical_cast<std::string>(pValueEval(e_value));

			std::string pat_start_str = boost::lexical_cast<std::string>((*align).getPatStart());
			std::string pat_end_str = boost::lexical_cast<std::string>((*align).getPatEnd());
			std::string seq_start_str = boost::lexical_cast<std::string>((*align).getSeqStart());
			std::string seq_end_str = boost::lexical_cast<std::string>((*align).getSeqEnd());

			align_str += ("P:\t" + pat_start_str + "\t" + sub_pattern + "\t" + pat_end_str + "\n");
			align_str += ("\t\t" + getAlignMark(sub_pattern, sub_sequence) + "\n");
			align_str += ("S:\t" + seq_start_str + "\t" + sub_sequence + "\t" + seq_end_str + "\n");
			align_str += ("\tSequence ID: " + seq_id_str + "\n");
			align_str += ("\tIdentity: " + percent_same + "%\n");
			align_str += ("\tGaps: " + percent_gaps + "%\n");
			align_str += ("\tScore: " + score_str + "\n");
			//align_str += ("\tE-value: " + e_value_str + "\n");
			//align_str += ("\tP-value: " + p_value_str + "\n");
			align_str += ("\tAlignment length: " + len_str + "\n\n");
			align_str += "------------------------------------------------------------\n\n";
		}

		return align_str;
	}

	double BLAST::getMinRate()
	{
		return min_rate_;
	}

	double BLAST::getMaxRate()
	{
		return max_rate_;
	}

	double BLAST::getAvgRate()
	{
		return avg_rate_;
	}

	std::string BLAST::getSubPattern(int pos_start, int pos_end)
	{
		return  pattern_.substr(pos_start, pos_end - pos_start + 1);
	}

	std::string BLAST::getSubSequence(std::string seq_id, int pos_start, int pos_end)
	{
		std::string sequence = (*(sequences_.find(seq_id))).second;
		return  sequence.substr(pos_start, pos_end - pos_start + 1);
	}

	std::string BLAST::getSequence(std::string seq_id)
	{
		return (*(sequences_.find(seq_id))).second;
	}

	std::string BLAST::getWordSequence(Word word)
	{
		return getSubPattern(word.getPatStart(), word.getPatEnd());
	}

	bool BLAST::charEqual(std::string sequence, int pattern_pos, int sequence_pos)
	{
		return (sequence.compare(sequence_pos, 1, pattern_, pattern_pos, 1) == 0);
	}

	std::string BLAST::getAlignMark(std::string pattern, std::string sequence)
	{
		std::string mark = "";
		std::string::iterator patt_it = pattern.begin();
		std::string::iterator seq_it = sequence.begin();

		for( ; patt_it != pattern.end(); ++patt_it, ++seq_it)
		{
			if((*patt_it) == (*seq_it))
				mark.append("|");
			else
				mark.append(" ");
		}

		return mark;
	}

	int BLAST::getAlignsSumInWords()
	{
		int sum = 0;

		for(Words::iterator w = words_.begin(); w != words_.end(); ++w)
		{
			sum += (*w).getAlignCount();
		}

		return sum;
	}
}
