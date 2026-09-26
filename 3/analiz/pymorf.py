# работа морфологического процессора pymorphy
from  pymorphy3  import  MorphAnalyzer
pm2= MorphAnalyzer()
pm2.parse('стекло')  # полный разбор
spis=pm2.parse('стекло')# запомнить в spis
print ( len(spis))
print(*spis, sep='\n', end='\n\n')
print('----------------------------')
pp=  spis[2].lexeme
print(len(pp))


