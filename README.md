# Simple-HL7-parser
HL7 Simple Parser  Updated 2 minutes ago This is very simple parser for text in HL7 format. Code is written in functions. The final Function is hl7 (path, file=True) , which can be used either to parse a HL7 file, or in the case of file=False path should be given a hl7 text line. Lines should be clearly identified with header (one header per line) in input, since function reads in lines. It returns a dictionary with headers as keys, and list of entries as values. ('^~&amp;#') delimiters are used to parse the text within each pipe if presented.
