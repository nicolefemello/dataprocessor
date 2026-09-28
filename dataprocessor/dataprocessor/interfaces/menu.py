from ..infra.fontes import FonteDadosArquivos
from ..infra.relatorios import criar_gerador
from ..services.processamento import executar_processamento


def processar_caminhos(caminho_clientes, caminho_transacoes, caminho_config):
    fonte = FonteDadosArquivos(caminho_clientes, caminho_transacoes, caminho_config)
    return executar_processamento(fonte)

def processar():
    caminho_clientes = input("Caminho do CSV de clientes [data/clientes.csv]: ").strip() or "data/clientes.csv"
    caminho_transacoes = input("Caminho do CSV de transações [data/transacoes.csv]: ").strip() or "data/transacoes.csv"
    caminho_config = input("Caminho do JSON de config [data/config.json]: ").strip() or "data/config.json"

    try:
        resultado = processar_caminhos(caminho_clientes, caminho_transacoes, caminho_config)
    except (OSError, ValueError, KeyError) as erro:
        print(f"[ERRO] Não foi possível processar: {erro}")
        return None
    print(f"Clientes válidos: {len(resultado.clientes)}")
    print(f"Transações válidas: {len(resultado.transacoes)}")
    return resultado

def exibir_relatorio(resultado, formato_padrao):
    formatos = {"texto", "json", "csv"}
    formato = input(f"Formato (texto/json/csv) [{formato_padrao}]: ").strip() or formato_padrao
    if formato not in formatos:
        print(f"Formato inválido: '{formato}'.")
        return
    gerador = criar_gerador(formato)
    print(gerador.render(resultado))
    return formato