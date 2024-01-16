from Parser.ParsingTable import ParsingTable
from Parser.grammarHash import grammarHash


pTable=ParsingTable(grammarHash)
pTable.constructParseTable()
pTable.printTable()