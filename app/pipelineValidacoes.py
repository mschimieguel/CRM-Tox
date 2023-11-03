from typing import List, Tuple 

def Executar(validacoes: List[Tuple[bool,str]]) -> Tuple[bool,str]:
    if  not isinstance(validacoes,list):
        raise TypeError

    for validacao in validacoes:
        if  not (isinstance(validacao,tuple) and len(validacao) == 2 ):
            raise TypeError
        if  not (isinstance(validacao[0],bool) or validacao[0] is None ):
            raise TypeError
        if validacao[0] is not True:
            return validacao
    return True,"Sucess"
    