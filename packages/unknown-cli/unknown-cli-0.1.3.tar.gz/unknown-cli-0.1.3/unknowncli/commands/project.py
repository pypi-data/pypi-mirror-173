import requests
import logging
import socket
from tabulate import tabulate
from pprint import pprint
from ..utils import dumps
from P4 import P4
log = logging.getLogger(__name__)

from typer import Context, launch, echo, secho, Option, Typer, confirm, prompt, style

app = Typer()


@app.command()
def info():
    p4 = P4()
    # p4.port = "ssl:perforce.unknownworlds.com:1666"
    # p4.user = "jonb"
    # p4.client = "jonb_work_sn2-main"
    p4.connect()
    ret = p4.run_clients("-u", p4.user)
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
