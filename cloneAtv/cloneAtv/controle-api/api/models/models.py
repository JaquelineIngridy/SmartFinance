from typing import List, Optional

from sqlalchemy import CHAR, DECIMAL, Date, DateTime, ForeignKeyConstraint, Identity, Index, Integer, LargeBinary, PrimaryKeyConstraint, String, Unicode, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class TipoMovimentacao(Base):
    __tablename__ = 'TipoMovimentacao'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK__TipoMovi__3214EC07196AE385'),
        Index('UQ__TipoMovi__06370DAC527E6F7A', 'Codigo', unique=True)
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    Codigo: Mapped[str] = mapped_column(Unicode(50, 'Latin1_General_CI_AS'))
    Descricao: Mapped[str] = mapped_column(Unicode(100, 'Latin1_General_CI_AS'))

    Movimentacao: Mapped[List['Movimentacao']] = relationship('Movimentacao', back_populates='TipoMovimentacao_')


class Usuario(Base):
    __tablename__ = 'Usuario'
    __table_args__ = (
        PrimaryKeyConstraint('Id', name='PK__Usuario__3214EC073A7F9860'),
        Index('UQ__Usuario__A9D10534B698A436', 'Email', unique=True),
        Index('UQ__Usuario__C1F89731C448F18D', 'CPF', unique=True)
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    CPF: Mapped[str] = mapped_column(String(14, 'Latin1_General_CI_AS'))
    Nome: Mapped[str] = mapped_column(Unicode(250, 'Latin1_General_CI_AS'))
    Email: Mapped[str] = mapped_column(Unicode(100, 'Latin1_General_CI_AS'))
    DataNascimento: Mapped[datetime.date] = mapped_column(Date)
    Sexo: Mapped[str] = mapped_column(CHAR(1, 'Latin1_General_CI_AS'))
    DataCriacao: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('(getdate())'))
    DataAtualizacao: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DataFim: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    Senha: Mapped[Optional[bytes]] = mapped_column(LargeBinary(64))

    BalancoMensal: Mapped[List['BalancoMensal']] = relationship('BalancoMensal', back_populates='usuario')
    HistoricoLogin: Mapped[List['HistoricoLogin']] = relationship('HistoricoLogin', back_populates='Usuario_')
    Investimentos: Mapped[List['Investimentos']] = relationship('Investimentos', back_populates='usuario')
    MetasFinanceiras: Mapped[List['MetasFinanceiras']] = relationship('MetasFinanceiras', back_populates='usuario')
    Movimentacao: Mapped[List['Movimentacao']] = relationship('Movimentacao', back_populates='Usuario_')
    OrcamentoMensal: Mapped[List['OrcamentoMensal']] = relationship('OrcamentoMensal', back_populates='usuario')


class BalancoMensal(Base):
    __tablename__ = 'BalancoMensal'
    __table_args__ = (
        ForeignKeyConstraint(['usuario_id'], ['Usuario.Id'], name='FK__BalancoMe__usuar__5EBF139D'),
        PrimaryKeyConstraint('id', name='PK__BalancoM__3213E83FFEE31301')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    usuario_id: Mapped[int] = mapped_column(Integer)
    mes_referencia: Mapped[datetime.date] = mapped_column(Date)
    receita_total: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 2))
    despesas_totais: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 2))
    saldo_inicial: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 2))
    saldo_final: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 2))

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='BalancoMensal')


class HistoricoLogin(Base):
    __tablename__ = 'HistoricoLogin'
    __table_args__ = (
        ForeignKeyConstraint(['UsuarioId'], ['Usuario.Id'], name='FK__Historico__Usuar__70DDC3D8'),
        PrimaryKeyConstraint('Id', name='PK__Historic__3214EC07FC65305C')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    UsuarioId: Mapped[int] = mapped_column(Integer)
    DataLogin: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('(getdate())'))
    IPAddress: Mapped[Optional[str]] = mapped_column(String(45, 'Latin1_General_CI_AS'))

    Usuario_: Mapped['Usuario'] = relationship('Usuario', back_populates='HistoricoLogin')


