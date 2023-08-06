import requests
import logging
import socket
from tabulate import tabulate
from pprint import pprint
from ..utils import dumps, abort
from P4 import P4
log = logging.getLogger(__name__)

from typer import Context, launch, echo, secho, Option, Typer, confirm, prompt, style

app = Typer()


@app.command()
def init():
    cmd = """
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "SN2" -Value "subst S: D:\\Perforce\\SN2"
    """

@app.command()
def info():
    p4 = P4()
    # p4.port = "ssl:perforce.unknownworlds.com:1666"
    # p4.user = "jonb"
    # p4.client = "jonb_work_sn2-main"
    p4.connect()
    try:
        ret = p4.run_clients("-u", p4.user)
    except Exception as e:
        if "P4PASSWD" in str(e):
            abort("Please log into perforce with p4 login")
    rows = []
    for r in ret:
        h = r["Host"]
        if h.lower() == socket.gethostname().lower():
            h = style(h, bold=True)
        else:
            h = style(h, fg="red")
        rows.append([r["client"], r["Stream"], r["Root"], h])
    tbl = tabulate(rows, headers=["Client", "Stream", "Root", "Host"])
    echo(tbl)
