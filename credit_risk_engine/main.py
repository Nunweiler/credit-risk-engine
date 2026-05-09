from datetime import date

from credit_risk_engine.repositories import (
    ClienteRepository,
    RendaRepository,
    DividaRepository,
    AvaliacaoRiscoRepository,
)
from credit_risk_engine.risk_engine import RiskEngine
from credit_risk_engine.services import (
    ClienteService,
    RendaService,
    DividaService,
    HistoricoClienteService,
    RiskService,
)


def exemplo_uso() -> None:
    clientes_repo = ClienteRepository()
    rendas_repo = RendaRepository()
    dividas_repo = DividaRepository()
    avaliacoes_repo = AvaliacaoRiscoRepository()

    risk_engine = RiskEngine(
        clientes=clientes_repo,
        rendas=rendas_repo,
        dividas=dividas_repo,
        avaliacoes=avaliacoes_repo,
    )

    cliente_service = ClienteService(clientes_repo)
    renda_service = RendaService(rendas_repo)
    divida_service = DividaService(dividas_repo)
    historico_service = HistoricoClienteService(
        clientes=clientes_repo,
        rendas=rendas_repo,
        dividas=dividas_repo,
        avaliacoes=avaliacoes_repo,
    )
    risk_service = RiskService(risk_engine)

    cliente = cliente_service.cadastrar_cliente(
        nome='João da Silva',
        cpf='123.456.789-00',
        data_nascimento=date(1990, 1, 1),
    )

    renda_service.registrar_renda(
        cliente_id=cliente.id,
        renda_mensal=5000.0,
        fonte='CLT',
    )

    divida_service.registrar_divida(
        cliente_id=cliente.id,
        valor=1000.0,
        descricao='Cartão de crédito',
        data_contratacao=date(2024, 1, 10),
        em_atraso=False,
    )

    divida_service.registrar_divida(
        cliente_id=cliente.id,
        valor=2000.0,
        descricao='Empréstimo pessoal',
        data_contratacao=date(2023, 6, 5),
        em_atraso=True,
    )

    avaliacao = risk_service.consultar_risco(cliente.id)

    print('Avaliação de risco:')
    print(f'Cliente: {cliente.nome}')
    print(f'Score: {avaliacao.score:.2f}')
    print(f'Categoria: {avaliacao.categoria}')
    print(f'Detalhes: {avaliacao.detalhes}')

    historico = historico_service.obter_historico(cliente.id)
    print('\nHistórico do cliente:')
    print(historico)


if __name__ == '__main__':
    exemplo_uso()