/**
 * @file: Alignment.cpp
 *
 * @author: Piotr Roz, Pawel Zielinski
 *
 * @date: 28.12.2012
 *
 * @description: Plik zawierajacy definicje klasy Alignment przechowujacej informacje o procesie przyrownywania dwoch sekwencji
 */

#include "Alignment.hpp"

namespace algorithms
{
	Alignment::Alignment(std::string seq_id, int seq_start, int seq_end, int pat_start, int pat_end)
	{
		sequence_id_ = seq_id;
		seq_start_ = seq_start;
		seq_end_ = seq_end;
		pat_start_ = pat_start;
		pat_end_ = pat_end;

		drop_off_ = 0;
		gaps_ = 0;
		score_ = pat_end_ - pat_start_ + 1;
		same_ = score_;
	}

	int Alignment::getDropOff()
	{
		return drop_off_;
	}

	void Alignment::setDropOff(int dropOff)
	{
		drop_off_ = dropOff;
	}

	int Alignment::incDropOff()
	{
		return ++drop_off_;
	}

	int Alignment::decDropOff()
	{
		if(drop_off_ > 0)
			--drop_off_;
		return drop_off_;
	}

	int Alignment::getScore()
	{
		return score_;
	}

	void Alignment::setScore(int score)
	{
		score_ = score;
	}

	int Alignment::incScore()
	{
		return ++score_;
	}

	int Alignment::decScore()
	{
		return --score_;
	}

	int Alignment::getSame()
	{
		return same_;
	}

	void Alignment::setSame(int same)
	{
		same_ = same;
	}

	int Alignment::incSame()
	{
		return ++same_;
	}

	int Alignment::getGaps()
	{
		return gaps_;
	}

	void Alignment::setGaps(int gaps)
	{
		gaps_ = gaps;
	}

	int Alignment::incGaps()
	{
		return ++gaps_;
	}

	int Alignment::getSeqEnd()
	{
		return seq_end_;
	}

	void Alignment::setSeqEnd(int seqEnd)
	{
		seq_end_ = seqEnd;
	}

	int Alignment::incSeqEnd()
	{
		return ++seq_end_;
	}

	int Alignment::getSeqStart()
	{
		return seq_start_;
	}

	void Alignment::setSeqStart(int seqStart)
	{
		seq_start_ = seqStart;
	}

	int Alignment::decSeqStart()
	{
		return --seq_start_;
	}

	int Alignment::getPatEnd()
	{
		return pat_end_;
	}

	void Alignment::setPatEnd(int patEnd)
	{
		pat_end_ = patEnd;
	}

	int Alignment::incPatEnd()
	{
		return ++pat_end_;
	}

	int Alignment::getPatStart()
	{
		return pat_start_;
	}

	int Alignment::decPatStart()
	{
		return --pat_start_;
	}

	void Alignment::setPatStart(int patStart)
	{
		pat_start_ = patStart;
	}

	std::string Alignment::getSequenceId()
	{
		return sequence_id_;
	}

	void Alignment::setSequenceId(std::string sequenceId)
	{
		sequence_id_ = sequenceId;
	}

	int Alignment::getAlignLength()
	{
		return (pat_end_ - pat_start_ + 1);
	}

	bool Alignment::operator<(const Alignment & a) const
	{
		return score_ < a.score_;
	}

	bool Alignment::operator>(const Alignment & a) const
	{
		return score_ > a.score_;
	}

	bool Alignment::operator==(const Alignment & a) const
	{
		return (sequence_id_ == a.sequence_id_ && seq_start_ == a.seq_start_ && seq_end_ == a.seq_end_ && pat_start_ == a.pat_start_ && pat_end_ == a.pat_end_);
	}
}
