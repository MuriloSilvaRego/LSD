# 🔧 Como Compilar Código LLVM IR

## ⚠️ Problema Comum: LLVM não instalado

Se você recebeu erro ao executar `llc`, provavelmente o LLVM não está instalado no seu sistema.

## 🪟 Windows

### Opção 1: Instalar LLVM (Recomendado)

1. **Baixar LLVM para Windows:**
   - Acesse: https://github.com/llvm/llvm-project/releases
   - Baixe a versão mais recente (ex: `LLVM-17.0.0-win64.exe`)
   - Execute o instalador
   - **IMPORTANTE**: Marque "Add LLVM to system PATH" durante a instalação

2. **Verificar instalação:**
   ```powershell
   llc --version
   ```

3. **Compilar:**
   ```powershell
   cd lib\parser
   llc output.ll -o output.s
   ```

### Opção 2: Usar WSL (Windows Subsystem for Linux)

Se você tem WSL instalado:

```bash
# No WSL
cd /mnt/c/Users/pedrov/Desktop/LSD/LSD/lib/parser
llc output.ll -o output.s
gcc output.s -o output
./output
```

### Opção 3: Usar Docker (Avançado)

```bash
docker run -v %CD%:/work -w /work llvm/llvm llc output.ll -o output.s
```

---

## 🐧 Linux

### Instalar LLVM

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install llvm

# Verificar
llc --version
```

### Compilar

```bash
cd lib/parser
llc output.ll -o output.s
gcc output.s -o output
./output
```

---

## 🍎 macOS

### Instalar LLVM

```bash
# Usando Homebrew
brew install llvm

# Adicionar ao PATH (se necessário)
export PATH="/opt/homebrew/opt/llvm/bin:$PATH"
```

### Compilar

```bash
cd lib/parser
llc output.ll -o output.s
gcc output.s -o output
./output
```

---

## ✅ Verificar se o Código LLVM está Correto

Antes de tentar compilar, você pode validar o código LLVM IR:

### Usando `opt` (se tiver LLVM instalado)

```bash
opt -verify output.ll
```

Se não houver erros, o código está sintaticamente correto.

---

## 🔍 Problemas Comuns e Soluções

### Erro: "llc: comando não encontrado"

**Causa**: LLVM não está instalado ou não está no PATH.

**Solução**:
- Windows: Instale LLVM e adicione ao PATH
- Linux: `sudo apt-get install llvm`
- macOS: `brew install llvm`

### Erro: "target triple mismatch"

**Causa**: O código foi gerado para um sistema diferente.

**Solução**: O gerador agora detecta automaticamente o sistema operacional. Se ainda der erro, edite manualmente o `output.ll`:

- Windows: `target triple = "x86_64-pc-windows-msvc"`
- Linux: `target triple = "x86_64-pc-linux-gnu"`
- macOS: `target triple = "x86_64-apple-darwin"`

### Erro: "gcc: comando não encontrado"

**Causa**: GCC não está instalado.

**Solução**:
- Windows: Instale MinGW-w64 ou use Visual Studio
- Linux: `sudo apt-get install gcc`
- macOS: Instale Xcode Command Line Tools: `xcode-select --install`

### Erro ao compilar assembly

**Causa**: Diferenças entre sistemas.

**Solução Windows (usando MinGW)**:
```powershell
gcc output.s -o output.exe
```

**Solução Windows (usando Visual Studio)**:
```powershell
cl output.s /Fe:output.exe
```

---

## 🎯 Alternativa: Usar Apenas o Interpretador

Se você não precisa compilar para executável, pode usar apenas o interpretador:

```bash
python executar_lsd.py exemplo_completo.lsd
```

Isso executa o código diretamente sem precisar de LLVM ou GCC.

---

## 📝 Exemplo Completo (Windows)

```powershell
# 1. Gerar código LLVM IR
cd lib\parser
python testar_geracao_codigo.py

# 2. Compilar para assembly (requer LLVM instalado)
llc output.ll -o output.s

# 3. Compilar para executável (requer GCC/MinGW)
gcc output.s -o output.exe

# 4. Executar
.\output.exe
```

---

## 🧪 Testar sem Compilar

Você pode validar que o código LLVM está correto verificando:

1. **Sintaxe**: O arquivo `output.ll` deve abrir sem erros
2. **Estrutura**: Deve ter `define i32 @main()`, `declare i32 @printf`, etc.
3. **Strings**: Devem estar no final do arquivo como `@str.X`

---

**Nota**: O código LLVM IR gerado está correto. O problema geralmente é a falta do LLVM instalado no sistema.

