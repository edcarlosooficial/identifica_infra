# Mareo Identifica Infra — FREE

> **Mareo Tecnologia** · Navegando nas águas da informação  
> **Amostra pública** de mapeamento e diagnóstico leve de rede.

O **Mareo Identifica Infra FREE** foi criado como uma demonstração simples do trabalho da Mareo Tecnologia em automação de infraestrutura.

A versão gratuita **mapeia a rede**. Ela não faz inventário profundo de hardware, softwares ou periféricos de outros equipamentos.

## O que a versão FREE faz

- IP único, faixa IPv4 ou rede CIDR;
- descoberta de hosts por ICMP e conexões TCP simples;
- DNS reverso;
- MAC quando disponível na tabela ARP local;
- teste de uma lista curta de serviços comuns;
- indício de sistema operacional por heurística;
- diagnóstico simples por host;
- exportação JSON e CSV;
- limite de **256 hosts por execução**;
- concorrência limitada a **8 hosts simultâneos**.

## Perfil de segurança da FREE

A versão pública foi propositalmente desenhada para ter comportamento previsível e transparente:

- **não usa credenciais**;
- **não executa comandos em outros hosts**;
- **não tenta autenticação**;
- **não usa SMB/SSH/WinRM para lateralidade**;
- **não instala serviços ou persistência**;
- **não altera firewall, Defender, UAC ou políticas do sistema**;
- **não explora vulnerabilidades**;
- **não usa ofuscação, injeção de processo ou técnicas de evasão**;
- **não captura payload de aplicações**;
- exige confirmação de autorização na interface e `--authorized` na CLI.

A presença de SSH, SMB, RDP ou WinRM no resultado significa apenas que uma conexão TCP simples identificou a porta como acessível.

## Exemplos

```text
192.168.1.10
192.168.1.10-192.168.1.50
192.168.1.0/24
```

CLI:

```bash
python mareo_mapper.py 192.168.1.0/24 --authorized
```

Interface gráfica:

```bash
python mareo_gui.py
```

## Plataformas

| Plataforma | Formato |
|---|---|
| Windows | Executável gerado via PyInstaller |
| Linux | Binário gerado via PyInstaller |
| macOS | Aplicação CLI Python / build PyInstaller |
| Android | CLI via Termux |
| iOS/iPadOS | Projeto Swift demonstrativo com Network.framework |

> No iOS/iPadOS não existe um “executável Unix universal” instalável como em Linux. Apps precisam ser compilados e assinados pelo ecossistema Apple e estão sujeitos às permissões de Rede Local.

## Segurança e falsos positivos

Nenhum software legítimo consegue garantir que jamais haverá falso positivo de antivírus/EDR. Para reduzir esse risco, o projeto evita comportamentos típicos de malware e mantém o código da FREE aberto e auditável.

Para distribuição profissional, a recomendação é assinar os binários com certificado de **code signing**, publicar hashes SHA-256 e manter builds reproduzíveis via GitHub Actions. O repositório não contém certificado ou chave privada.

Veja também [SECURITY.md](SECURITY.md).

## Diferença para a versão completa

A edição completa da Mareo é privada e modular. Conforme autorização e escopo, pode integrar inventário de hardware, software e periféricos, agentes, SNMP, WinRM/CIM, SSH, NetBox/CMDB, Zabbix, Grafana, OpenTelemetry, Graylog, histórico e AIOps.

Mesmo na FULL, protocolos administrativos são usados apenas como mecanismos explícitos de administração autorizada; o produto não implementa evasão, exploração ou movimentação lateral automática.

## Autor

**Edcarlos Silva**  
**Mareo Tecnologia**

## Licença

MIT para esta amostra pública.
