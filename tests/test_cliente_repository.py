import pytest
from datetime import date
from credit_risk_engine.models import Cliente
from credit_risk_engine.repositories import ClienteRepository


class TestClienteRepository:
    def test_adicionar_cliente_com_id_zero(self):
        """Testa adicionar um cliente com id=0, deve gerar id automaticamente."""
        repo = ClienteRepository()
        cliente = Cliente(
            id=0,
            nome="João Silva",
            cpf="123.456.789-00",
            data_nascimento=date(1990, 1, 1)
        )

        resultado = repo.adicionar(cliente)

        assert resultado.id == 1
        assert resultado.nome == "João Silva"
        assert resultado.cpf == "123.456.789-00"

    def test_adicionar_cliente_com_id_existente(self):
        """Testa adicionar um cliente com id específico."""
        repo = ClienteRepository()
        cliente = Cliente(
            id=5,
            nome="Maria Santos",
            cpf="987.654.321-00",
            data_nascimento=date(1985, 5, 15)
        )

        resultado = repo.adicionar(cliente)

        assert resultado.id == 5
        assert resultado.nome == "Maria Santos"

    def test_obter_por_id_existente(self):
        """Testa obter cliente por id existente."""
        repo = ClienteRepository()
        cliente = Cliente(
            id=1,
            nome="Pedro Costa",
            cpf="111.222.333-44",
            data_nascimento=date(1995, 10, 20)
        )
        repo.adicionar(cliente)

        resultado = repo.obter_por_id(1)

        assert resultado is not None
        assert resultado.id == 1
        assert resultado.nome == "Pedro Costa"

    def test_obter_por_id_inexistente(self):
        """Testa obter cliente por id inexistente."""
        repo = ClienteRepository()

        resultado = repo.obter_por_id(999)

        assert resultado is None

    def test_listar_clientes_vazio(self):
        """Testa listar clientes quando o repositório está vazio."""
        repo = ClienteRepository()

        resultado = repo.listar()

        assert resultado == []

    def test_listar_clientes_com_dados(self):
        """Testa listar clientes com dados."""
        repo = ClienteRepository()
        cliente1 = Cliente(id=1, nome="Cliente 1", cpf="111", data_nascimento=date(1990, 1, 1))
        cliente2 = Cliente(id=2, nome="Cliente 2", cpf="222", data_nascimento=date(1990, 1, 1))
        repo.adicionar(cliente1)
        repo.adicionar(cliente2)

        resultado = repo.listar()

        assert len(resultado) == 2
        assert any(c.id == 1 for c in resultado)
        assert any(c.id == 2 for c in resultado)

    def test_ids_unicos_automaticos(self):
        """Testa que ids são gerados de forma única automaticamente."""
        repo = ClienteRepository()
        cliente1 = Cliente(id=0, nome="Cliente 1", cpf="111", data_nascimento=date(1990, 1, 1))
        cliente2 = Cliente(id=0, nome="Cliente 2", cpf="222", data_nascimento=date(1990, 1, 1))

        repo.adicionar(cliente1)
        repo.adicionar(cliente2)

        assert cliente1.id == 1
        assert cliente2.id == 2

    def test_adicionar_cliente_com_atributos_opcionais(self):
        """Testa adicionar cliente com atributos opcionais."""
        repo = ClienteRepository()
        cliente = Cliente(
            id=0,
            nome="Ana Paula",
            cpf="333.444.555-66",
            data_nascimento=date(1980, 3, 10),
            ativo=False
        )

        resultado = repo.adicionar(cliente)

        assert resultado.ativo is False
        assert resultado.data_cadastro == date.today()