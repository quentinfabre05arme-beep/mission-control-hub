"""
Start ngrok tunnel for dashboard access
"""
from pyngrok import ngrok
import subprocess
import time
import os

def start_server():
    """Start the HTTP server"""
    print("Starting HTTP server on port 9000...")
    # Server should already be running, but just in case
    try:
        import http.server
        import socketserver
        
        os.chdir('C:\\Users\\quent\\.openclaw\\workspace')
        
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", 9000), handler)
        
        import threading
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print("✅ Server started")
        return httpd
    except Exception as e:
        print(f"Server may already be running: {e}")
        return None

def start_ngrok():
    """Start ngrok tunnel"""
    print("\n🌐 Starting ngrok tunnel...")
    print("=" * 50)
    
    try:
        # Connect ngrok to port 9000
        public_url = ngrok.connect(9000, "http")
        
        print(f"✅ SUCCESS!")
        print(f"\n📱 Your dashboard is now accessible at:")
        print(f"   {public_url}")
        print(f"   {public_url}/mission_control_hub.html")
        
        print(f"\n🔗 Local access:")
        print(f"   http://localhost:9000/mission_control_hub.html")
        
        print(f"\n⚠️  This URL is temporary.")
        print(f"   It will change if you restart ngrok.")
        
        print(f"\n📲 Open the URL on your phone now!")
        print("=" * 50)
        
        # Keep running
        print("\nPress Ctrl+C to stop the tunnel")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nStopping ngrok...")
            ngrok.disconnect(public_url)
            ngrok.kill()
            print("✅ Tunnel closed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nYou may need to:")
        print("1. Sign up at https://ngrok.com")
        print("2. Add your auth token: ngrok authtoken YOUR_TOKEN")

if __name__ == '__main__':
    print("=" * 50)
    print("Mission Control - Mobile Access Setup")
    print("=" * 50)
    
    server = start_server()
    start_ngrok()
