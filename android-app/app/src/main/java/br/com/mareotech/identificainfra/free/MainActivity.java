package br.com.mareotech.identificainfra.free;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;

import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends Activity {
    private EditText targetInput;
    private CheckBox authCheck;
    private TextView statusText;
    private TextView resultText;
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    private static final int MAX_HOSTS = 256;
    private static final int[] PORTS = {22, 53, 80, 135, 139, 443, 445, 3389, 5985, 8080};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        targetInput = findViewById(R.id.targetInput);
        authCheck = findViewById(R.id.authCheck);
        statusText = findViewById(R.id.statusText);
        resultText = findViewById(R.id.resultText);
        Button scanButton = findViewById(R.id.scanButton);

        targetInput.setText("192.168.1.0/24");
        scanButton.setOnClickListener(v -> startScan());
    }

    private void startScan() {
        if (!authCheck.isChecked()) {
            statusText.setText("Confirme a autorização antes de iniciar.");
            return;
        }

        final List<String> targets;
        try {
            targets = parseTargets(targetInput.getText().toString().trim());
        } catch (Exception e) {
            statusText.setText("Alvo inválido: " + e.getMessage());
            return;
        }

        if (targets.size() > MAX_HOSTS) {
            statusText.setText("FREE limitada a 256 hosts por execução.");
            return;
        }

        resultText.setText("");
        statusText.setText("Mapeando " + targets.size() + " host(s)...");

        executor.submit(() -> {
            StringBuilder out = new StringBuilder();
            int active = 0;

            for (String ip : targets) {
                HostInfo info = probeHost(ip);
                if (info.active) {
                    active++;
                    out.append(info.toLine()).append("\n");
                }
                final String snapshot = out.toString();
                final int done = active;
                runOnUiThread(() -> {
                    resultText.setText(snapshot);
                    statusText.setText("Ativos encontrados: " + done);
                });
            }

            final int totalActive = active;
            runOnUiThread(() -> statusText.setText(
                    "Concluído: " + totalActive + " ativo(s) em " + targets.size() + " analisado(s)."
            ));
        });
    }

    private HostInfo probeHost(String ip) {
        boolean reachable = false;
        try {
            reachable = InetAddress.getByName(ip).isReachable(500);
        } catch (Exception ignored) {}

        List<Integer> open = new ArrayList<>();
        for (int port : PORTS) {
            try (Socket socket = new Socket()) {
                socket.connect(new InetSocketAddress(ip, port), 180);
                open.add(port);
                reachable = true;
            } catch (Exception ignored) {}
        }

        String hostname = "";
        try {
            hostname = InetAddress.getByName(ip).getCanonicalHostName();
            if (hostname.equals(ip)) hostname = "";
        } catch (Exception ignored) {}

        return new HostInfo(ip, reachable, hostname, open);
    }

    private List<String> parseTargets(String value) {
        if (value == null || value.isEmpty()) {
            throw new IllegalArgumentException("informe um IP ou CIDR");
        }

        if (!value.contains("/")) {
            List<String> one = new ArrayList<>();
            one.add(value);
            return one;
        }

        String[] parts = value.split("/");
        if (parts.length != 2) throw new IllegalArgumentException("CIDR inválido");

        String[] oct = parts[0].split("\\.");
        if (oct.length != 4) throw new IllegalArgumentException("IPv4 inválido");

        int prefix = Integer.parseInt(parts[1]);
        if (prefix < 24 || prefix > 32) {
            throw new IllegalArgumentException("na FREE Android use /24 a /32");
        }

        long base = 0;
        for (String o : oct) {
            int n = Integer.parseInt(o);
            if (n < 0 || n > 255) throw new IllegalArgumentException("IPv4 inválido");
            base = (base << 8) | n;
        }

        long mask = prefix == 0 ? 0 : 0xffffffffL << (32 - prefix);
        long network = base & mask;
        long broadcast = network | (~mask & 0xffffffffL);

        List<String> result = new ArrayList<>();
        long start = prefix == 32 ? network : network + 1;
        long end = prefix == 32 ? network : broadcast - 1;

        for (long x = start; x <= end && result.size() < MAX_HOSTS; x++) {
            result.add(((x >> 24) & 255) + "." + ((x >> 16) & 255) + "." + ((x >> 8) & 255) + "." + (x & 255));
        }
        return result;
    }

    private static class HostInfo {
        final String ip;
        final boolean active;
        final String hostname;
        final List<Integer> ports;

        HostInfo(String ip, boolean active, String hostname, List<Integer> ports) {
            this.ip = ip;
            this.active = active;
            this.hostname = hostname;
            this.ports = ports;
        }

        String toLine() {
            return ip + (hostname.isEmpty() ? "" : "  " + hostname) +
                    (ports.isEmpty() ? "" : "  portas=" + ports);
        }
    }
}
