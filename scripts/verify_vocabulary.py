import os
import re
import sys

def carregar_dicionario_atual(folder_path):
    """Varre a pasta atual e mapeia o status de cada palavra existente."""
    known_words = set()
    unknown_words = set()
    
    known_pattern = re.compile(r'-\s+\[x\]\s+\d+\.\s+(.+)')
    unknown_pattern = re.compile(r'-\s+\[\s*\]\s+\d+\.\s+(.+)')
    
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.md'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        known_match = known_pattern.search(line)
                        if known_match:
                            known_words.add(known_match.group(1).strip().lower())
                            continue
                        
                        unknown_match = unknown_pattern.search(line)
                        if unknown_match:
                            unknown_words.add(unknown_match.group(1).strip().lower())
    else:
        print(f"Erro: A pasta base '{folder_path}' não foi encontrada.")
        sys.exit(1)
        
    return known_words, unknown_words

def extrair_palavras_do_texto(texto_path):
    """Lê o texto alvo, remove pontuações e extrai palavras únicas."""
    if not os.path.exists(texto_path):
        print(f"Erro: O arquivo de texto '{texto_path}' não foi encontrado.")
        sys.exit(1)
        
    with open(texto_path, 'r', encoding='utf-8') as f:
        conteudo = f.read().lower()
    
    # Usa regex para pegar apenas letras e apóstrofos (ex: "don't", "it's")
    palavras = re.findall(r"\b[a-zA-Z']+\b", conteudo)
    return set(palavras)

def analisar_texto(pasta_dicionario, caminho_texto):
    # 1. Carrega o panorama atual do seu vocabulário
    known_set, unknown_set = carregar_dicionario_atual(pasta_dicionario)
    
    # 2. Extrai as palavras do texto que você quer ler/analisar
    palavras_texto = extrair_palavras_do_texto(caminho_texto)
    
    # 3. Separa e cruza as informações
    ja_conhecidas = palavras_texto.intersection(known_set)
    ja_em_estudo = palavras_texto.intersection(unknown_set)
    totalmente_novas = palavras_texto - known_set - unknown_set
    
    # Imprime o relatório no terminal
    print("\n" + "="*40)
    print(f" ANÁLISE DE TEXTO: {os.path.basename(caminho_texto)}")
    print("="*40)
    print(f"Total de palavras únicas no texto: {len(palavras_texto)}")
    print(f"✓ Já conhecidas [x]: {len(ja_conhecidas)}")
    print(f"⏳ Já em estudo [ ]: {len(ja_em_estudo)}")
    print(f"❌ Não adicionadas ainda: {len(totalmente_novas)}")
    print("="*40)
    
    if totalmente_novas:
        print("\n[!] PALAVRAS QUE VOCÊ AINDA NÃO ADICIONOU NO SEU DICIONÁRIO:")
        # Ordena alfabeticamente para facilitar a leitura
        lista_novas = sorted(list(totalmente_novas))
        print(", ".join(lista_novas))
        
        # Opcional: Mostra as palavras em formato de string separada por vírgula 
        # pronto para você copiar e mandar para o seu primeiro script!
        print("\nFormato pronto para copiar e injetar no script anterior:")
        print(",".join(lista_novas))
    else:
        print("\n🎉 Boa! Todas as palavras desse texto já estão mapeadas no seu dicionário.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Erro: Você precisa passar o caminho do arquivo de texto.")
        print("Exemplo: python3 verificar_texto.py ./artigo.txt")
        sys.exit(1)
        
    pasta_dicionario = "../words"
    caminho_do_texto = sys.argv[1]
    
    analisar_texto(pasta_dicionario, caminho_do_texto)