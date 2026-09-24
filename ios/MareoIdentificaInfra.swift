import Foundation
import Network

// Mareo Identifica Infra FREE — amostra iOS.
// Por restrições do iOS, esta amostra não enumera a sub-rede livremente.
// Ela testa endpoints explicitamente informados pelo usuário.

struct MareoProbeResult {
    let host: String
    let port: UInt16
    let reachable: Bool
}

final class MareoTCPProbe {
    func test(host: String, port: UInt16, timeoutSeconds: Double = 1.0, completion: @escaping (MareoProbeResult) -> Void) {
        guard let nwPort = NWEndpoint.Port(rawValue: port) else {
            completion(MareoProbeResult(host: host, port: port, reachable: false))
            return
        }
        let connection = NWConnection(host: NWEndpoint.Host(host), port: nwPort, using: .tcp)
        var finished = false
        let finish: (Bool) -> Void = { ok in
            if finished { return }
            finished = true
            connection.cancel()
            completion(MareoProbeResult(host: host, port: port, reachable: ok))
        }
        connection.stateUpdateHandler = { state in
            switch state {
            case .ready: finish(true)
            case .failed(_), .cancelled: finish(false)
            default: break
            }
        }
        connection.start(queue: .global())
        DispatchQueue.global().asyncAfter(deadline: .now() + timeoutSeconds) { finish(false) }
    }
}
