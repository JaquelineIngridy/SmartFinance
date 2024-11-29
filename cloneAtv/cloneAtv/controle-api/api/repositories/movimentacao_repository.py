from sqlalchemy import select
from sqlalchemy.orm import Session
from ..schemas.movimentacao import movimentacao_retorno_schema
from ..schemas.movimentacao import movimentacao_requisicao_schema
from api.models import models
from datetime import datetime 

def criar_movimentacao(movimentacao: movimentacao_requisicao_schema, db: Session):
    nova_movimentacao = models.Movimentacao(
        UsuarioId=movimentacao.UsuarioId,
        Categoria=movimentacao.Categoria,
        Valor=movimentacao.Valor,
        TipoMovimentacaoId=movimentacao.TipoMovimentacaoId,
        DataMovimentacao=movimentacao.DataMovimentacao,
        Descricao=movimentacao.Descricao,
        DataCriacao=datetime.now()
    )

    db.add(nova_movimentacao)
    db.commit()
    db.refresh(nova_movimentacao)

    return nova_movimentacao

def listar_movimentacao_usuario(id: int, db: Session):

    db_movimentacoes = db.scalars(
        select(models.Movimentacao)
        .join(models.Movimentacao.TipoMovimentacao_)
        .join(models.Movimentacao.Usuario_)
        .where(models.Movimentacao.UsuarioId == id)
    ).all()

    return [
        movimentacao_retorno_schema.MovimentacaoRetornoSchema(
            Id=db_mov.Id,
            UsuarioMovimentacao=movimentacao_retorno_schema.UsuarioMovimentacao(
                Id=db_mov.Usuario_.Id,
                CPF=db_mov.Usuario_.CPF,
                Nome=db_mov.Usuario_.Nome,
                Email=db_mov.Usuario_.Email
            ),
            Categoria=db_mov.Categoria,
            Valor=db_mov.Valor,
            TipoMovimentacao=movimentacao_retorno_schema.TipoMovimentacao(
                Id=db_mov.TipoMovimentacao_.Id,
                Codigo=db_mov.TipoMovimentacao_.Codigo,
                Descricao=db_mov.TipoMovimentacao_.Descricao
            ),
            DataMovimentacao=db_mov.DataMovimentacao,
            Descricao=db_mov.Descricao,
            DataCriacao=db_mov.DataCriacao,
            DataPrevista=db_mov.DataPrevista,
            DataFim=db_mov.DataFim,
            DataAtualizacao=db_mov.DataAtualizacao
        )

        for db_mov in db_movimentacoes
    ]