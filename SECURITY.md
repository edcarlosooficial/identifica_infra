# Política de Segurança — Mareo Identifica Infra FREE

## Objetivo

A edição FREE é um **mapeador de rede demonstrativo**, não uma ferramenta ofensiva.

## Comportamentos deliberadamente ausentes

O projeto não implementa:

- execução remota;
- tentativa de senhas ou credenciais;
- reutilização de tokens/sessões;
- movimentação lateral;
- persistência;
- bypass de UAC, firewall ou antimalware;
- exploração de vulnerabilidades;
- injeção de código;
- shellcode;
- carregamento reflexivo;
- ofuscação para evitar detecção;
- desativação de logs ou trilhas;
- captura de payload.

## Descoberta de serviços

A FREE usa apenas ICMP e conexões TCP curtas em uma lista pequena e documentada de portas. Não há handshake de autenticação nem execução de protocolo administrativo.

## Autorização

Use apenas em redes próprias ou com autorização explícita. A CLI exige `--authorized`; a GUI pede confirmação antes da análise.

## Distribuição

Para reduzir falsos positivos:

1. prefira builds reproduzíveis;
2. publique SHA-256 dos artefatos;
3. assine executáveis e instaladores com certificado de code signing quando houver infraestrutura de assinatura;
4. não ofusque o binário;
5. mantenha metadados de produto, fabricante e versão;
6. submeta falsos positivos aos fornecedores de antivírus quando necessário.

Nenhuma dessas medidas garante ausência total de falso positivo, mas elas tornam a proveniência e o comportamento do software mais verificáveis.
