#define BOOST_TEST_MODULE boosttest
#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MAIN
#include <boost/test/unit_test.hpp>
#include "../KMP.hpp"

using namespace std;

BOOST_AUTO_TEST_SUITE (kmpTests)

/**
* Test dla klasy KMP
*/
BOOST_AUTO_TEST_CASE (kmpTest)
{
	BOOST_TEST_MESSAGE( "Testing KMP class..." );

	std::string text = "BABABAABBBBBBBBBBBAAAAABAABAAAABBBBBBABAABABBBABABABBAABABBAAAAAABAAABBABBABBBBA";
	std::string pattern = "BBABA";

	algorithms::KMP * kmp = new algorithms::KMP();

	BOOST_CHECK_EQUAL( kmp->compute(text).size(), 0 );

	int status = kmp->calculateTable(pattern);
	algorithms::Positions positions = kmp->compute(text);
	BOOST_CHECK_EQUAL( positions.size(), 2 );

	BOOST_CHECK_EQUAL( positions[0], 36 );
	BOOST_CHECK_EQUAL( positions[1], 45 );
}

BOOST_AUTO_TEST_SUITE_END( )
