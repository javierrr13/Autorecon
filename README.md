# 🔍 AutoRecon - Automated Security Reconnaissance Framework

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Nmap Integration](https://img.shields.io/badge/nmap-integrated-orange)](https://nmap.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**AutoRecon** es un framework de reconocimiento de seguridad automatizado escrito en Python que integra herramientas profesionales como Nmap y Subfinder para realizar auditorías de seguridad completas y automatizadas.

## ✨ **Características Destacadas**

### 🔥 **Escaneo Inteligente Multi-fase**
- **Escaneo rápido TCP**: Top 1000 puertos con detección de servicios y versiones
- **Escaneo completo TCP**: Todos los puertos (-p-) con detección avanzada
- **Integración nativa con Nmap**: Usa la API oficial de `python-nmap`
- **Parseo estructurado**: Resultados en JSON listos para procesamiento

### 🎯 **Enumeración Contextual**
- **Sistema de plugins**: Arquitectura modular y extensible
- **Detección automática de servicios**: Ejecuta plugins basados en servicios encontrados
- **Enumeración de subdominios**: Integra Subfinder, DNSx y FFuF
- **Brute-force inteligente**: Solo cuando se solicita explícitamente

### 📊 **Gestión Profesional de Resultados**
- **Salida estructurada**: JSON para procesamiento automatizado
- **Reportes formateados**: Markdown listos para presentación
- **Organización automática**: Directorios por objetivo/IP
- **Persistencia completa**: Todos los resultados guardados automáticamente

## 🏗️ **Arquitectura del Sistema**

### **Core Components**

```python
# scanner.py - Motor principal de escaneo
class Scanner:
    """
    Sistema de escaneo basado en Nmap con dos modos:
    1. run_fast(): Escaneo rápido top 1000 puertos
    2. run_full(): Escaneo completo todos los puertos
    """
    
    def _parse_nmap(self, nm):
        """
        Parseo inteligente de resultados Nmap:
        - Filtra hosts activos/inactivos
        - Extrae: puerto, servicio, producto, versión
        - Organiza por protocolo (TCP/UDP)
        """

# enumerator.py - Sistema de enumeración
class Enumerator:
    """
    Coordinador de plugins de enumeración:
    - Detecta servicios escaneados
    - Ejecuta plugins correspondientes
    - Combina resultados automáticamente
    """

# subdom.py - Plugin de enumeración de subdominios
class SubdomPlugin(PluginABC):
    """
    Plugin de descubrimiento de subdominios:
    - Subfinder: Descubrimiento pasivo
    - DNSx: Resolución y filtrado wildcard
    - FFuF: Brute-force opcional
    """
