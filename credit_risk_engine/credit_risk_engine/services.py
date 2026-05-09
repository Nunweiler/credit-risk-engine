from typing import Dict, Any, Optional, List

from .models import Cliente, Renda, Divida
from .repositories import (
    ClienteRepository,
    RendaRepository,
    DividaRepository,
    AvaliacaoRiscoRepository,
)
from .risk_engine import RiskEngine


class ClienteService:
    def __init__(self, repo: ClienteRepository) -> None:
        self._repo = repo

    def cadastrar_cliente(self, nome: str, cpf: str, data_nascimento) -> Cliente:
        cliente = Cliente(id=0, nome=nome, cpf=cpf, data_nascimento=data_nascimento)
        return self._repo.adicionar(cliente)

    def obter_cliente(self, cliente_id: int) -> Optional[Cliente]:
        return self._repo.obter_por_id(cliente_id)

    def listar_clientes(self) -> List[Cliente]:
        return self._repo.listar()


class RendaService:
    def __init__(self, repo: RendaRepository) -> None:
        self._repo = repo

    def registrar_renda(self, cliente_id: int, renda_mensal: float, fonte: str = 'não informado') -> None:
        renda = Renda(cliente_id=cliente_id, renda_mensal=renda_mensal, fonte=fonte)
        self._repo.registrar(renda)


class DividaService:
    def __init__(self, repo: DividaRepository) -> None:
        self._repo = repo

    def registrar_divida(
        self,
        cliente_id: int,
        valor: float,
        descricao: str,
        data_contratacao,
        em_atraso: bool = False,
    ) -> Divida:
        divida = Divida(
            id=0,
            cliente_id=cliente_id,
            valor=valor,
            descricao=descricao,
            data_contratacao=data_contratacao,
            em_atraso=em_atraso,
        )
        return self._repo.registrar(divida)


class HistoricoClienteService:
    def __init__(
        self,
        clientes: ClienteRepository,
        rendas: RendaRepository,
        dividas: DividaRepository,
        avaliacoes: AvaliacaoRiscoRepository,
    ) -> None:
        self._clientes = clientes
        self._rendas = rendas
        self._dividas = dividas
        self._avaliacoes = avaliacoes

    def obter_historico(self, cliente_id: int) -> Dict[str, Any]:
        cliente = self._clientes.obter_por_id(cliente_id)
        if not cliente:
            raise ValueError('Cliente não encontrado')

        rendas = self._rendas.listar_por_cliente(cliente_id)
        dividas = self._dividas.listar_por_cliente(cliente_id)
        avaliacoes = self._avaliacoes.listar_por_cliente(cliente_id)

        return {
            'cliente': cliente,
            'rendas': rendas,
            'dividas': dividas,
            'avaliacoes_risco': avaliacoes,
        }


class RiskService:
    def __init__(self, engine: RiskEngine) -> None:
        self._engine = engine

    def consultar_risco(self, cliente_id: int):
        return self._engine.avaliar_cliente(cliente_id)