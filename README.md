# TradingView → Discord Alert Formatter (Python)

Formatea alertas (texto/JSON) y las publica en un canal de Discord.

## ⚠️ Seguridad
Este repo está sanitizado: **no contiene tokens**.  
Antes de usarlo:
1) Creá un bot en Discord y obtené el token.
2) Definí variables de entorno (ver `.env.example`).
3) **Rotá cualquier token viejo** si alguna vez estuvo en un repo.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# completá .env
python formateo_alerta_tradingview.py
```
