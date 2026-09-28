import argparse
import logging
import os
from pathlib import Path

from .infra.fontes import FonteDadosArquivos
from .infra.relatorios import criar_gerador
from .services.processamento import executar_processamento
from .interfaces.menu import processar, exibir_relatorio


def configurar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Processa clientes e transações.")
    parser.add_argument("--clientes", required=False, help="Caminho do CSV de clientes.", default="data/clientes.csv")
    parser.add_argument("--transacoes", required=False, help="Caminho do CSV de transações.", default="data/transacoes.csv")
    parser.add_argument("--config", required=False, help="Caminho do JSON de configuração.", default="data/conifg.csv")
    parser.add_argument("--formato", choices=("texto", "json", "csv"), default="texto")
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--menu", default=False)
    return parser


def menu() -> int:
    resultado = None
    formato_relatorio = "texto"
    while True:
        print("\n=== DataProcessor — Menu ===")
        print("1. Processar dados")
        print("2. Exibir relatório")
        print("3. Sair")
        opcao = input("Escolha uma opção: ").strip()
        os.system("cls" if os.name == "nt" else "clear")

        if opcao == "1":
            resultado = processar()
        elif opcao == "2":
            if resultado is None:
                print("Nenhum dado processado. Escolha a opção 1 primeiro.")
                continue
            formato_relatorio = exibir_relatorio(resultado, formato_relatorio)
        elif opcao == "3":
            break
        else:
            print(f"Opção inválida: {opcao}. Escolha 1, 2 ou 3.")
            continue
    return 1

def main(argv: list[str] | None = None) -> int:
    args = configurar_parser().parse_args(argv)
    if args.menu:
        menu()
        return 1
    args.output.mkdir(parents=True, exist_ok=True)
    log_path = args.output / "dataprocessor.log"
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logging.info("Iniciando processamento")
    try:
        fonte = FonteDadosArquivos(args.clientes, args.transacoes, args.config)
        resultado = executar_processamento(fonte)
        relatorio = criar_gerador(args.formato).render(resultado)
        nome = "relatorio.txt" if args.formato == "texto" else f"relatorio.{args.formato}"
        (args.output / nome).write_text(relatorio, encoding="utf-8")
        logging.info(
            "Processamento concluído: %d clientes e %d transações válidos",
            len(resultado.clientes),
            len(resultado.transacoes),
        )
        print(relatorio, end="")
        return 0
    except (OSError, ValueError, KeyError) as erro:
        logging.exception("Falha no processamento")
        print(f"[ERRO] {erro}")
        return 1