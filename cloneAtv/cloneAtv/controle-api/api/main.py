from fastapi import FastAPI
from api.routers import balanco_mensal_router, investimentos_router, metas_financeiras_router, orcamento_mensal_router, tipo_movimentacao_router, user_router, movimentacao_router
from auth import router as auth_router

app = FastAPI()

app.include_router(user_router.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(movimentacao_router.router, prefix="/movimentacao", tags=["Movimentações"])
app.include_router(investimentos_router.router, prefix="/investimentos", tags=["Investimentos"])
app.include_router(metas_financeiras_router.router, prefix="/metas", tags=["Metas Financeiras"])
app.include_router(orcamento_mensal_router.router, prefix="/orcamentos", tags=["Orçamento mensal"])
app.include_router(tipo_movimentacao_router.router, prefix="/tipo", tags=["Tipo movimentação"])
app.include_router(balanco_mensal_router.router, prefix="/balanco", tags=["Balanço mensal"])

