#define BOOST_TEST_MODULE boosttest
#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MAIN
#include <boost/test/unit_test.hpp>
#include "../CellSW.hpp"
#include "../SW.hpp"

using namespace std;

BOOST_AUTO_TEST_SUITE (swTests)

/**
* Test dla klasy CellSW
*/
BOOST_AUTO_TEST_CASE (cellSwTest)
{
	BOOST_TEST_MESSAGE( "Testing CellSW class..." );

	algorithms::CellSW cell(10, 20, 50);

	BOOST_CHECK( !cell.getGap() );
	BOOST_CHECK_EQUAL( cell.getI(), 10 );
	BOOST_CHECK_EQUAL( cell.getJ(), 20 );
	BOOST_CHECK_EQUAL( cell.getValue(), 50 );

	cell.setGap(true);
	cell.setI(5);
	cell.setJ(30);
	cell.setValue(100);

	BOOST_CHECK( cell.getGap() );
	BOOST_CHECK_EQUAL( cell.getI(), 5 );
	BOOST_CHECK_EQUAL( cell.getJ(), 30 );
	BOOST_CHECK_EQUAL( cell.getValue(), 100 );
}

/**
* Test dla klasy SW
*/
BOOST_AUTO_TEST_CASE (swTest)
{
	BOOST_TEST_MESSAGE( "Testing SW class..." );

	algorithms::SW * sw = new algorithms::SW(2, -1, -3, -1);
	sw->compute("AAAB", "AABAB");

	algorithms::RouteVector rvector = sw->backtrack(sw->getSimilarity());

	BOOST_CHECK_EQUAL(rvector.size(), 3);

	algorithms::RouteVector::iterator it = rvector.begin();
	BOOST_CHECK_EQUAL(std::get<0>(*it), 1);
	BOOST_CHECK_EQUAL(std::get<1>(*it), 0);
	++it;
	BOOST_CHECK_EQUAL(std::get<0>(*it), 2);
	BOOST_CHECK_EQUAL(std::get<1>(*it), 1);
	++it;
	BOOST_CHECK_EQUAL(std::get<0>(*it), 3);
	BOOST_CHECK_EQUAL(std::get<1>(*it), 2);

	algorithms::StringTuple new_texts = sw->getSimilarityStrings(sw->getSimilarity(), rvector);
	BOOST_CHECK_EQUAL(std::get<0>(new_texts), "AAB");
	BOOST_CHECK_EQUAL(std::get<1>(new_texts), "AAB");

	algorithms::SW * sw2 = new algorithms::SW(2, -1, -3, -1);
	int value = sw2->computeFast("AAAB", "AABAB");
	BOOST_CHECK_EQUAL(value, 6);

	BOOST_CHECK_EQUAL(sw2->getMatch(), 2);
	BOOST_CHECK_EQUAL(sw2->getMismatch(), -1);
	BOOST_CHECK_EQUAL(sw2->getOpen(), -3);
	BOOST_CHECK_EQUAL(sw2->getExtend(), -1);

	sw2->setMatch(3);
	sw2->setMismatch(-2);
	sw2->setOpen(-5);
	sw2->setExtend(-2);

	BOOST_CHECK_EQUAL(sw2->getMatch(), 3);
	BOOST_CHECK_EQUAL(sw2->getMismatch(), -2);
	BOOST_CHECK_EQUAL(sw2->getOpen(), -5);
	BOOST_CHECK_EQUAL(sw2->getExtend(), -2);
}

BOOST_AUTO_TEST_SUITE_END( )
