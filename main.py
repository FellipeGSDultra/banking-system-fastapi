# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from typing import List

# Importando dos nossos arquivos organizados na pasta 'src'
from src.database import users_db, transactions_db
from src.models import UserCreate, DepositRequest, TransferRequest, TransactionHistory, Token
from src.security import get_password_hash, verify_password, create_access_token, get_current_user

app = FastAPI(title="Banking API Organizada", version="2.0.0")

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    users_db[user.username] = {
        "password": get_password_hash(user.password),
        "balance": 0.0
    }
    return {"message": f"Usuário {user.username} criado com sucesso!"}

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/deposit")
async def deposit(request: DepositRequest, current_user: str = Depends(get_current_user)):
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que zero")
    
    users_db[current_user]["balance"] += request.amount
    
    transactions_db.append({
        "type": "DEPOSIT", "amount": request.amount, 
        "sender": current_user, "receiver": current_user,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return {"message": "Depósito realizado", "saldo_atual": users_db[current_user]["balance"]}

@app.post("/transfer")
async def transfer(request: TransferRequest, current_user: str = Depends(get_current_user)):
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser maior que zero")
    if request.target_user not in users_db:
        raise HTTPException(status_code=404, detail="Conta de destino não existe")
    if users_db[current_user]["balance"] < request.amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
        
    users_db[current_user]["balance"] -= request.amount
    users_db[request.target_user]["balance"] += request.amount
    
    transactions_db.append({
        "type": "TRANSFER", "amount": request.amount,
        "sender": current_user, "receiver": request.target_user,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return {"message": "Transferência realizada com sucesso"}

@app.get("/history", response_model=List[TransactionHistory])
async def get_history(current_user: str = Depends(get_current_user)):
    return [t for t in transactions_db if t["sender"] == current_user or t["receiver"] == current_user]