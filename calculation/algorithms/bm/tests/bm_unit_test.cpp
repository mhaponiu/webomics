#define BOOST_TEST_MODULE boosttest
#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MAIN
#include <boost/test/unit_test.hpp>
#include "../BM.hpp"

using namespace std;

BOOST_AUTO_TEST_SUITE (bmTests)

/**
* Test dla klasy BM
*/
BOOST_AUTO_TEST_CASE (bmTest)
{
	BOOST_TEST_MESSAGE( "Testing BM class..." );

	std::string text = "BABABAABBBBBBBBBBBAAAAABAABAAAABBBBBBABAABABBBABABABBAABABBAAAAAABAAABBABBABBBBA";
	std::string pattern = "BBABA";

	algorithms::BM * bm = new algorithms::BM();

	BOOST_CHECK_EQUAL( bm->compute(text).size(), 0 );

	bm->prepare(pattern);
	algorithms::Positions positions = bm->compute(text);
	BOOST_CHECK_EQUAL( positions.size(), 2 );

	BOOST_CHECK_EQUAL( positions[0], 36 );
	BOOST_CHECK_EQUAL( positions[1], 45 );
}

BOOST_AUTO_TEST_SUITE_END( )
