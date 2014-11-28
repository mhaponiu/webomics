#include <iostream>
#include <string>
#include <vector>
#include <stdio.h>
#include <stdlib.h>

#include <boost/python.hpp>

#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>

using namespace boost::python;

// cl /EHsc /MD /D "WIN32" /D "_WIN32_WINNT#0x501" /D "_CONSOLE" /D "CALC_EXPORTS" /D "_USRDLL" /D "_WINDLL" /D "_WINDOWS" /IE:\Python27\include /IE:\boost\boost_1_51 MemoryTest.cpp /link /dll /LIBPATH:E:\Python27\libs /LIBPATH:E:\boost\boost_1_51\lib /OUT:build\memo.pyd

void matrix(std::string text, std::string pattern)
{
	std::cout << "Rozpoczynam badanie boost::numeric::ublas::matrix<short int>..." << std::endl;

	typedef boost::numeric::ublas::matrix<short int> Matrix;

	Matrix matrix(text.length(), pattern.length());

	// Wype³nienie macierzy
	for(long i = 0; i < matrix.size1(); ++ i)		// Po wierszach
	{
		for(long j = 0; j < matrix.size2(); ++ j) 	// Po kolumnach
		{
			matrix(i, j) = (short int)5;
		}
	}

	std::cout << "Zakonczylem badanie boost::numeric::ublas::matrix<short int>." << std::endl;
}

void vectors(std::string text, std::string pattern)
{
	std::cout << "Rozpoczynam badanie std::vector<std::vector<short int> >..." << std::endl;

	typedef std::vector<short int> Row;
	typedef std::vector<Row> Matrix;

	Matrix matrix;

	// Wype³nienie macierzy
	for(long i = 0; i < text.length(); ++i)
	{
		Row row;

		for(long j = 0; j < pattern.length(); ++j)	// Tworzymy wiersz
		{
			row.push_back((short int)5);
		}

		// Dodajemy wiersz do macierzy
		matrix.push_back(row);
	}

	std::cout << "Zakonczylem badanie std::vector<std::vector<short int> >." << std::endl;
}

void heap(std::string text, std::string pattern)
{
	long int size = text.length();
	long int size2 = pattern.length();

	std::cout << "Rozpoczynam badanie malloc (short int)..." << std::endl;

	short int ** matrix;

	matrix = (short int **)malloc(size2 * sizeof(short int*));
	for(int j = 0; j < size2; ++j)
		matrix[j] = (short int*)malloc(size * sizeof(short int));

	std::cout << "Zakonczylem badanie malloc (short int)." << std::endl;
}

void liveMatrix(std::string text, std::string pattern)
{
	std::cout << "Rozpoczynam badanie boost::numeric::ublas::matrix<short int>..." << std::endl;

	typedef boost::numeric::ublas::matrix<short int> Matrix;

	Matrix matrix(text.length(), pattern.length());

	// Wype³nienie macierzy
	for(long i = 0; i < matrix.size1(); ++ i)		// Po wierszach
	{
		for(long j = 0; j < matrix.size2(); ++ j) 	// Po kolumnach
		{
			matrix(i, j) = (short int)5;
		}
	}

	std::cout << "Zakonczylem badanie boost::numeric::ublas::matrix<short int>." << std::endl;
}

BOOST_PYTHON_MODULE(memo)
{
	def("matrix", matrix);
	def("vectors", vectors);
	def("heap", heap);
	def("liveMatrix", liveMatrix);
}
