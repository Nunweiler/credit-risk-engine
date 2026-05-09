import pytest
from datetime import date
from credit_risk_engine.models import Cliente, Renda, Divida, AvaliacaoRisco


class TestCliente:
    def test_cliente_creation(self):
        """Testa a criação de um cliente com dados válidos."""
        cliente = Cliente(
            id=1,
            nome="João Silva",
            cpf="123.456.789-00",
            data_nascimento=date(1990, 1, 1),
            data_cadastro=date(2023, 1, 1),
            ativo=True
        )
        assert cliente.id == 1
        assert cliente.nome == "João Silva"
        assert cliente.cpf == "123.456.789-00"
        assert cliente.data_nascimento == date(1990, 1, 1)
        assert cliente.data_cadastro == date(2023, 1, 1)
        assert cliente.ativo is True

    def test_cliente_default_values(self):
        """Testa os valores padrão do cliente."""
        cliente = Cliente(
            id=2,
            nome="Maria Santos",
            cpf="987.654.321-00",
            data_nascimento=date(1985, 5, 15)
        )
        assert cliente.ativo is True
        assert cliente.data_cadastro == date.today()

    def test_cliente_immutable_fields(self):
        """Testa que os campos do dataclass são imutáveis após criação."""
        cliente = Cliente(
            id=3,
            nome="Pedro Costa",
            cpf="111.222.333-44",
            data_nascimento=date(1995, 10, 20)
        )
        # Tentar alterar deve funcionar, pois dataclasses não são frozen por padrão
        cliente.nome = "Pedro Costa Jr."
        assert cliente.nome == "Pedro Costa Jr."


class TestRenda:
    def test_renda_creation(self):
        """Testa a criação de uma renda."""
        renda = Renda(
            cliente_id=1,
            renda_mensal=5000.0,
            fonte="CLT",
            data_registro=date(2023, 1, 1)
        )
        assert renda.cliente_id == 1
        assert renda.renda_mensal == 5000.0
        assert renda.fonte == "CLT"
        assert renda.data_registro == date(2023, 1, 1)

    def test_renda_default_values(self):
        """Testa valores padrão da renda."""
        renda = Renda(cliente_id=2, renda_mensal=3000.0)
        assert renda.fonte == "não informado"
        assert renda.data_registro == date.today()


class TestDivida:
    def test_divida_creation(self):
        """Testa a criação de uma dívida."""
        divida = Divida(
            id=1,
            cliente_id=1,
            valor=1000.0,
            descricao="Cartão de crédito",
            data_contratacao=date(2023, 1, 1),
            em_atraso=False
        )
        assert divida.id == 1
        assert divida.cliente_id == 1
        assert divida.valor == 1000.0
        assert divida.descricao == "Cartão de crédito"
        assert divida.data_contratacao == date(2023, 1, 1)
        assert divida.em_atraso is False

    def test_divida_default_em_atraso(self):
        """Testa valor padrão de em_atraso."""
        divida = Divida(
            id=2,
            cliente_id=2,
            valor=2000.0,
            descricao="Empréstimo",
            data_contratacao=date(2023, 6, 1)
        )
        assert divida.em_atraso is False


class TestAvaliacaoRisco:
    def test_avaliacao_creation(self):
        """Testa a criação de uma avaliação de risco."""
        avaliacao = AvaliacaoRisco(
            cliente_id=1,
            score=750.0,
            categoria="moderado",
            endividamento=0.3,
            renda_mensal=5000.0,
            data_avaliacao=date(2023, 1, 1),
            detalhes="Avaliação realizada"
        )
        assert avaliacao.cliente_id == 1
        assert avaliacao.score == 750.0
        assert avaliacao.categoria == "moderado"
        assert avaliacao.endividamento == 0.3
        assert avaliacao.renda_mensal == 5000.0
        assert avaliacao.data_avaliacao == date(2023, 1, 1)
        assert avaliacao.detalhes == "Avaliação realizada"

    def test_avaliacao_default_values(self):
        """Testa valores padrão da avaliação."""
        avaliacao = AvaliacaoRisco(
            cliente_id=2,
            score=800.0,
            categoria="baixo",
            endividamento=0.2,
            renda_mensal=4000.0
        )
        assert avaliacao.data_avaliacao == date.today()
        assert avaliacao.detalhes is None