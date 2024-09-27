import logging
import os
import re

import pandas as pd
import PyPDF2

from configs.tools.aws.s3 import AWSS3
from configs.tools.postgre import RDSPostgreSQLManager

logging.basicConfig(level=logging.INFO)


class PDFTextExtractor:
    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path
        self.extracted_text = ""
        self.aws = AWSS3()

    def start(self):
        try:
            t = self.extract_text()
            df = self.text_to_dataframe(t)
            self.send_to_db(df, "pdf_text")
            return True
        except Exception as e:
            print(e)
            return False

    def extract_text(self):
        self.download_file()
        # Abrir o arquivo PDF em modo de leitura binária
        with open(f"download/{self.pdf_file_path}", "rb") as file:
            # Criar um objeto leitor de PDF
            pdf_reader = PyPDF2.PdfReader(file)

            extracted_text = ""

            # Iterar por todas as páginas do PDF
            for page_num in range(len(pdf_reader.pages)):
                # Obter a página atual
                page = pdf_reader.pages[page_num]
                # Extrair texto da página e adicionar ao texto extraído
                extracted_text += page.extract_text()

        extracted_text = self.extract_operations(extracted_text)
        extracted_text = self.split_text_by_newline(extracted_text)

        return extracted_text

    def split_text_by_newline(self, text):
        # Divide o texto por '\n' e retorna como uma lista de strings
        if text:
            return text.split("\n")
        else:
            return []

    def extract_operations(self, texto):
        # Regex para capturar tudo de "C/V" até "Posição Ajuste"
        pattern = r"(C/V.*?)(?=\nPosição Ajuste)"

        # Encontrar o trecho do texto
        resultado = re.search(pattern, texto, re.DOTALL)

        if resultado:
            return resultado.group(1)
        else:
            return "Padrão não encontrado."

    def text_to_dataframe(self, texto_operacoes):
        # Extrair o cabeçalho e os dados das operações
        cabecalho = texto_operacoes[0].split()  # Primeira linha contém o cabeçalho
        dados = [
            linha.split() for linha in texto_operacoes[1:] if linha
        ]  # As demais são dados

        # Criar o DataFrame
        df = pd.DataFrame(dados, columns=cabecalho)

        return df

    def get_text(self):
        t = self.extract_text()
        # Retorna o texto extraído
        return t

    def get_df(self):
        df = self.get_text()
        return self.text_to_dataframe(df)

    def download_file(self):
        bucket = os.getenv("AWS_BUCKET")
        if not os.path.exists("download"):
            os.makedirs("download", exist_ok=True)
        return self.aws.download_file_from_s3(
            bucket, self.pdf_file_path, f"download/{self.pdf_file_path}"
        )

    def send_to_db(self, df, table_name):
        try:
            connection = RDSPostgreSQLManager().alchemy()
            df.to_sql(table_name, connection, if_exists="append", index=False)
            logging.info(f"Success to save into {table_name}")
            os.remove(f"download/{self.pdf_file_path}")
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    # Exemplo de uso
    pdf_path = "src/files/pdf/jornada/corretora_jornada_de_dados (1).pdf"
    pdf_extractor = PDFTextExtractor(pdf_path)
    t = pdf_extractor.get_text()
    df = pdf_extractor.get_df()
    pdf_extractor.send_to_db(df, "pdf_text")
    print(t)
