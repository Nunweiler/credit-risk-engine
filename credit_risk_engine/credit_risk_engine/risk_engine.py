from datetime import date

from .models import AvaliacaoRisco
from .repositories import (
    ClienteRepository,
    RendaRepository,
    DividaRepository,
    AvaliacaoRiscoRepository,
)


class RiskEngine:
    """Motor simples de análise de risco de crédito.

    A lógica aqui é propositalmente simples e baseada em regras
    para fins didáticos.
    """

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

    def avaliar_cliente(self, cliente_id: int) -> AvaliacaoRisco:
        cliente = self._clientes.obter_por_id(cliente_id)
        if not cliente:
            raise ValueError(f'Cliente {cliente_id} não encontrado')

        renda_atual = self._rendas.obter_renda_atual(cliente_id)
        if not renda_atual or renda_atual.renda_mensal <= 0:
            renda_mensal = 0.0
        else:
            renda_mensal = renda_atual.renda_mensal

        dividas = self._dividas.listar_por_cliente(cliente_id)
        total_dividas = sum(d.valor for d in dividas)
        total_atraso = sum(d.valor for d in dividas if d.em_atraso)
        qtd_dividas = len(dividas)

        if renda_mensal > 0:
            indice_endividamento = total_dividas / renda_mensal
        else:
            indice_endividamento = float('inf') if total_dividas > 0 else 0.0

        score = 1000.0
        score -= indice_endividamento * 300
        score -= qtd_dividas * 20
        score -= (total_atraso / renda_mensal) * 200 if renda_mensal > 0 else 0

        score = max(0.0, min(score, 1000.0))

        if score >= 800:
            categoria = 'baixo'
        elif score >= 600:
            categoria = 'moderado'
        else:
            categoria = 'alto'

        detalhes = (
            f'Total dívidas: {total_dividas:.2f}, '
            f'Índice endividamento: {indice_endividamento:.2f}, '
            f'Dívidas em atraso: {total_atraso:.2f}'
        )

        avaliacao = AvaliacaoRisco(
            cliente_id=cliente_id,
            score=score,
            categoria=categoria,
            endividamento=indice_endividamento,
            renda_mensal=renda_mensal,
            data_avaliacao=date.today(),
            detalhes=detalhes,
        )

        self._avaliacoes.registrar(avaliacao)
        return avaliacao