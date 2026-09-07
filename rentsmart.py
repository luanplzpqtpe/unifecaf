"""RentSmart - orcamentos de locacao com orientacao a objetos."""

from __future__ import annotations

import csv
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

MOEDA = Decimal("0.01")


def dinheiro(valor: Decimal) -> str:
    """Formata Decimal no padrao monetario brasileiro."""
    valor = valor.quantize(MOEDA, rounding=ROUND_HALF_UP)
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class Imovel(ABC):
    """Classe-base das categorias de imovel."""

    categoria = "Imovel"
    aluguel_base = Decimal("0")

    @abstractmethod
    def calcular_aluguel(self) -> Decimal:
        """Retorna o aluguel mensal final."""

    @abstractmethod
    def detalhamento(self) -> list[tuple[str, Decimal]]:
        """Retorna os componentes usados no calculo."""


@dataclass(frozen=True)
class Apartamento(Imovel):
    quartos: int
    possui_garagem: bool
    possui_criancas: bool
    categoria = "Apartamento"
    aluguel_base = Decimal("700")

    def __post_init__(self) -> None:
        if self.quartos not in (1, 2):
            raise ValueError("Apartamento deve possuir 1 ou 2 quartos.")

    def subtotal(self) -> Decimal:
        return self.aluguel_base + (Decimal("200") if self.quartos == 2 else 0) + (Decimal("300") if self.possui_garagem else 0)

    def desconto(self) -> Decimal:
        return self.subtotal() * Decimal("0.05") if not self.possui_criancas else Decimal("0")

    def calcular_aluguel(self) -> Decimal:
        return (self.subtotal() - self.desconto()).quantize(MOEDA)

    def detalhamento(self) -> list[tuple[str, Decimal]]:
        itens = [("Aluguel-base", self.aluguel_base)]
        if self.quartos == 2:
            itens.append(("Adicional de 2 quartos", Decimal("200")))
        if self.possui_garagem:
            itens.append(("Vaga de garagem", Decimal("300")))
        if self.desconto():
            itens.append(("Desconto sem criancas (5%)", -self.desconto()))
        return itens


@dataclass(frozen=True)
class Casa(Imovel):
    quartos: int
    possui_garagem: bool
    categoria = "Casa"
    aluguel_base = Decimal("900")

    def __post_init__(self) -> None:
        if self.quartos not in (1, 2):
            raise ValueError("Casa deve possuir 1 ou 2 quartos.")

    def calcular_aluguel(self) -> Decimal:
        valor = self.aluguel_base
        if self.quartos == 2:
            valor += Decimal("250")
        if self.possui_garagem:
            valor += Decimal("300")
        return valor.quantize(MOEDA)

    def detalhamento(self) -> list[tuple[str, Decimal]]:
        itens = [("Aluguel-base", self.aluguel_base)]
        if self.quartos == 2:
            itens.append(("Adicional de 2 quartos", Decimal("250")))
        if self.possui_garagem:
            itens.append(("Vaga de garagem", Decimal("300")))
        return itens


@dataclass(frozen=True)
class Estudio(Imovel):
    vagas: int
    categoria = "Estudio"
    aluguel_base = Decimal("1200")

    def __post_init__(self) -> None:
        if self.vagas == 1 or self.vagas < 0:
            raise ValueError("Informe 0 vaga ou o pacote minimo de 2 vagas.")

    def custo_estacionamento(self) -> Decimal:
        if self.vagas == 0:
            return Decimal("0")
        return Decimal("250") + Decimal("60") * (self.vagas - 2)

    def calcular_aluguel(self) -> Decimal:
        return (self.aluguel_base + self.custo_estacionamento()).quantize(MOEDA)

    def detalhamento(self) -> list[tuple[str, Decimal]]:
        itens = [("Aluguel-base", self.aluguel_base)]
        if self.vagas >= 2:
            itens.append(("Pacote inicial de 2 vagas", Decimal("250")))
        if self.vagas > 2:
            itens.append((f"{self.vagas - 2} vaga(s) adicional(is)", Decimal("60") * (self.vagas - 2)))
        return itens


