import json, threading, tkinter as tk
from dataclasses import asdict
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from mareo_mapper import APP_NAME, APP_VERSION, parse_targets, scan

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} — {APP_VERSION}")
        self.geometry("960x620")
        self.configure(bg="#0B1F33")
        self.results=[]
        side=tk.Frame(self,bg="#0B1F33",width=250); side.pack(side="left",fill="y"); side.pack_propagate(False)
        cv=tk.Canvas(side,width=220,height=80,bg="#0B1F33",highlightthickness=0); cv.pack(pady=(24,8))
        cv.create_line(38,14,38,50,fill="#22B8C7",width=2)
        cv.create_polygon(35,16,18,43,35,39,fill="#22B8C7")
        cv.create_polygon(41,16,60,41,41,37,fill="#4CA7D8")
        cv.create_polygon(18,47,61,47,54,54,27,54,fill="#B58A45")
        cv.create_text(82,31,text="MAREO",anchor="w",fill="white",font=("Segoe UI",19,"bold"))
        cv.create_text(83,50,text="TECNOLOGIA",anchor="w",fill="#22B8C7",font=("Segoe UI",8,"bold"))
        tk.Label(side,text="IDENTIFICA INFRA FREE",bg="#0B1F33",fg="#B58A45",font=("Segoe UI",9,"bold")).pack(anchor="w",padx=24)
        tk.Label(side,text="Mapeamento simples da rede.\nAmostra pública.\n\nLimite: 256 hosts.",justify="left",bg="#0B1F33",fg="#CBD9E2").pack(anchor="w",padx=24,pady=10)

        main=tk.Frame(self,bg="#F4F7F8"); main.pack(side="left",fill="both",expand=True)
        tk.Label(main,text="Diagnóstico rápido de rede",bg="#F4F7F8",fg="#0B1F33",font=("Segoe UI",18,"bold")).pack(anchor="w",padx=24,pady=(24,4))
        tk.Label(main,text="Informe IP, faixa ou CIDR. Use somente com autorização.",bg="#F4F7F8",fg="#647784").pack(anchor="w",padx=24)
        row=tk.Frame(main,bg="#F4F7F8"); row.pack(fill="x",padx=24,pady=15)
        self.target=tk.StringVar(value="192.168.1.0/24")
        tk.Entry(row,textvariable=self.target,font=("Consolas",11)).pack(side="left",fill="x",expand=True)
        tk.Button(row,text="Analisar",command=self.start).pack(side="right",padx=(10,0))
        self.tree=ttk.Treeview(main,columns=("ip","status","hostname","mac","os","services"),show="headings")
        for col,label,w in [("ip","IP",110),("status","Status",70),("hostname","Hostname",170),("mac","MAC",135),("os","SO (indício)",190),("services","Serviços",170)]:
            self.tree.heading(col,text=label); self.tree.column(col,width=w,anchor="w")
        self.tree.pack(fill="both",expand=True,padx=24)
        bottom=tk.Frame(main,bg="#F4F7F8"); bottom.pack(fill="x",padx=24,pady=12)
        self.status=tk.StringVar(value="Pronto.")
        tk.Label(bottom,textvariable=self.status,bg="#F4F7F8",fg="#647784").pack(side="left")
        tk.Button(bottom,text="Exportar JSON",command=self.export_json).pack(side="right")

    def start(self):
        try: count=len(parse_targets(self.target.get()))
        except Exception as e: messagebox.showerror(APP_NAME,str(e)); return
        if not messagebox.askyesno(APP_NAME,f"Você confirma autorização para analisar {count} host(s)?"): return
        for x in self.tree.get_children(): self.tree.delete(x)
        self.status.set("Analisando...")
        threading.Thread(target=self.worker,daemon=True).start()

    def worker(self):
        try:
            self.results=scan(self.target.get())
            for r in self.results:
                self.after(0,self.tree.insert,"","end",values=(r.ip,"ATIVO" if r.online else "-",r.hostname,r.mac,r.os_hint if r.online else "",",".join(r.services)))
            self.after(0,self.status.set,f"Concluído: {sum(r.online for r in self.results)} ativo(s) / {len(self.results)}.")
        except Exception as e:self.after(0,messagebox.showerror,APP_NAME,str(e))

    def export_json(self):
        if not self.results:return
        path=filedialog.asksaveasfilename(defaultextension=".json",initialfile="mareo_identifica_infra_free.json")
        if path: Path(path).write_text(json.dumps([asdict(r) for r in self.results],indent=2,ensure_ascii=False),encoding="utf-8")

if __name__=="__main__": App().mainloop()
