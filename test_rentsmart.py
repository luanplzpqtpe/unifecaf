import unittest
from decimal import Decimal
from tempfile import TemporaryDirectory
from pathlib import Path

from rentsmart import Apartamento, Casa, Contrato, Estudio, Orcamento


class TestRentSmart(unittest.TestCase):
    def test_apartamento_com_adicionais_e_desconto(self):
        self.assertEqual(Apartamento(2, True, False).calcular_aluguel(), Decimal("1140.00"))

    def test_casa_dois_quartos_com_garagem(self):
        self.assertEqual(Casa(2, True).calcular_aluguel(), Decimal("1450.00"))

    def test_estudio_com_quatro_vagas(self):
        self.assertEqual(Estudio(4).calcular_aluguel(), Decimal("1570.00"))

    def test_parcelamento(self):
        self.assertEqual(Contrato(3).valor_parcela, Decimal("666.67"))

    def test_csv_tem_doze_meses(self):
        with TemporaryDirectory() as pasta:
            arquivo = Orcamento("Teste", Casa(1, False), Contrato(2)).gerar_csv(Path(pasta) / "p.csv")
            self.assertEqual(len(arquivo.read_text(encoding="utf-8-sig").splitlines()), 13)


if __name__ == "__main__":
    unittest.main()
