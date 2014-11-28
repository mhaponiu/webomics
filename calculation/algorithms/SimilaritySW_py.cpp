#include "SimilaritySW_py.hpp"

namespace algorithms
{
	SimilaritySW_py::SimilaritySW_py()
	{
		this->value = 0;
		this->text_form = "";
		this->pattern_form = "";
	}

	SimilaritySW_py::SimilaritySW_py(int value, std::string text_form, std::string pattern_form, int position_i, int position_j)
	{
		this->value = value;
		this->text_form = text_form;
		this->pattern_form = pattern_form;
		this->position_i = position_i;
		this->position_j = position_j;
	}

	int SimilaritySW_py::getValue()
	{
		return this->value;
	}

	std::string SimilaritySW_py::getText()
	{
		return this->text_form;
	}

	std::string SimilaritySW_py::getPattern()
	{
		return this->pattern_form;
	}

	int SimilaritySW_py::getPositionI()
	{
		return this->position_i;
	}

	int SimilaritySW_py::getPositionJ()
	{
		return this->position_j;
	}
}
