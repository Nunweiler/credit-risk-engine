import pytest
from datetime import date
from unittest.mock import Mock
from credit_risk_engine.models import Cliente
from credit_risk_engine.repositories import ClienteRepository
from credit_risk_engine.services import ClienteService


class TestClienteService:
    def test_cadastrar_cliente(self):
        """Testa o cadastro de um novo cliente."""
        repo_mock = Mock(spec=ClienteRepository)
        cliente_retornado = Cliente(
            id=1,
            nome="João Silva",
            cpf="123.456.789-00",
            data_nascimento=date(1990, 1, 1)
        )
        repo_mock.adicionar.return_value = cliente_retornado

        service = ClienteService(repo_mock)

        resultado = service.cadastrar_cliente(
            nome="João Silva",
            cpf="123.456.789-00",
            data_nascimento=date(1990, 1, 1)
        )

        repo_mock.adicionar.assert_called_once()
        chamado = repo_mock.adicionar.call_args[0][0]
        assert chamado.id == 0
        assert chamado.nome == "João Silva"
        assert chamado.cpf == "123.456.789-00"
        assert chamado.data_nascimento == date(1990, 1, 1)
        assert resultado == cliente_retornado

    def test_obter_cliente_existente(self):
        """Testa obter um cliente existente."""
        repo_mock = Mock(spec=ClienteRepository)
        cliente = Cliente(
            id=1,
            nome="Maria Santos",
            cpf="987.654.321-00",
            data_nascimento=date(1985, 5, 15)
        )
        repo_mock.obter_por_id.return_value = cliente

        service = ClienteService(repo_mock)

        resultado = service.obter_cliente(1)

        repo_mock.obter_por_id.assert_called_once_with(1)
        assert resultado == cliente

    def test_obter_cliente_inexistente(self):
        """Testa obter um cliente inexistente."""
        repo_mock = Mock(spec=ClienteRepository)
        repo_mock.obter_por_id.return_value = None

        service = ClienteService(repo_mock)

        resultado = service.obter_cliente(999)

        repo_mock.obter_por_id.assert_called_once_with(999)
        assert resultado is None

    def test_listar_clientes(self):
        """Testa listar todos os clientes."""
        repo_mock = Mock(spec=ClienteRepository)
        clientes = [
            Cliente(id=1, nome="Cliente 1", cpf="111", data_nascimento=date(1990, 1, 1)),
            Cliente(id=2, nome="Cliente 2", cpf="222", data_nascimento=date(1990, 1, 1))
        ]
        repo_mock.listar.return_value = clientes

        service = ClienteService(repo_mock)

        resultado = service.listar_clientes()

        repo_mock.listar.assert_called_once()
        assert resultado == clientes

    def test_listar_clientes_vazio(self):
        """Testa listar clientes quando não há nenhum."""
        repo_mock = Mock(spec=ClienteRepository)
        repo_mock.listar.return_value = []

        service = ClienteService(repo_mock)

        resultado = service.listar_clientes()

        repo_mock.listar.assert_called_once()
        assert resultado == []

    def test_cadastrar_cliente_com_dados_minimos(self):
        """Testa cadastro com dados mínimos obrigatórios."""
        repo_mock = Mock(spec=ClienteRepository)
        cliente_retornado = Cliente(
            id=1,
            nome="Pedro",
            cpf="123",
            data_nascimento=date(2000, 1, 1)
        )
        repo_mock.adicionar.return_value = cliente_retornado

        service = ClienteService(repo_mock)

        resultado = service.cadastrar_cliente(
            nome="Pedro",
            cpf="123",
            data_nascimento=date(2000, 1, 1)
        )

        assert resultado.id == 1
        assert resultado.ativo is True  # valor padrão
        assert resultado.data_cadastro == date.today()  # valor padrão