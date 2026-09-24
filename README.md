# Mareo Identifica Infra — FREE

> **Mareo Tecnologia** · Navegando nas águas da informação  
> **Amostra pública** de mapeamento e diagnóstico leve de rede.

O **Mareo Identifica Infra FREE** foi criado como uma demonstração simples do trabalho da Mareo Tecnologia em automação de infraestrutura.

A versão gratuita **mapeia a rede**. Ela não faz inventário profundo de hardware, softwares ou periféricos de outros equipamentos.

## O que a versão FREE faz

- IP único, faixa IPv4 ou rede CIDR;
- descoberta de hosts por ICMP e TCP;
- DNS reverso;
- MAC quando disponível na tabela ARP local;
- teste de uma lista curta de serviços comuns;
- indício de sistema operacional por heurística;
- diagnóstico simples por host;
- exportação JSON e CSV;
- limite de **256 hosts por execução**.

## Exemplos

```text
192.168.1.10
192.168.1.10-192.168.1.50
192.168.1.0/24
```

## Plataformas

| Plataforma | Formato |
|---|---|
| Windows | Executável gerado via PyInstaller |
| Linux | Binário gerado via PyInstaller |
| macOS | Aplicação CLI Python / build PyInstaller |
| Android | CLI via Termux |
| iOS/iPadOS | Projeto Swift demonstrativo com Network.framework |

> No iOS/iPadOS não existe um “executável Unix universal” instalável como em Linux. Apps precisam ser compilados/assinados pelo ecossistema Apple e estão sujeitos às permissões de Rede Local. O código iOS deste repositório é uma amostra nativa limitada a diagnóstico TCP autorizado.

## Download

Os builds são produzidos pelo GitHub Actions em **Actions → Build Free**. Releases podem ser criadas a partir das tags do projeto.

## Executar com Python

```bash
python mareo_mapper.py 192.168.1.0/24
```

Interface gráfica:

```bash
python mareo_gui.py
```

## Android / Termux

```bash
pkg update
pkg install python
python mareo_mapper.py 192.168.1.0/24
```

## Segurança e autorização

Use somente em redes, equipamentos e ambientes que sejam seus ou para os quais você tenha autorização explícita.

A versão FREE não tenta credenciais, não explora vulnerabilidades e não captura conteúdo de aplicações.

## Diferença para a versão completa

A edição completa da Mareo é privada e modular. Conforme autorização e escopo, pode integrar inventário de hardware, software e periféricos, agentes, SNMP, WinRM/CIM, SSH, NetBox/CMDB, Zabbix, Grafana, OpenTelemetry, Graylog, histórico e AIOps.

## Autor

**Edcarlos Silva**  
**Mareo Tecnologia**

## Licença

MIT para esta amostra pública.
