#include "CellSW.hpp"

namespace algorithms
{
	CellSW::CellSW()
	{
		i_ = 0;
		j_ = 0;
		value_ = 0;
		gap_ = false;
	}

	CellSW::CellSW(long int i, long int j, int value)
	{
		i_ = i;
		j_ = j;
		value_ = value;
		gap_ = false;
	}

	long int CellSW::getI()
	{
		return i_;
	}

	void CellSW::setI(long int i)
	{
		i_ = i;
	}

	long int CellSW::getJ()
	{
		return j_;
	}

	void CellSW::setJ(long int j)
	{
		j_ = j;
	}

	int CellSW::getValue()
	{
		return value_;
	}

	void CellSW::setValue(int value)
	{
		value_ = value;
	}

	bool CellSW::getGap()
	{
		return gap_;
	}

	void CellSW::setGap(bool gap)
	{
		gap_ = gap;
	}
}


