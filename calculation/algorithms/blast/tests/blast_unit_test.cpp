#define BOOST_TEST_MODULE boosttest
#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MAIN
#include <boost/test/unit_test.hpp>
#include "../Word.hpp"
#include "../Alignment.hpp"
#include "../Blast.hpp"

using namespace std;

BOOST_AUTO_TEST_SUITE (blastTests)

/**
* Test dla klasy Word
*/
BOOST_AUTO_TEST_CASE (wordTest)
{
	BOOST_TEST_MESSAGE( "Testing Word class..." );

	algorithms::Word word1(0, 0, 10);
	algorithms::Word word2(1, 20, 30);

	BOOST_CHECK_EQUAL( word1.getID(), 0 );
	BOOST_CHECK_EQUAL( word2.getID(), 1 );

	BOOST_CHECK_EQUAL( word1.getPatStart(), 0 );
	BOOST_CHECK_EQUAL( word2.getPatStart(), 20 );

	BOOST_CHECK_EQUAL( word1.getPatEnd(), 10 );
	BOOST_CHECK_EQUAL( word2.getPatEnd(), 30 );

	word1.setPatStart(5);
	word1.setPatEnd(15);

	BOOST_CHECK_EQUAL( word1.getPatStart(), 5 );
	BOOST_CHECK_EQUAL( word1.getPatEnd(), 15 );

	word2.decPatStart();
	word2.incPatEnd();

	BOOST_CHECK_EQUAL( word2.getPatStart(), 19 );
	BOOST_CHECK_EQUAL( word2.getPatEnd(), 31 );

	BOOST_CHECK_EQUAL( word1.getAlignCount(), 0 );
	word1.addAlign("1234", 10, 20, 30, 40);
	BOOST_CHECK_EQUAL( word1.getAlignCount(), 1 );
	algorithms::Alignments aligns = word1.getAligns();
	BOOST_CHECK_EQUAL( aligns.size(), word1.getAlignCount() );
	word1.setAligns(aligns);
	BOOST_CHECK_EQUAL( aligns.size(), word1.getAlignCount() );
	BOOST_CHECK_EQUAL( word1.findSeqID("1234"), true );
	BOOST_CHECK_EQUAL( word1.findSeqID("123"), false );

	word2.setRate(1.0);
	BOOST_CHECK_EQUAL( word2.getRate(), 1.0 );

	word2.setCount(5);
	BOOST_CHECK_EQUAL( word2.getCount(), 5 );
	word2.incCount();
	BOOST_CHECK_EQUAL( word2.getCount(), 6 );
}

/**
* Test dla klasy Alignment
*/
BOOST_AUTO_TEST_CASE (alignmentTest)
{
	BOOST_TEST_MESSAGE( "Testing Alignment class..." );

	algorithms::Alignment align1("1234", 0, 10, 20, 30);
	algorithms::Alignment align2("9999", 100, 110, 200, 300);

	BOOST_CHECK_EQUAL( align1.getSequenceId(), "1234" );
	BOOST_CHECK_EQUAL( align2.getSequenceId(), "9999" );
	align2.setSequenceId("1");
	BOOST_CHECK_EQUAL( align2.getSequenceId(), "1" );

	align1.setDropOff(2);
	BOOST_CHECK_EQUAL( align1.getDropOff(), 2 );
	align1.incDropOff();
	BOOST_CHECK_EQUAL( align1.getDropOff(), 3 );
	align1.decDropOff();
	BOOST_CHECK_EQUAL( align1.getDropOff(), 2 );

	align1.setScore(10);
	BOOST_CHECK_EQUAL( align1.getScore(), 10 );
	align1.incScore();
	BOOST_CHECK_EQUAL( align1.getScore(), 11 );
	align1.decScore();
	BOOST_CHECK_EQUAL( align1.getScore(), 10 );

	align1.setSame(5);
	BOOST_CHECK_EQUAL( align1.getSame(), 5 );
	align1.incSame();
	BOOST_CHECK_EQUAL( align1.getSame(), 6 );

	align1.setGaps(5);
	BOOST_CHECK_EQUAL( align1.getGaps(), 5 );
	align1.incGaps();
	BOOST_CHECK_EQUAL( align1.getGaps(), 6 );

	align1.setSeqEnd(15);
	BOOST_CHECK_EQUAL( align1.getSeqEnd(), 15 );
	align1.incSeqEnd();
	BOOST_CHECK_EQUAL( align1.getSeqEnd(), 16 );

	align1.setSeqStart(5);
	BOOST_CHECK_EQUAL( align1.getSeqStart(), 5 );
	align1.decSeqStart();
	BOOST_CHECK_EQUAL( align1.getSeqStart(), 4 );

	align1.setPatEnd(15);
	BOOST_CHECK_EQUAL( align1.getPatEnd(), 15 );
	align1.incPatEnd();
	BOOST_CHECK_EQUAL( align1.getPatEnd(), 16 );

	align1.setPatStart(5);
	BOOST_CHECK_EQUAL( align1.getPatStart(), 5 );
	align1.decPatStart();
	BOOST_CHECK_EQUAL( align1.getPatStart(), 4 );

	BOOST_CHECK_EQUAL( align1.getAlignLength(), 13 );
}

/**
* Test dla klasy Blast
*/
BOOST_AUTO_TEST_CASE (blastTest)
{
	BOOST_TEST_MESSAGE( "Testing Blast class..." );

	algorithms::BLAST blast(11, 0.05, 5);

	bool result;

	result = blast.prepare("ACCGGUAGAGCAC"); // 13
	BOOST_CHECK( result );

	blast.addSequence("0", "GGCAUACCGGUAGAGCCAACGCAGUGUGAC");
	blast.addSequence("1", "AGACCGGUAGAGCACGGCACACCGGUAGAGCAC");
	blast.addSequence("2", "GACCGGUAGAGCACC");

	result = blast.search();
	BOOST_CHECK( result );

	result = blast.estimate();
	BOOST_CHECK( result );

	result = blast.extend();
	BOOST_CHECK( result );

	algorithms::Alignment best_align = blast.getBestAlign();
	algorithms::Alignments aligns = blast.getAligns(0);
	std::string align_str = blast.getAlignString(aligns);

	algorithms::BLAST blast2(15, 0.05, 5);
	result = blast2.prepare("ACCGGUAGAGCAC"); // 13
	BOOST_CHECK( !result );


	algorithms::BLAST blast3(11, 5.0, 5);
	result = blast3.prepare("ACCGGUAGAGCAC"); // 13
	BOOST_CHECK( result );

	result = blast3.estimate();
	BOOST_CHECK( !result );
}


BOOST_AUTO_TEST_SUITE_END( )
