#include "SW_py.hpp"

namespace algorithms
{
	SW_py::SW_py()
	{
		this->sw = NULL;
		this->similarity = NULL;
	}

	SW_py::SW_py(int w_match, int w_mismatch, int w_open, int w_extend)
	{
		this->sw = new SW(w_match, w_mismatch, w_open, w_extend);
		this->similarity = NULL;
	}

	SW_py::~SW_py()
	{
		if(this->similarity != NULL)
			delete this->similarity;
		if(this->sw != NULL)
			delete this->sw;
	}

	int SW_py::fastInitAndCompute(int w_match, int w_mismatch, int w_open, int w_extend, std::string text, std::string pattern)
	{
		this->sw = new SW(w_match, w_mismatch, w_open, w_extend);
		int max_value = this->sw->computeFast(text, pattern);
		delete this->sw;
		this->sw = NULL;
		return max_value;
	}

	int SW_py::compute(std::string text, std::string pattern)
	{
		if(this->sw == NULL)
			return -1;
		this->sw->compute(text, pattern);
		return this->sw->getSimilarity().getValue();
	}

	SimilaritySW_py SW_py::fastComputeWithStringsResult(int w_match, int w_mismatch, int w_open, int w_extend, std::string text, std::string pattern)
	{
		this->sw = new SW(w_match, w_mismatch, w_open, w_extend);
		this->sw->compute(text, pattern);
		SimilaritySW_py result = this->backtrack();
		delete this->sw;
		this->sw = NULL;
		return result;
	}

	SimilaritySW_py SW_py::backtrack()
	{
		//TODO: Zrobic to samo co wyzej ale ladniej ;)
		StringTuple forms = this->sw->getSimilarityStrings(this->sw->getSimilarity(), this->sw->backtrack(this->sw->getSimilarity()));

		int value = this->sw->getSimilarity().getValue();
		std::string text_form = std::get<0>(forms);
		std::string pattern_form = std::get<1>(forms);
		int position_i = this->sw->getSimilarity().getPoistionI();
		int position_j = this->sw->getSimilarity().getPositionJ();

		SimilaritySW_py similarity(value, text_form, pattern_form, position_i, position_j);
		this->similarity = &similarity;
		return similarity;
	}

	SimilaritySW_py SW_py::getSimilarity()
	{
		if(this->similarity == NULL)
			return this->backtrack();
		else
			return *this->similarity;
	}

	int SW_py::getMatch() const
	{
		return this->sw->getMatch();
	}

	void SW_py::setMatch(int match)
	{
		this->sw->setMatch(match);
	}

	int SW_py::getMismatch() const
	{
		return this->sw->getMismatch();
	}

	void SW_py::setMismatch(int mismatch)
	{
		this->sw->setMismatch(mismatch);
	}

	int SW_py::getGapOpen() const
	{
		return this->sw->getOpen();
	}

	void SW_py::setGapOpen(int open)
	{
		this->sw->setOpen(open);
	}

	int SW_py::getGapExtend() const
	{
		return this->sw->getExtend();
	}

	void SW_py::setGapExtend(int extend)
	{
		this->sw->setExtend(extend);
	}

	// Funkcje dla Python

	void SW_py::set_similarity(SimilaritySW_py similarity)
	{
		this->similarity = &similarity;
	}

	SimilaritySW_py SW_py::get_similarity() const
	{
		return *this->similarity;
	}
}