@dataclass(frozen=True)
class Contrato:
    parcelas: int
    taxa: Decimal = Decimal("2000")

    def __post_init__(self) -> None:
        if not 1 <= self.parcelas <= 5:
            raise ValueError("A taxa contratual pode ser dividida de 1 a 5 parcelas.")

    @property
    def valor_parcela(self) -> Decimal:
        return (self.taxa / self.parcelas).quantize(MOEDA, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Orcamento:
    cliente: str
    imovel: Imovel
    contrato: Contrato

    def resumo(self) -> str:
        linhas = ["\n" + "=" * 58, "RENTSMART - RESUMO DO ORCAMENTO", "=" * 58]
        linhas += [f"Cliente: {self.cliente}", f"Categoria: {self.imovel.categoria}", "", "Composicao do aluguel:"]
        linhas += [f"  {descricao:<40} {dinheiro(valor):>14}" for descricao, valor in self.imovel.detalhamento()]
        linhas += ["-" * 58, f"ALUGUEL MENSAL: {dinheiro(self.imovel.calcular_aluguel())}", "", f"Taxa contratual: {dinheiro(self.contrato.taxa)}", f"Parcelamento: {self.contrato.parcelas}x de {dinheiro(self.contrato.valor_parcela)}", "=" * 58]
        return "\n".join(linhas)

    def gerar_csv(self, caminho: str | Path = "projecao_12_meses.csv") -> Path:
        caminho = Path(caminho)
        aluguel = self.imovel.calcular_aluguel()
        with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mes", "Aluguel", "Parcela da taxa contratual", "Total previsto"])
            for mes in range(1, 13):
                parcela = self.contrato.valor_parcela if mes <= self.contrato.parcelas else Decimal("0")
                escritor.writerow([mes, f"{aluguel:.2f}", f"{parcela:.2f}", f"{aluguel + parcela:.2f}"])
        return caminho


def perguntar_opcao(mensagem: str, opcoes: set[str]) -> str:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in opcoes:
            return resposta
        print(f"Opcao invalida. Escolha: {', '.join(sorted(opcoes))}.")


def perguntar_inteiro(mensagem: str, minimo: int, maximo: int | None = None) -> int:
    while True:
        try:
            valor = int(input(mensagem).strip())
            if valor < minimo or (maximo is not None and valor > maximo):
                raise ValueError
            return valor
        except ValueError:
            limite = f" entre {minimo} e {maximo}" if maximo is not None else f" maior ou igual a {minimo}"
            print(f"Digite um numero inteiro{limite}.")


def sim_nao(mensagem: str) -> bool:
    return perguntar_opcao(mensagem + " [s/n]: ", {"s", "n"}) == "s"


def criar_imovel() -> Imovel:
    categoria = perguntar_opcao("Categoria [apartamento/casa/estudio]: ", {"apartamento", "casa", "estudio"})
    if categoria == "apartamento":
        return Apartamento(perguntar_inteiro("Quartos [1/2]: ", 1, 2), sim_nao("Deseja garagem?"), sim_nao("O cliente possui criancas?"))
    if categoria == "casa":
        return Casa(perguntar_inteiro("Quartos [1/2]: ", 1, 2), sim_nao("Deseja garagem?"))
    while True:
        vagas = perguntar_inteiro("Vagas [0 ou minimo 2]: ", 0)
        if vagas != 1:
            return Estudio(vagas)
        print("Para estudio, informe 0 ou o pacote minimo de 2 vagas.")


def main() -> None:
    print("\nBem-vindo ao RentSmart")
    cliente = input("Nome do cliente: ").strip() or "Cliente nao informado"
    imovel = criar_imovel()
    parcelas = perguntar_inteiro("Parcelas da taxa contratual [1-5]: ", 1, 5)
    orcamento = Orcamento(cliente, imovel, Contrato(parcelas))
    print(orcamento.resumo())
    saida = orcamento.gerar_csv()
    print(f"Projecao criada com sucesso: {saida.resolve()}")


if __name__ == "__main__":
    main()
