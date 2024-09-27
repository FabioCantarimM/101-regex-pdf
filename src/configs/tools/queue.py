import json
import os
import re
import urllib.parse

from configs.rules.notas import rules_dict
from configs.tools.aws.sqs import AWSSQSManager
from table_pdf_extractor import PDFTableExtractor
from text_pdf_extractor import PDFTextExtractor


class HTMLSQSListener:
    def __init__(self):
        self.queue = os.getenv("QUEUE_NAME")
        self.sqs = AWSSQSManager()

    def check_messages(self):
        has_message = self.sqs.check_message_in_queue(self.queue)
        if has_message:
            messages = self.sqs.receive_messages_from_queue(self.queue)

            for message in messages:
                receipt_handle = message["ReceiptHandle"]
                json_body = json.loads(message["Body"])
                object_key = json_body["Records"][0]["s3"]["object"]["key"]
                object_key_unquote = urllib.parse.unquote(object_key)
                object_key_final = re.sub(r"\+(?=\()", " ", object_key_unquote)

                try:
                    print("oi")
                    resultTxt = PDFTextExtractor(object_key_final).start()
                    resultImg = PDFTableExtractor(
                        object_key_final, configs=rules_dict["jornada"]
                    ).start()
                except Exception as e:
                    self.sqs.delete_message_from_queue(self.queue, receipt_handle)
                    raise (e)
                if resultTxt & resultImg:
                    print("Tarefa Processada com sucesso")
                else:
                    print("Tarefa Processada sem sucesso")
                self.sqs.delete_message_from_queue(self.queue, receipt_handle)
