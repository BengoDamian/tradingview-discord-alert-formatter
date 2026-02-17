import os
from dotenv import load_dotenv
load_dotenv()

import pyperclip
import json
import re

def clasificar_mensaje(mensaje_completo):
    mensaje_completo = mensaje_completo.lower()
    clasificaciones = []

    # Temporalidad
    if any(temp in mensaje_completo for temp in ["m3", "m5"]):
        clasificaciones.append(("⏱️", "Temporalidad muy corta (1-5 minutos)"))
    elif "m15" in mensaje_completo:
        clasificaciones.append(("⏲️", "Temporalidad corta (15 minutos)"))
    elif "h1" in mensaje_completo:
        clasificaciones.append(("🕐", "Temporalidad media (1 hora)"))
    elif "h2" in mensaje_completo:
        clasificaciones.append(("🕑", "Temporalidad media (2 horas)"))
    elif "h4" in mensaje_completo:
        clasificaciones.append(("🕓", "Temporalidad larga (4 horas)"))
    elif "diario" in mensaje_completo:
        clasificaciones.append(("📅", "Temporalidad diaria"))
    else:
        clasificaciones.append(("🗓️", "Temporalidad no especificada"))

    # Acción y Advertencia
    if "bos" in mensaje_completo:
        clasificaciones.append(("✅", "Confirmación de la señal, posible entrada"))
    if any(palabra in mensaje_completo for palabra in ["espera", "atento", "vigilar", "monitorear", "seguimiento"]):
        clasificaciones.append(("⏳", "En espera de confirmación o más señales"))
    if any(palabra in mensaje_completo for palabra in ["descartada", "sin validez"]):
        clasificaciones.append(("❌", "Alerta descartada"))
    if any(palabra in mensaje_completo for palabra in ["cuidado", "precaución", "precaucion"]):
        clasificaciones.append(("⚠️", "Requiere precaución"))
    if any(palabra in mensaje_completo for palabra in ["reteste", "pullback", "retesteo"]):
        clasificaciones.append(("🔄", "Retesteo de nivel, posible oportunidad"))
    if "preparar" in mensaje_completo:
        clasificaciones.append(("🔧", "Preparación para posible entrada"))
    if any(palabra in mensaje_completo for palabra in ["revisar", "controlar"]):
        clasificaciones.append(("🔍", "Revisar y analizar la situación actual"))
    if any(palabra in mensaje_completo for palabra in ["crítica", "urgente", "inmediata"]):
        clasificaciones.append(("🔴", "Atención inmediata requerida"))
    if any(palabra in mensaje_completo for palabra in ["zona", "nivel", "poi"]):
        clasificaciones.append(("🟣", "Zona o nivel importante identificado"))

    # Compra o Venta
    if "compra" in mensaje_completo:
        clasificaciones.append(("🟢", "Compra"))
    if "venta" in mensaje_completo:
        clasificaciones.append(("🔴", "Venta"))

    # Tipo de Operación
    if "swing" in mensaje_completo:
        if "macro" in mensaje_completo:
            clasificaciones.append(("📈", "Macro para Swing"))
        elif "micro" in mensaje_completo:
            clasificaciones.append(("📉", "Micro para Swing"))
        else:
            clasificaciones.append(("🔄", "Swing"))
    elif "macro" in mensaje_completo:
        clasificaciones.append(("📊", "Macro"))
    elif "micro" in mensaje_completo:
        clasificaciones.append(("📉", "Micro"))
    elif "intraday" in mensaje_completo:
        clasificaciones.append(("⏳", "Intraday"))

    return clasificaciones

def extraer_parte(mensaje_completo, palabras_clave):
    for palabra in palabras_clave:
        if palabra in mensaje_completo:
            return palabra
    return ""

print("Este script permite generar un mensaje de alerta para TradingView.\n")
print("Instrucciones:")
print("Introduce la información de la alerta en un solo mensaje.\n")

