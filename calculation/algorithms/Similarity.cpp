#include "Similarity.hpp"

namespace algorithms
{
	void Similarity::setValuesSW(int value, int position_i, int position_j)
	{
		this->value = value;
		this->position_i = position_i;
		this->position_j = position_j;
	}

	RatingsMatrix Similarity::getMatrix()
	{
		return this->matrix;
	}

	void Similarity::setMatrix(RatingsMatrix matrix)
	{
		this->matrix = matrix;
	}

	int Similarity::getValue()
	{
		return this->value;
	}

	std::string Similarity::getTextForm()
	{
		return this->text_form;
	}

	std::string Similarity::getPatternForm()
	{
		return this->pattern_form;
	}

	int Similarity::getPoistionI()
	{
		return this->position_i;
	}

	int Similarity::getPositionJ()
	{
		return this->position_j;
	}

	void Similarity::setPatternForm(std::string patternForm)
	{
		this->pattern_form = patternForm;
	}

	void Similarity::setPositionI(int positionI)
	{
		this->position_i = positionI;
	}

	void Similarity::setPositionJ(int positionJ)
	{
		this->position_j = positionJ;
	}

	void Similarity::setTextForm(std::string textForm)
	{
		this->text_form = textForm;
	}

	void Similarity::setValue(int value)
	{
		this->value = value;
	}
}
