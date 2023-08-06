from Excel_Trans.Excel_translator import Translator

trans = Translator()

trans.UzbekTranslate(file=r"test.xlsx", to_variant='cyrillic', save_file='test.xls')