while True:
    # Solicita la entrada del usuario en un solo mensaje
    mensaje_completo = input("Introduce el mensaje de alerta completo (o 'salir' para terminar): ")
    
    if mensaje_completo.lower() == 'salir':
        break

    # Variables para el ticker y precio
    ticker = "{{ticker}}"
    close = "{{close}}"

    # Clasificar el mensaje
    clasificaciones = clasificar_mensaje(mensaje_completo)

    # Extraer partes del mensaje
    temporalidades = ["m3", "m5", "m15", "h1", "h2", "h4", "diario"]
    temporalidad = next((temp for temp in temporalidades if temp in mensaje_completo), "no especificada")
    
    # Eliminar la primera temporalidad del mensaje completo
    mensaje_completo_sin_temporalidad = mensaje_completo.replace(temporalidad, "", 1)
    
    accion = extraer_parte(mensaje_completo_sin_temporalidad, ["bos", "espera", "atento", "vigilar", "monitorear", "seguimiento", "descartada", "sin validez", "cuidado", "precaución", "precaucion", "reteste", "pullback", "retesteo", "preparar", "revisar", "controlar", "crítica", "urgente", "inmediata", "zona", "nivel", "poi", "compra", "venta"])
    
    # Extraer advertencia entre paréntesis
    advertencia = re.search(r'\((.*?)\)', mensaje_completo_sin_temporalidad)
    advertencia = advertencia.group(1) if advertencia else ""

    comentario = mensaje_completo_sin_temporalidad.replace(accion, "").replace(f"({advertencia})", "").strip()

    # Crear el mensaje formateado
    mensaje_formateado = f"🔔 ALERTA: {ticker}\n"
    mensaje_formateado += f"{[c for c in clasificaciones if c[0] in ['⏱️', '⏲️', '🕐', '🕑', '🕓', '📅', '🗓️']][0][0]} Temporalidad: {temporalidad} - {[c for c in clasificaciones if c[0] in ['⏱️', '⏲️', '🕐', '🕑', '🕓', '📅', '🗓️']][0][1]}\n"
    mensaje_formateado += f"{[c for c in clasificaciones if c[0] == '✅'][0][0] if any(c[0] == '✅' for c in clasificaciones) else 'ℹ️'} Acción: {accion} - {[c for c in clasificaciones if c[0] == '✅'][0][1] if any(c[0] == '✅' for c in clasificaciones) else 'Información general'}\n"
    mensaje_formateado += f"💲 Precio Actual de la alerta: {close}\n"
    mensaje_formateado += f"{[c for c in clasificaciones if c[0] == '⚠️'][0][0] if any(c[0] == '⚠️' for c in clasificaciones) else '⚪'} Advertencia: {advertencia} - {[c for c in clasificaciones if c[0] == '⚠️'][0][1] if any(c[0] == '⚠️' for c in clasificaciones) else 'Impacto no especificado'}\n"
    mensaje_formateado += f"✍️ Comentario: {comentario}\n"

    # Añadir clasificación de tipo de operación si existe
    if any(c[0] in ['📈', '📉', '📊', '🔄', '⏳'] for c in clasificaciones):
        mensaje_formateado += f"{[c for c in clasificaciones if c[0] in ['📈', '📉', '📊', '🔄', '⏳']][0][0]} {clasificaciones[-1][1]}\n"

    # Añadir clasificación de compra o venta si existe
    if any(c[0] in ['🟢', '🔴'] for c in clasificaciones):
        mensaje_formateado += f"{[c for c in clasificaciones if c[0] in ['🟢', '🔴']][0][0]} {clasificaciones[-1][1]}\n"

    # Crea el mensaje en formato JSON para TradingView
    mensaje_tradingview = {
        "content": mensaje_formateado
    }

    # Convierte el mensaje a formato JSON legible
    mensaje_json = json.dumps(mensaje_tradingview, indent=2, ensure_ascii=False)

    # Copia el mensaje JSON al portapapeles
    pyperclip.copy(mensaje_json)

    # Imprime el mensaje formateado y el JSON en la consola
    print("\nMensaje formateado:")
    print(mensaje_formateado)
    print("\nMensaje JSON:")
    print(mensaje_json)
    print("\nMensaje JSON copiado al portapapeles. Pega directamente en TradingView.")

print("Programa terminado.")