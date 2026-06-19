from dotenv import load_dotenv
import os

load_dotenv()

SIP_URL = os.getenv("SIP_URL")
SIP_USUARIO = os.getenv("SIP_USUARIO")
SIP_SENHA = os.getenv("SIP_SENHA")
SIP_ORGAO = os.getenv("SIP_ORGAO", "PCPE")