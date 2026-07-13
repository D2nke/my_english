import os
import re
import sys

def process_all_vocabulary(folder_path, words_file_path):
    # 1. Valida e lê o arquivo com as NOVAS palavras (que serão as ÚNICAS desconhecidas)
    if not os.path.exists(words_file_path):
        print(f"Erro: O arquivo de palavras '{words_file_path}' não foi encontrado.")
        print("Uso correto: python3 script.py ./caminho_do_arquivo_com_palavras.md")
        return

    print(f"Lendo novas palavras desconhecidas de: {words_file_path}")
    with open(words_file_path, 'r', encoding='utf-8') as f:
        new_words_raw = f.read()
    
    # Limpa e formata as novas palavras (elas serão as únicas com [ ])
    new_unknown_words = [w.strip().lower() for w in new_words_raw.split(',') if w.strip()]
    
    # 2. Varre a pasta para coletar APENAS as palavras conhecidas [x]
    known_set = set()
    known_pattern = re.compile(r'-\s+\[x\]\s+\d+\.\s+(.+)')
    
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.md'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        # Procura APENAS por palavras conhecidas [x]
                        # As linhas com [ ] são completamente ignoradas e descartadas aqui!
                        known_match = known_pattern.search(line)
                        if known_match:
                            known_set.add(known_match.group(1).strip().lower())
    else:
        print(f"Erro: A pasta base '{folder_path}' não foi encontrada.")
        return
    
    # 3. Monta a lista de desconhecidas apenas com as novas palavras
    unknown_set = set()
    for word in new_unknown_words:
        # Se por acaso você passou uma palavra nova que já tinha marcado como conhecida antes,
        # o script mantém ela como conhecida para você não perder seu progresso anterior.
        if word not in known_set:
            unknown_set.add(word)
    
    # 4. Unifica conhecidas e as novas desconhecidas, ordenando o índice global
    all_words_sorted = sorted(list(known_set) + list(unknown_set))
    
    # 5. Geração dos arquivos estruturados de 1000 em 1000
    words_per_file = 1000
    words_per_subgroup = 100
    
    output_dir = "../updated_words"
    os.makedirs(output_dir, exist_ok=True)
    
    for i in range(0, len(all_words_sorted), words_per_file):
        file_chunk = all_words_sorted[i:i + words_per_file]
        
        low_bound = i
        high_bound = i + words_per_file
        filename = f"{low_bound}-{high_bound}.md"
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as out:
            out.write(f"# The {low_bound}-{high_bound} New Most Common English Words\n\n")
            out.write(f"A checklist to track my English vocabulary progress (Words {low_bound + 1}-{high_bound}).\n\n")
            out.write("---\n\n")
            
            for j in range(0, len(file_chunk), words_per_subgroup):
                subgroup_chunk = file_chunk[j:j + words_per_subgroup]
                
                start_sub_num = low_bound + j + 1
                end_sub_num = low_bound + j + words_per_subgroup
                
                out.write(f"## Words {start_sub_num}-{end_sub_num}\n\n")
                
                for index, word in enumerate(subgroup_chunk):
                    current_word_num = low_bound + j + index + 1
                    
                    # Se a palavra estiver no grupo das conhecidas antigas -> [x]
                    # Se for das novas que você acabou de passar -> [ ]
                    status_flag = "[x]" if word in known_set else "[ ]"
                    out.write(f"- {status_flag} {current_word_num}. {word}\n")
                
                out.write("\n")
                
        print(f"Gerado com sucesso: {file_path} contendo {len(file_chunk)} palavras.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Erro: Você precisa passar o caminho do arquivo de palavras.")
        print("Exemplo: python3 script.py ./novas_palavras.md")
        sys.exit(1)
    
    pasta_dicionario = "../words"
    arquivo_novas_palavras = sys.argv[1]
    
    process_all_vocabulary(pasta_dicionario, arquivo_novas_palavras)