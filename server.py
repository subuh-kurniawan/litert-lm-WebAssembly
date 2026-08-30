#!/usr/bin/env python3
import http.server
import socketserver
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable COOP (Cross-Origin-Opener-Policy) and COEP (Cross-Origin-Embedder-Policy)
        # to support advanced WebAssembly SharedArrayBuffer features if needed
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        
        # Add CORS header just in case models are loaded from other local resources
        self.send_header("Access-Control-Allow-Origin", "*")
        
        # Add Cache-Control for fast local development
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        
        super().end_headers()

if __name__ == "__main__":
    # Custom port check
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print("Port harus berupa angka. Menggunakan port default 8000.")

    Handler = MyHTTPRequestHandler
    
    # Allow address reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"==================================================")
        print(f"🚀 Gemma4 Server Lokal Berhasil Dijalankan!")
        print(f"🔗 Buka di Browser: http://localhost:{PORT}")
        print(f"🔒 Header COOP/COEP Aktif (Diperlukan oleh WebAssembly)")
        print(f"==================================================")
        print("Tekan Ctrl+C untuk menghentikan server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer dihentikan.")
            sys.exit(0)
