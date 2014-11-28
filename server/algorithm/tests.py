from django.test import TestCase

# Biblioteka obliczeniowa
import calc

class AlgorithmsTest(TestCase):
    def test_kmp(self):
        text = "BABABAABBBBBBBBBBBAAAAABAABAAAABBBBBBABAABABBBABABABBAABABBAAAAAABAAABBABBABBBBA"
        pattern = "BBABA"
        
        kmp = calc.KMP()
        
        positions = kmp.computeFast(pattern, text)
        self.assertEqual(len(positions), 2)
        self.assertEqual(positions[0], 36)
        self.assertEqual(positions[1], 45)
        
    def test_bm(self):
        text = "BABABAABBBBBBBBBBBAAAAABAABAAAABBBBBBABAABABBBABABABBAABABBAAAAAABAAABBABBABBBBA"
        pattern = "BBABA"
        
        bm = calc.BM()
        
        positions = bm.computeFast(pattern, text)
        self.assertEqual(len(positions), 2)
        self.assertEqual(positions[0], 36)
        self.assertEqual(positions[1], 45)
        
    def test_sw(self):
        sw = calc.SW(2, -1, -3, -1)
        value = sw.compute("AAAB", "AABAB")
        self.assertEqual(value, 6)
        
        sw = calc.SW()
        value = sw.fastInitAndCompute(2, -1, -3, -1, "AAAB", "AABAB")
        self.assertEqual(value, 6)
        
        sw = calc.SW()
        value = sw.compute("AAAB", "AABAB")
        self.assertEqual(value, -1)
        
    def test_align(self):
        align = calc.Alignment("1234", 0, 10, 20, 30)
    
        self.assertEqual( align.getSeqStart(), 0 )
        self.assertEqual( align.getSeqEnd(), 10 )
        
        self.assertEqual( align.getPatStart(), 20 )
        self.assertEqual( align.getPatEnd(), 30 )
        
        self.assertEqual( align.getSequenceId(), "1234" )
        
        self.assertEqual( align.getDropOff(), 0 )
        self.assertEqual( align.getScore(), 11 )
        self.assertEqual( align.getSame(), 11 )
        self.assertEqual( align.getGaps(), 0 )
        
    def test_blast(self):
        blast = calc.Blast(11, 0.05, 5)
        result = blast.prepare("ACCGGUAGAGCAC")
        self.assertTrue( result )
        
        blast.addSequence("0", "GGCAUACCGGUAGAGCCAACGCAGUGUGAC")
        blast.addSequence("1", "AGACCGGUAGAGCACGGCACACCGGUAGAGCAC")
        blast.addSequence("2", "GACCGGUAGAGCACC")
        
        result = blast.search()
        self.assertTrue( result )
        
        result = blast.estimate()
        self.assertTrue( result )
    
        result = blast.extend()
        self.assertTrue( result )
        
        blast = calc.Blast(15, 0.05, 5)
        result = blast.prepare("ACCGGUAGAGCAC") # 13
        self.assertTrue( not result )
        
        blast = calc.Blast(11, 5.0, 5)
        result = blast.prepare("ACCGGUAGAGCAC") # 13
        self.assertTrue( result )
    
        result = blast.estimate()
        self.assertTrue( not result )
        