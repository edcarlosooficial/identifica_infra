import SwiftUI

@main
struct MareoIdentificaInfraFREEApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    @State private var host = ""
    @State private var port = "443"
    @State private var status = "Informe um host e uma porta."
    @State private var running = false

    var body: some View {
        NavigationStack {
            Form {
                Section("Diagnóstico autorizado") {
                    TextField("Host ou IP", text: $host)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled()
                    TextField("Porta", text: $port)
                        .keyboardType(.numberPad)

                    Button(running ? "Testando..." : "Testar conectividade TCP") {
                        runProbe()
                    }
                    .disabled(running || host.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                }

                Section("Resultado") {
                    Text(status)
                }

                Section("Mareo Tecnologia") {
                    Text("Identifica Infra FREE")
                    Text("A versão iOS testa somente endpoints explicitamente informados. O iOS não permite varredura irrestrita de sub-rede por um app comum.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Mareo Infra FREE")
        }
    }

    private func runProbe() {
        guard let value = UInt16(port), !host.isEmpty else {
            status = "Host ou porta inválidos."
            return
        }
        running = true
        status = "Testando..."
        MareoTCPProbe().test(host: host, port: value) { result in
            DispatchQueue.main.async {
                running = false
                status = result.reachable
                    ? "\(result.host):\(result.port) acessível por TCP."
                    : "\(result.host):\(result.port) não respondeu ao teste TCP."
            }
        }
    }
}
