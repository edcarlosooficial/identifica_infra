from __future__ import annotations
import argparse, concurrent.futures, csv, ipaddress, json, os, platform, re, socket, subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

APP_NAME="Mareo Identifica Infra FREE"
APP_VERSION="0.2.0"
MAX_HOSTS=256
COMMON_PORTS=[22,53,80,135,139,443,445,3389,5985,8080]
PORT_NAMES={22:"SSH",53:"DNS",80:"HTTP",135:"MS-RPC",139:"NetBIOS",443:"HTTPS",445:"SMB",3389:"RDP",5985:"WinRM",8080:"HTTP-Alt"}

@dataclass
class HostResult:
    ip:str
    online:bool
    hostname:str=""
    mac:str=""
    ttl:Optional[int]=None
    open_ports:list[int]=field(default_factory=list)
    services:list[str]=field(default_factory=list)
    os_hint:str="Indeterminado"
    diagnosis:list[str]=field(default_factory=list)

def run_cmd(cmd:list[str],timeout:float=5):
    kw=dict(capture_output=True,text=True,errors="replace",timeout=timeout)
    if os.name=="nt": kw["creationflags"]=getattr(subprocess,"CREATE_NO_WINDOW",0)
    return subprocess.run(cmd,**kw)

def parse_targets(value:str)->list[str]:
    value=value.strip()
    if not value: raise ValueError("Informe um IP, CIDR ou faixa.")
    if "/" in value:
        net=ipaddress.ip_network(value,strict=False)
        if net.version!=4: raise ValueError("Amostra FREE suporta IPv4.")
        targets=list(net.hosts())
    elif "-" in value:
        a,b=[x.strip() for x in value.split("-",1)]
        start,end=ipaddress.ip_address(a),ipaddress.ip_address(b)
        if start.version!=4 or end.version!=4 or int(end)<int(start): raise ValueError("Faixa IPv4 inválida.")
        targets=[ipaddress.ip_address(n) for n in range(int(start),int(end)+1)]
    else:
        ip=ipaddress.ip_address(value)
        if ip.version!=4: raise ValueError("Amostra FREE suporta IPv4.")
        targets=[ip]
    if len(targets)>MAX_HOSTS: raise ValueError(f"FREE limitada a {MAX_HOSTS} hosts por execução.")
    return [str(x) for x in targets]

def ping_host(ip:str):
    sys=platform.system().lower()
    if sys=="windows": cmd=["ping","-n","1","-w","700",ip]
    elif sys=="darwin": cmd=["ping","-c","1","-W","1000",ip]
    else: cmd=["ping","-c","1","-W","1",ip]
    try:
        cp=run_cmd(cmd,2.5)
        txt=(cp.stdout or "")+(cp.stderr or "")
        m=re.search(r"ttl[=:\s](\d+)",txt,re.I)
        return cp.returncode==0,(int(m.group(1)) if m else None)
    except Exception:
        return False,None

def tcp_probe(ip:str,ports:Iterable[int],timeout:float=.22)->list[int]:
    opened=[]
    for port in ports:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.settimeout(timeout)
        try:
            if s.connect_ex((ip,port))==0: opened.append(port)
        except OSError: pass
        finally: s.close()
    return opened

def reverse_dns(ip:str)->str:
    try:return socket.gethostbyaddr(ip)[0]
    except Exception:return ""

def arp_mac(ip:str)->str:
    try:
        cp=run_cmd(["arp","-a"],3)
        m=re.search(rf"\b{re.escape(ip)}\b\s+([0-9a-fA-F]{{2}}(?:[:-][0-9a-fA-F]{{2}}){{5}})",cp.stdout or "")
        return m.group(1).replace("-",":").upper() if m else ""
    except Exception:return ""

def os_hint(ttl:Optional[int],ports:list[int])->str:
    p=set(ports)
    if p.intersection({135,139,445,3389,5985}): return "Windows/appliance (heurística)"
    if 22 in p:return "Linux/Unix/appliance (heurística)"
    if ttl is not None:
        if ttl<=64:return "Linux/Unix/appliance (TTL)"
        if ttl<=128:return "Windows/appliance (TTL)"
    return "Indeterminado"

def diagnose(ports:list[int],hostname:str)->list[str]:
    p=set(ports); notes=[]
    if not p: notes.append("Host respondeu; nenhuma porta comum da amostra foi detectada.")
    if p.intersection({80,443,8080}): notes.append("Serviço web detectado.")
    if 445 in p: notes.append("SMB detectado; valide necessidade de exposição no segmento.")
    if 3389 in p: notes.append("RDP detectado; mantenha acesso restrito.")
    if 22 in p: notes.append("SSH detectado.")
    if hostname: notes.append(f"Nome resolvido: {hostname}.")
    return notes

def scan_one(ip:str)->HostResult:
    online,ttl=ping_host(ip)
    ports=tcp_probe(ip,COMMON_PORTS)
    if ports: online=True
    if not online:return HostResult(ip=ip,online=False)
    host=reverse_dns(ip); mac=arp_mac(ip)
    return HostResult(ip=ip,online=True,hostname=host,mac=mac,ttl=ttl,open_ports=ports,
                      services=[PORT_NAMES[p] for p in ports],os_hint=os_hint(ttl,ports),
                      diagnosis=diagnose(ports,host))

def scan(target:str)->list[HostResult]:
    targets=parse_targets(target)
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(32,max(4,len(targets)))) as ex:
        for r in ex.map(scan_one,targets): results.append(r)
    return sorted(results,key=lambda r:ipaddress.ip_address(r.ip))

def export_json(results:list[HostResult],path:str):
    payload={"app":APP_NAME,"version":APP_VERSION,"generated_at":datetime.now().isoformat(timespec="seconds"),"hosts":[asdict(r) for r in results]}
    Path(path).write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding="utf-8")

def export_csv(results:list[HostResult],path:str):
    with open(path,"w",newline="",encoding="utf-8-sig") as f:
        w=csv.writer(f,delimiter=";")
        w.writerow(["ip","online","hostname","mac","ttl","os_hint","open_ports","services","diagnosis"])
        for r in results:w.writerow([r.ip,r.online,r.hostname,r.mac,r.ttl or "",r.os_hint,",".join(map(str,r.open_ports)),",".join(r.services)," | ".join(r.diagnosis)])

def main():
    ap=argparse.ArgumentParser(description="Mareo Identifica Infra FREE — mapeamento leve e autorizado de rede.")
    ap.add_argument("target",help="IP, CIDR ou faixa IPv4")
    ap.add_argument("--json",dest="json_path")
    ap.add_argument("--csv",dest="csv_path")
    args=ap.parse_args()
    print("Mareo Tecnologia | Identifica Infra FREE")
    print("Use somente em redes próprias ou autorizadas.")
    results=scan(args.target)
    for r in results:
        if r.online:
            print(f"[UP] {r.ip:15} {r.hostname or '-':28} {r.os_hint:30} {','.join(r.services) or '-'}")
    print(f"\nAtivos: {sum(r.online for r in results)}/{len(results)}")
    if args.json_path: export_json(results,args.json_path)
    if args.csv_path: export_csv(results,args.csv_path)

if __name__=="__main__": main()
