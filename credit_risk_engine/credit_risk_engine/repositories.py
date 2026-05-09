from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Dict, List, Optional

from .models import Cliente, Renda, Divida, AvaliacaoRisco


class ClienteRepository:
    """Repositório em memória para clientes.

    Em um cenário real, isso seria substituído por acesso a banco de dados.
    """

    def __init__(self) -> None:
        self._clientes: Dict[int, Cliente] = {}
        self._proximo_id: int = 1

    def adicionar(self, cliente: Cliente) -> Cliente:
        if cliente.id == 0:
            cliente.id = self._proximo_id
            self._proximo_id += 1
        self._clientes[cliente.id] = cliente
        return cliente

    def obter_por_id(self, cliente_id: int) -> Optional[Cliente]:
        return self._clientes.get(cliente_id)

    def listar(self) -> List[Cliente]:
        return list(self._clientes.values())


class RendaRepository:
    def __init__(self) -> None:
        self._rendas: List[Renda] = []

    def registrar(self, renda: Renda) -> None:
        self._rendas.append(renda)

    def obter_renda_atual(self, cliente_id: int) -> Optional[Renda]:
        rendas_cliente = [r for r in self._rendas if r.cliente_id == cliente_id]
        if not rendas_cliente:
            return None
        rendas_cliente.sort(key=lambda r: r.data_registro)
        return rendas_cliente[-1]

    def listar_por_cliente(self, cliente_id: int) -> List[Renda]:
        return [r for r in self._rendas if r.cliente_id == cliente_id]


class DividaRepository:
    def __init__(self) -> None:
        self._dividas: Dict[int, Divida] = {}
        self._por_cliente: Dict[int, List[int]] = defaultdict(list)
        self._proximo_id: int = 1

    def registrar(self, divida: Divida) -> Divida:
        if divida.id == 0:
            divida.id = self._proximo_id
            self._proximo_id += 1
        self._dividas[divida.id] = divida
        self._por_cliente[divida.cliente_id].append(divida.id)
        return divida

    def listar_por_cliente(self, cliente_id: int) -> List[Divida]:
        ids = self._por_cliente.get(cliente_id, [])
        return [self._dividas[i] for i in ids]


class AvaliacaoRiscoRepository:
    def __init__(self) -> None:
        self._avaliacoes: Dict[int, List[AvaliacaoRisco]] = defaultdict(list)

    def registrar(self, avaliacao: AvaliacaoRisco) -> None:
        self._avaliacoes[avaliacao.cliente_id].append(avaliacao)

    def listar_por_cliente(self, cliente_id: int) -> List[AvaliacaoRisco]:
        return list(self._avaliacoes.get(cliente_id, []))

    def obter_ultima(self, cliente_id: int) -> Optional[AvaliacaoRisco]:
        historico = self._avaliacoes.get(cliente_id, [])
        if not historico:
            return None
        historico.sort(key=lambda a: a.data_avaliacao)
        return historico[-1]