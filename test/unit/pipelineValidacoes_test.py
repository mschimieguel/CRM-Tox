import unittest
import sys 
import os
sys.path.append(os.path.abspath('..'))
import app.pipelineValidacoes as pipelineValidacoes

class TestPipelineValidacoes(unittest.TestCase):
        
    def test_pipelinevalidacoesVerdadeira(self):
        resultado,mensagem = pipelineValidacoes.Executar([(True,"Mensagem Erro")])
        self.assertTrue(resultado)   
        self.assertEqual(mensagem,"Sucess")

    def test_pipelinevalidacoesFalsa(self):
        resultado,mensagem = pipelineValidacoes.Executar([(False,"Mensagem Erro")])
        self.assertFalse(resultado)   
        self.assertEqual(mensagem,"Mensagem Erro") 
    
    def test_pipelinevalidacoesMultiplasValidacoes(self):
        resultado,mensagem = pipelineValidacoes.Executar(
            [
                (True,"Mensagem Erro1"),
                (False,"Mensagem Erro2"),
                (True,"Mensagem Erro3")

            ]
        )
        self.assertFalse(resultado)   
        self.assertEqual(mensagem,"Mensagem Erro2")
    
    def test_pipelinevalidacoesFalsa_MensagemIdefinida(self):
        mensagemIdefinida = None
        resultado,mensagem = pipelineValidacoes.Executar([(False,mensagemIdefinida)])
        self.assertFalse(resultado)   
        self.assertEqual(mensagem,mensagemIdefinida)
    
    def test_pipelinevalidacoesVazia(self):
        resultado,mensagem = pipelineValidacoes.Executar([])
        self.assertTrue(resultado)   
        self.assertEqual(mensagem,"Sucess")

    def test_pipelinevalidacoesNulla(self):
        with self.assertRaises(TypeError):
            pipelineValidacoes.Executar(None)
         

    def test_pipelinevalidacoes_ValidacaoNone(self):
        resultado,mensagem = pipelineValidacoes.Executar([(None,"Mensagem Erro")])
        self.assertFalse(resultado)   
        self.assertEqual(mensagem,"Mensagem Erro")

    def test_pipelinevalidacoes_ValidacaoOutrosValores(self):
        with self.assertRaises(TypeError):
            pipelineValidacoes.Executar(["outroValor"])

    def test_pipelinevalidacoes_ValidacaoMuitosValores(self):
        with self.assertRaises(TypeError):
            pipelineValidacoes.Executar([( "teste", "teste")])

if __name__ == '__main__':
    unittest.main()