class Investimentos(Base):
    __tablename__ = 'Investimentos'
    __table_args__ = (
        ForeignKeyConstraint(['usuario_id'], ['Usuario.Id'], name='FK__Investime__usuar__6A30C649'),
        PrimaryKeyConstraint('id', name='PK__Investim__3213E83F0C7A1F7B')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    usuario_id: Mapped[int] = mapped_column(Integer)
    tipo_investimento: Mapped[str] = mapped_column(String(100, 'Latin1_General_CI_AS'))
    valor_investido: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 0))
    data_investido: Mapped[datetime.date] = mapped_column(Date)
    valor_atual: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 0))

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='Investimentos')


class MetasFinanceiras(Base):
    __tablename__ = 'MetasFinanceiras'
    __table_args__ = (
        ForeignKeyConstraint(['usuario_id'], ['Usuario.Id'], name='FK__MetasFina__usuar__6D0D32F4'),
        PrimaryKeyConstraint('id', name='PK__MetasFin__3213E83FC47712E2')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    usuario_id: Mapped[int] = mapped_column(Integer)
    descricao_meta: Mapped[str] = mapped_column(String(250, 'Latin1_General_CI_AS'))
    valor_meta: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 0))
    valor_atual: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 0))
    data_limite: Mapped[datetime.date] = mapped_column(Date)

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='MetasFinanceiras')


class Movimentacao(Base):
    __tablename__ = 'Movimentacao'
    __table_args__ = (
        ForeignKeyConstraint(['IdTipoMovimentacao'], ['TipoMovimentacao.Id'], name='FK__Movimenta__IdTip__571DF1D5'),
        ForeignKeyConstraint(['UsuarioId'], ['Usuario.Id'], name='FK__Movimenta__Usuar__5629CD9C'),
        PrimaryKeyConstraint('Id', name='PK__Moviment__3214EC078B5F0DE1')
    )

    Id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    UsuarioId: Mapped[int] = mapped_column(Integer)
    Categoria: Mapped[str] = mapped_column(Unicode(100, 'Latin1_General_CI_AS'))
    Valor: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 2))
    IdTipoMovimentacao: Mapped[int] = mapped_column(Integer)
    DataMovimentacao: Mapped[datetime.date] = mapped_column(Date)
    Descricao: Mapped[str] = mapped_column(Unicode(250, 'Latin1_General_CI_AS'))
    DataCriacao: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=text('(getdate())'))
    DataPrevista: Mapped[Optional[datetime.date]] = mapped_column(Date)
    DataFim: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    DataAtualizacao: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    TipoMovimentacao_: Mapped['TipoMovimentacao'] = relationship('TipoMovimentacao', back_populates='Movimentacao')
    Usuario_: Mapped['Usuario'] = relationship('Usuario', back_populates='Movimentacao')


class OrcamentoMensal(Base):
    __tablename__ = 'OrcamentoMensal'
    __table_args__ = (
        ForeignKeyConstraint(['usuario_id'], ['Usuario.Id'], name='FK__Orcamento__usuar__6754599E'),
        PrimaryKeyConstraint('id', name='PK__Orcament__3213E83F1EFD2859')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1), primary_key=True)
    usuario_id: Mapped[int] = mapped_column(Integer)
    mes_referencia: Mapped[datetime.date] = mapped_column(Date)
    valor_orcamento: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 0))
    valor_gasto: Mapped[decimal.Decimal] = mapped_column(DECIMAL(18, 0))
    data_criacao: Mapped[datetime.date] = mapped_column(Date)
    data_atualizacao: Mapped[datetime.date] = mapped_column(Date)

    usuario: Mapped['Usuario'] = relationship('Usuario', back_populates='OrcamentoMensal')
