/**
 * @file: Word.cpp
 *
 * @author: Piotr Roz, Pawel Zielinski
 *
 * @date: 28.12.2012
 *
 * @description: Plik zawierajacy definicje klasy Word przechowujacej informacje o fragmencie wzorca, z ktorym skojarzone sa obiekty
 * klasy Alignment - kolejne przyrownania
 */

#include "Word.hpp"

namespace algorithms
{
	Word::Word(int ID, int pat_start, int pat_end)
	{
		ID_ = ID;
		count_ = 0;
		rate_ = 0.0;

		pat_start_ = pat_start;
		pat_end_ = pat_end;
	}

	int Word::getID()
	{
		return ID_;
	}

	void Word::incCount()
	{
		++count_;
	}

	void Word::setCount(int count)
	{
		count_ = count;
	}

	int Word::getCount()
	{
		return count_;
	}

	void Word::setRate(double rate)
	{
		rate_ = rate;
	}

	double Word::getRate()
	{
		return rate_;
	}

	void Word::addAlign(std::string seq_id, int seq_start, int seq_end, int pat_start, int pat_end)
	{
		Alignment alignment(seq_id, seq_start, seq_end, pat_start, pat_end);
		aligns_.push_back(alignment);
	}

	Alignments Word::getAligns()
	{
		return aligns_;
	}

	void Word::setAligns(Alignments aligns)
	{
		aligns_ = aligns;
	}

	int Word::getPatEnd()
	{
		return pat_end_;
	}

	void Word::setPatEnd(int patEnd)
	{
		pat_end_ = patEnd;
	}

	int Word::incPatEnd()
	{
		return ++pat_end_;
	}

	int Word::getPatStart()
	{
		return pat_start_;
	}

	int Word::decPatStart()
	{
		return --pat_start_;
	}

	void Word::setPatStart(int patStart)
	{
		pat_start_ = patStart;
	}

	bool Word::findSeqID(std::string seq_id)
	{
		for(Alignments::iterator align = aligns_.begin(); align != aligns_.end(); ++align)
		{
			if((*align).getSequenceId() == seq_id)
				return true;
		}

		return false;
	}

	int Word::getAlignCount()
	{
		return (int)aligns_.size();
	}
}
