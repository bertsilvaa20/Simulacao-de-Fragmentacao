class SimuladorDisco:
    def __init__(self, total_blocos=16, tamanho_bloco_kb=4):
        self.total_blocos = total_blocos
        self.tamanho_bloco_kb = tamanho_bloco_kb
        self.disco = ["-"] * total_blocos
        self.arquivos = {}  

    def exibir_disco(self):
        print("\nEstado Atual do Disco:")
        print(" | ".join(self.disco))
        self.calcular_metricas()

    def adicionar_arquivo(self, nome, tamanho_kb):
        
        blocos_necessarios = (tamanho_kb + self.tamanho_bloco_kb - 1) // self.tamanho_bloco_kb
        
        
        blocos_livres_encontrados = []
        for i in range(self.total_blocos):
            if self.disco[i] == "-":
                blocos_livres_encontrados.append(i)
                if len(blocos_livres_encontrados) == blocos_necessarios:
                    break

        
        if len(blocos_livres_encontrados) < blocos_necessarios:
            print(f"\n[ERRO] Não há espaço para o arquivo '{nome}' ({tamanho_kb} KB).")
            return False

        
        for bloco in blocos_livres_encontrados:
            self.disco[bloco] = nome
            
        self.arquivos[nome] = (blocos_livres_encontrados, tamanho_kb)
        print(f"\n[SUCESSO] Arquivo '{nome}' alocado nos blocos: {blocos_livres_encontrados}")
        self.exibir_disco()
        return True
    
    def remover_arquivo(self, nome):
        if nome not in self.arquivos:
            print(f"\n[ERRO] Arquivo '{nome}' não encontrado.")
            return False

        blocos_alocados, _ = self.arquivos[nome]
        for bloco in blocos_alocados:
            self.disco[bloco] = "-"
            
        del self.arquivos[nome]
        print(f"\n[SUCESSO] Arquivo '{nome}' removido. Blocos {blocos_alocados} liberados!")
        self.exibir_disco()
        return True

    def calcular_metricas(self):
        frag_interna_total = 0
        total_saltos = 0
        
        
        for nome, (blocos, tamanho_real) in self.arquivos.items():
            espaco_alocado_kb = len(blocos) * self.tamanho_bloco_kb
            frag_interna_arquivo = espaco_alocado_kb - tamanho_real
            frag_interna_total += frag_interna_arquivo
            
            
            saltos = 0
            for i in range(len(blocos) - 1):
                if blocos[i+1] != blocos[i] + 1:
                    saltos += 1
            total_saltos += saltos

        
        blocos_livres = self.disco.count("-")
        maior_espaco_continuo = 0
        corrente_atual = 0
        for bloco in self.disco:
            if bloco == "-":
                corrente_atual += 1
                if corrente_atual > maior_espaco_continuo:
                    maior_espaco_continuo = corrente_atual
            else:
                corrente_atual = 0
                
        frag_externa = blocos_livres - maior_espaco_continuo

        print(f"--> Fragmentação Interna Total: {frag_interna_total} KB")
        print(f"--> Fragmentação Externa (Espaço desperdiçado não-contíguo): {frag_externa * self.tamanho_bloco_kb} KB")
        print(f"--> penalidade no Tempo de Acesso (Total de fragmentações/saltos): {total_saltos} saltos do cabeçote")


# teste prático
if __name__ == "__main__":
    
    simulador = SimuladorDisco(total_blocos=16, tamanho_bloco_kb=4)
    simulador.exibir_disco()

    
    simulador.adicionar_arquivo("A", 5)  
    simulador.adicionar_arquivo("B", 8)  
    simulador.adicionar_arquivo("C", 12) 

    # simulando movimento do cabeçote

    simulador.remover_arquivo("B")
    simulador.adicionar_arquivo("D", 11)

    ## simulando FRAGMENTAÇÃO EXTERNA

    # simulador.adicionar_arquivo("A", 8)  
    # simulador.adicionar_arquivo("B", 8)  
    # simulador.adicionar_arquivo("C", 8)  
    # simulador.adicionar_arquivo("D", 8)  
    # simulador.adicionar_arquivo("E", 32) 

    # simulador.remover_arquivo("B") 
    # simulador.remover_arquivo("D") 