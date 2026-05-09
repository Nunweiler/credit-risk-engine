from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Cliente:
    id: int
    nome: str
    cpf: str
    data_nascimento: date
    data_cadastro: date = field(default_factory=date.today)
    ativo: bool = True


@dataclass
class Renda:
    cliente_id: int
    renda_mensal: float
    fonte: str = 'não informado'
    data_registro: date = field(default_factory=date.today)


@dataclass
class Divida:
    id: int
    cliente_id: int
    valor: float
    descricao: str
    data_contratacao: date
    em_atraso: bool = False


@dataclass
class AvaliacaoRisco:
    cliente_id: int
    score: float
    categoria: str
    endividamento: float
    renda_mensal: float
    data_avaliacao: date = field(default_factory=date.today)
    detalhes: Optional[str] = None