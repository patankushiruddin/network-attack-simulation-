import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Canvas
import threading
import time
import random
import socket
import struct
from datetime import datetime
import json
from collections import deque
import math

class ModernNetworkAttackSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Network Attack Simulator - Educational Tool")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e1e')
        
        # Modern color scheme
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#0078d4',
            'success': '#107c10',
            'warning': '#ff8c00',
            'danger': '#d13438',
            'panel': '#252526',
            'border': '#3e3e42',
            'text_secondary': '#cccccc'
        }
        
        # Attack variables
        self.is_attacking = False
        self.attack_thread = None
        self.packet_log = deque(maxlen=1000)
        self.traffic_data = deque(maxlen=50)
        self.attack_stats = {'dos': 0, 'spoof': 0, 'total': 0}
        
        # History tracking
        self.operation_history = deque(maxlen=500)  # Store last 500 operations
        
        # Create GUI
        self.create_modern_widgets()
        
        # Start update loop
        self.update_display()
        
    def create_modern_widgets(self):
        # Main container with modern styling
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title Bar
        title_frame = tk.Frame(main_frame, bg=self.colors['panel'], height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🔐 NETWORK ATTACK SIMULATOR", 
                               font=('Segoe UI', 20, 'bold'), 
                               bg=self.colors['panel'], fg=self.colors['accent'])
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame, text="Educational Tool for Understanding Network Security", 
                                 font=('Segoe UI', 10), 
                                 bg=self.colors['panel'], fg=self.colors['text_secondary'])
        subtitle_label.pack()
        
        # Content Area
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left Panel - Controls
        left_panel = tk.Frame(content_frame, bg=self.colors['panel'], width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # DoS Attack Section
        self.create_dos_section(left_panel)
        
        # IP Spoofing Section
        self.create_spoof_section(left_panel)
        
        # Network Map Button
        self.create_map_button(left_panel)
        
        # Right Panel - Visualization
        right_panel = tk.Frame(content_frame, bg=self.colors['panel'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Traffic Visualization
        self.create_traffic_viz(right_panel)
        
        # Packet Log
        self.create_packet_log(right_panel)
        
        # Status Bar
        self.create_status_bar(main_frame)
        
    def create_dos_section(self, parent):
        dos_frame = tk.LabelFrame(parent, text="🚨 DoS Attack Simulation", 
                                 font=('Segoe UI', 12, 'bold'),
                                 bg=self.colors['panel'], fg=self.colors['fg'],
                                 relief=tk.FLAT, bd=2)
        dos_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Configure grid
        for i in range(6):
            dos_frame.grid_rowconfigure(i, pad=5)
        dos_frame.grid_columnconfigure(1, weight=1)
        
        # Target IP
        tk.Label(dos_frame, text="Target IP:", bg=self.colors['panel'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.dos_target_ip = tk.Entry(dos_frame, bg='#2d2d30', fg=self.colors['fg'],
                                     insertbackground=self.colors['fg'], relief=tk.FLAT)
        self.dos_target_ip.grid(row=0, column=1, sticky=tk.EW, padx=(0, 10), pady=5)
        self.dos_target_ip.insert(0, "192.168.1.100")
        
        # Target Port
        tk.Label(dos_frame, text="Target Port:", bg=self.colors['panel'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.dos_target_port = tk.Entry(dos_frame, bg='#2d2d30', fg=self.colors['fg'],
                                       insertbackground=self.colors['fg'], relief=tk.FLAT)
        self.dos_target_port.grid(row=1, column=1, sticky=tk.EW, padx=(0, 10), pady=5)
        self.dos_target_port.insert(0, "80")
        
        # Packet Rate
        tk.Label(dos_frame, text="Packet Rate:", bg=self.colors['panel'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.dos_packet_rate = tk.Scale(dos_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                                        bg=self.colors['panel'], fg=self.colors['fg'],
                                        troughcolor='#2d2d30', activebackground=self.colors['accent'],
                                        highlightthickness=0, relief=tk.FLAT)
        self.dos_packet_rate.grid(row=2, column=1, sticky=tk.EW, padx=(0, 10), pady=5)
        self.dos_packet_rate.set(50)
        
        # Attack Button
        self.dos_button = tk.Button(dos_frame, text="▶️ START DoS ATTACK", 
                                   command=self.toggle_dos_attack,
                                   bg=self.colors['danger'], fg='white',
                                   font=('Segoe UI', 11, 'bold'),
                                   relief=tk.FLAT, pady=10)
        self.dos_button.grid(row=3, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=5)
        
        # Reset Button
        self.reset_button = tk.Button(dos_frame, text="🔄 RESET ALL", 
                                     command=self.reset_all,
                                     bg=self.colors['text_secondary'], fg='white',
                                     font=('Segoe UI', 10, 'bold'),
                                     relief=tk.FLAT, pady=8)
        self.reset_button.grid(row=4, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=5)
        
        # Attack Status
        self.dos_status = tk.Label(dos_frame, text="Status: Ready", 
                                  bg=self.colors['panel'], fg=self.colors['text_secondary'],
                                  font=('Segoe UI', 9))
        self.dos_status.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=10)
        
    def create_spoof_section(self, parent):
        spoof_frame = tk.LabelFrame(parent, text="🎭 IP Spoofing Simulation", 
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=self.colors['panel'], fg=self.colors['fg'],
                                   relief=tk.FLAT, bd=2)
        spoof_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Configure grid
        for i in range(6):
            spoof_frame.grid_rowconfigure(i, pad=5)
        spoof_frame.grid_columnconfigure(1, weight=1)
        
        # Target IP
        tk.Label(spoof_frame, text="Target IP:", bg=self.colors['panel'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.spoof_target_ip = tk.Entry(spoof_frame, bg='#2d2d30', fg=self.colors['fg'],
                                       insertbackground=self.colors['fg'], relief=tk.FLAT)
        self.spoof_target_ip.grid(row=0, column=1, sticky=tk.EW, padx=(0, 10), pady=5)
        self.spoof_target_ip.insert(0, "192.168.1.100")
        
        # Spoofed IP
        tk.Label(spoof_frame, text="Spoofed IP:", bg=self.colors['panel'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.spoof_source_ip = tk.Entry(spoof_frame, bg='#2d2d30', fg=self.colors['fg'],
                                       insertbackground=self.colors['fg'], relief=tk.FLAT)
        self.spoof_source_ip.grid(row=1, column=1, sticky=tk.EW, padx=(0, 10), pady=5)
        self.spoof_source_ip.insert(0, "10.0.0.1")
        
                # Message
        tk.Label(spoof_frame, text="Message:", bg=self.colors['panel'], fg=self.colors['fg'],
                font=('Segoe UI', 10)).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.spoof_message = tk.Entry(spoof_frame, bg='#2d2d30', fg=self.colors['fg'],
                                     insertbackground=self.colors['fg'], relief=tk.FLAT)
        self.spoof_message.grid(row=2, column=1, sticky=tk.EW, padx=(0, 10), pady=5)
        self.spoof_message.insert(0, "Hello from spoofed IP!")
        
        # Send Button
        self.spoof_button = tk.Button(spoof_frame, text="📤 SEND SPOOFED PACKET", 
                                     command=self.send_spoofed_packet,
                                     bg=self.colors['warning'], fg='white',
                                     font=('Segoe UI', 11, 'bold'),
                                     relief=tk.FLAT, pady=10)
        self.spoof_button.grid(row=3, column=0, columnspan=2, sticky=tk.EW, padx=10, pady=10)
        
    def create_map_button(self, parent):
        """Create the Network Map and Cryption buttons section"""
        map_frame = tk.LabelFrame(parent, text="🗺️ Network Tools", 
                                font=('Segoe UI', 12, 'bold'),
                                bg=self.colors['panel'], fg=self.colors['fg'],
                                relief=tk.FLAT, bd=2)
        map_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Buttons container
        buttons_frame = tk.Frame(map_frame, bg=self.colors['panel'])
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Network Map Button
        self.map_button = tk.Button(buttons_frame, text="🗺️ NETWORK MAP", 
                                  command=self.open_network_map_window,
                                  bg=self.colors['success'], fg='white',
                                  font=('Segoe UI', 10, 'bold'),
                                  relief=tk.FLAT, pady=12)
        self.map_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 2))
        
        # Cryption Button
        self.cryption_button = tk.Button(buttons_frame, text="🔐 CRYPTION", 
                                       command=self.open_cryption_window,
                                       bg=self.colors['accent'], fg='white',
                                       font=('Segoe UI', 10, 'bold'),
                                       relief=tk.FLAT, pady=12)
        self.cryption_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2)
        
        # History Button
        self.history_button = tk.Button(buttons_frame, text="📜 HISTORY", 
                                     command=self.open_history_window,
                                     bg=self.colors['warning'], fg='white',
                                     font=('Segoe UI', 10, 'bold'),
                                     relief=tk.FLAT, pady=12)
        self.history_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(2, 0))
        
        # Info Label
        info_label = tk.Label(map_frame, text="Network tools, encryption & history tracking", 
                            bg=self.colors['panel'], fg=self.colors['text_secondary'],
                            font=('Segoe UI', 9), justify=tk.CENTER)
        info_label.pack(pady=(0, 10))
        
    def create_traffic_viz(self, parent):
        viz_frame = tk.LabelFrame(parent, text="📈 Traffic Visualization", 
                                 font=('Segoe UI', 12, 'bold'),
                                 bg=self.colors['panel'], fg=self.colors['fg'],
                                 relief=tk.FLAT, bd=2)
        viz_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Create canvas for bar chart
        self.chart_canvas = Canvas(viz_frame, height=250, bg='#2d2d30', highlightthickness=0)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_packet_log(self, parent):
        log_frame = tk.LabelFrame(parent, text="📋 Packet Log", 
                                 font=('Segoe UI', 12, 'bold'),
                                 bg=self.colors['panel'], fg=self.colors['fg'],
                                 relief=tk.FLAT, bd=2)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create frame for treeview and scrollbar
        tree_frame = tk.Frame(log_frame, bg=self.colors['panel'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview with modern styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Modern.Treeview", 
                       background='#2d2d30',
                       foreground=self.colors['fg'],
                       fieldbackground='#2d2d30',
                       borderwidth=0,
                       font=('Consolas', 9))
        style.configure("Modern.Treeview.Heading",
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        columns = ('Time', 'Type', 'Source', 'Destination', 'Info')
        self.packet_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', 
                                       height=12, style="Modern.Treeview")
        
        for col in columns:
            self.packet_tree.heading(col, text=col)
            self.packet_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.packet_tree.yview)
        self.packet_tree.configure(yscrollcommand=scrollbar.set)
        
        self.packet_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_status_bar(self, parent):
        status_frame = tk.Frame(parent, bg=self.colors['panel'], height=30)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("✅ Ready - Educational Tool Only")
        self.status_label = tk.Label(status_frame, textvariable=self.status_var, 
                                    bg=self.colors['panel'], fg=self.colors['success'],
                                    font=('Segoe UI', 10))
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        # Clock
        self.clock_var = tk.StringVar()
        self.clock_label = tk.Label(status_frame, textvariable=self.clock_var, 
                                   bg=self.colors['panel'], fg=self.colors['text_secondary'],
                                   font=('Segoe UI', 10))
        self.clock_label.pack(side=tk.RIGHT, padx=15, pady=5)
        
        # About Button
        self.about_button = tk.Button(status_frame, text="📚 About", 
                                     command=self.open_about_window,
                                     bg=self.colors['accent'], fg='white',
                                     font=('Segoe UI', 9, 'bold'),
                                     relief=tk.FLAT, padx=15, pady=3)
        self.about_button.pack(side=tk.RIGHT, padx=(0, 15), pady=5)
        self.update_clock()
        
    def update_clock(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_var.set(f"🕐 {current_time}")
        self.root.after(1000, self.update_clock)
        
    def toggle_dos_attack(self):
        if not self.is_attacking:
            self.start_dos_attack()
        else:
            self.stop_attack()
            
    def start_dos_attack(self):
        try:
            target_ip = self.dos_target_ip.get()
            target_port = int(self.dos_target_port.get())
            packet_rate = int(self.dos_packet_rate.get())
            
            if not target_ip or not target_port:
                messagebox.showerror("Error", "Please enter valid target IP and port")
                return
                
            self.is_attacking = True
            self.dos_button.config(text="⏸️ STOP DoS ATTACK", bg=self.colors['success'])
            self.dos_status.config(text="Status: Attacking...", fg=self.colors['danger'])
            self.status_var.set(f"🚨 DoS Attack Running - Target: {target_ip}:{target_port}")
            
            # Add to history
            self.add_to_history("Start DoS", "DoS", f"Target: {target_ip}:{target_port}, Rate: {packet_rate} packets/sec")
            
            # Start attack in separate thread
            self.attack_thread = threading.Thread(target=self.dos_attack_worker, 
                                                 args=(target_ip, target_port, packet_rate))
            self.attack_thread.daemon = True
            self.attack_thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
            
    def dos_attack_worker(self, target_ip, target_port, packet_rate):
        packet_count = 0
        
        while self.is_attacking:
            try:
                # Simulate packet creation
                packet_info = {
                    'time': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                    'type': 'SYN_FLOOD',
                    'source': f"192.168.1.{random.randint(1, 254)}",
                    'destination': f"{target_ip}:{target_port}",
                    'info': f"SYN Packet #{packet_count}"
                }
                
                self.packet_log.append(packet_info)
                self.traffic_data.append(packet_rate)
                self.attack_stats['dos'] += 1
                self.attack_stats['total'] += 1
                
                packet_count += 1
                
                # Control packet rate
                time.sleep(1.0 / packet_rate)
                
            except Exception as e:
                print(f"Attack simulation error: {e}")
                break
                
    def stop_attack(self):
        self.is_attacking = False
        self.dos_button.config(text="▶️ START DoS ATTACK", bg=self.colors['danger'])
        self.dos_status.config(text="Status: Stopped", fg=self.colors['text_secondary'])
        self.status_var.set("✅ Attack Stopped")
        
        # Add to history
        self.add_to_history("Stop DoS", "DoS", "DoS attack stopped by user")
        
    def send_spoofed_packet(self):
        try:
            target_ip = self.spoof_target_ip.get()
            spoofed_ip = self.spoof_source_ip.get()
            message = self.spoof_message.get()
            
            if not target_ip or not spoofed_ip:
                messagebox.showerror("Error", "Please enter valid IP addresses")
                return
                
            # Simulate spoofed packet
            packet_info = {
                'time': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                'type': 'IP_SPOOF',
                'source': spoofed_ip,
                'destination': target_ip,
                'info': f"Message: {message}"
            }
            
            self.packet_log.append(packet_info)
            self.traffic_data.append(10)  # Add some traffic
            self.attack_stats['spoof'] += 1
            self.attack_stats['total'] += 1
            
            # Track spoof time for visualization
            self.last_spoof_time = time.time()
            
            self.status_var.set(f"🎭 Spoofed packet sent from {spoofed_ip} to {target_ip}")
            
            # Add to history
            self.add_to_history("Send Spoof", "IP Spoof", f"From: {spoofed_ip} To: {target_ip}, Message: {message[:30]}...")
            
            # Add some random traffic
            for i in range(3):
                time.sleep(0.1)
                random_packet = {
                    'time': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                    'type': 'RESPONSE',
                    'source': f"10.0.0.{random.randint(1, 254)}",
                    'destination': target_ip,
                    'info': f"Response #{i+1}"
                }
                self.packet_log.append(random_packet)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send spoofed packet: {e}")
            
    def reset_all(self):
        """Reset all attack data and statistics"""
        # Stop any running attacks
        if self.is_attacking:
            self.stop_attack()
        
        # Clear all data
        self.packet_log.clear()
        self.traffic_data.clear()
        self.attack_stats = {'dos': 0, 'spoof': 0, 'total': 0}
        
        # Reset input fields to defaults
        self.dos_target_ip.delete(0, tk.END)
        self.dos_target_ip.insert(0, "192.168.1.100")
        self.dos_target_port.delete(0, tk.END)
        self.dos_target_port.insert(0, "80")
        self.dos_packet_rate.set(50)
        
        self.spoof_target_ip.delete(0, tk.END)
        self.spoof_target_ip.insert(0, "192.168.1.100")
        self.spoof_source_ip.delete(0, tk.END)
        self.spoof_source_ip.insert(0, "10.0.0.1")
        self.spoof_message.delete(0, tk.END)
        self.spoof_message.insert(0, "Hello from spoofed IP!")
        
        # Reset status displays
        self.dos_status.config(text="Status: Ready", fg=self.colors['text_secondary'])
        self.status_var.set("✅ System Reset - Ready for New Simulation")
        
        # Clear packet tree
        for item in self.packet_tree.get_children():
            self.packet_tree.delete(item)
        
        # Clear chart
        self.chart_canvas.delete("all")
        
        # Add to history
        self.add_to_history("Reset System", "System", "All data and statistics reset")
        
    def draw_bar_chart(self):
        self.chart_canvas.delete("all")
        
        if not self.traffic_data:
            return
            
        # Canvas dimensions
        width = self.chart_canvas.winfo_width()
        height = self.chart_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        # Chart dimensions
        margin = 40
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # Get recent data (last 20 values)
        data = list(self.traffic_data)[-20:]
        if not data:
            return
            
        max_value = max(data) if data else 1
        bar_width = chart_width / len(data)
        
        # Draw axes
        self.chart_canvas.create_line(margin, height - margin, width - margin, height - margin, 
                                    fill=self.colors['text_secondary'], width=2)
        self.chart_canvas.create_line(margin, margin, margin, height - margin, 
                                    fill=self.colors['text_secondary'], width=2)
        
        # Draw bars
        for i, value in enumerate(data):
            bar_height = (value / max_value) * chart_height if max_value > 0 else 0
            x1 = margin + i * bar_width
            y1 = height - margin - bar_height
            x2 = x1 + bar_width - 2
            y2 = height - margin
            
            # Color based on intensity
            if value > 70:
                color = self.colors['danger']
            elif value > 40:
                color = self.colors['warning']
            else:
                color = self.colors['success']
                
            self.chart_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
            
            # Value label
            if bar_height > 20:
                self.chart_canvas.create_text(x1 + bar_width/2, y1 - 5, 
                                            text=str(int(value)), 
                                            fill=self.colors['fg'], 
                                            font=('Arial', 8))
        
        # Title
        self.chart_canvas.create_text(width/2, 20, 
                                    text="Traffic Intensity (Packets/Second)", 
                                    fill=self.colors['fg'], 
                                    font=('Segoe UI', 11, 'bold'))
        
    def update_display(self):
        # Update packet tree
        if self.packet_log:
            # Get new packets
            new_packets = list(self.packet_log)
            
            # Clear and repopulate tree
            for item in self.packet_tree.get_children():
                self.packet_tree.delete(item)
                
            for packet in new_packets[-50:]:  # Show last 50 packets
                self.packet_tree.insert('', 'end', values=(
                    packet['time'],
                    packet['type'],
                    packet['source'],
                    packet['destination'],
                    packet['info'][:30] + '...' if len(packet['info']) > 30 else packet['info']
                ))
        
        # Update bar chart
        self.draw_bar_chart()
        
        # Schedule next update
        self.root.after(100, self.update_display)
        
    def open_about_window(self):
        """Open a new window with educational information about network attacks"""
        about_window = tk.Toplevel(self.root)
        about_window.title("📚 About Network Attacks - Educational Information")
        about_window.geometry("800x600")
        about_window.configure(bg=self.colors['bg'])
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Title
        title_frame = tk.Frame(about_window, bg=self.colors['panel'], height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🔐 NETWORK ATTACK EDUCATION", 
                               font=('Segoe UI', 18, 'bold'), 
                               bg=self.colors['panel'], fg=self.colors['accent'])
        title_label.pack(pady=(15, 5))
        
        subtitle_label = tk.Label(title_frame, text="Educational Information for Learning Purposes Only", 
                                 font=('Segoe UI', 10), 
                                 bg=self.colors['panel'], fg=self.colors['text_secondary'])
        subtitle_label.pack()
        
        # Content Frame
        content_frame = tk.Frame(about_window, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Scrollable Text Area
        about_text = scrolledtext.ScrolledText(
            content_frame, 
            wrap=tk.WORD, 
            bg='#2d2d30', 
            fg=self.colors['fg'],
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            padx=20, 
            pady=20
        )
        about_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags
        about_text.tag_configure('title', font=('Segoe UI', 14, 'bold'), 
                                foreground=self.colors['accent'])
        about_text.tag_configure('subtitle', font=('Segoe UI', 12, 'bold'), 
                                 foreground=self.colors['fg'])
        about_text.tag_configure('warning', font=('Segoe UI', 11, 'bold'), 
                                 foreground=self.colors['danger'])
        about_text.tag_configure('bullet', font=('Segoe UI', 11), 
                                 foreground=self.colors['text_secondary'])
        
        # Add content
        about_text.insert(tk.END, "🚨 DENIAL OF SERVICE (DoS) ATTACK\n\n", 'title')
        about_text.insert(tk.END, "• Overwhelms target with traffic\n", 'bullet')
        about_text.insert(tk.END, "• Consumes system resources\n", 'bullet')
        about_text.insert(tk.END, "• Makes services unavailable\n", 'bullet')
        about_text.insert(tk.END, "• Types: SYN flood, UDP flood, ICMP flood\n\n", 'bullet')
        
        about_text.insert(tk.END, "🎭 IP SPOOFING ATTACK\n\n", 'title')
        about_text.insert(tk.END, "• Fakes source IP address\n", 'bullet')
        about_text.insert(tk.END, "• Hides attacker identity\n", 'bullet')
        about_text.insert(tk.END, "• Can bypass IP-based filters\n", 'bullet')
        about_text.insert(tk.END, "• Used in DDoS and man-in-the-middle\n\n", 'bullet')
        
        about_text.insert(tk.END, "🔐 RSA CRYPTOGRAPHY\n\n", 'title')
        about_text.insert(tk.END, "• Asymmetric encryption algorithm\n", 'bullet')
        about_text.insert(tk.END, "• Uses public and private key pairs\n", 'bullet')
        about_text.insert(tk.END, "• Based on mathematical prime factorization\n", 'bullet')
        about_text.insert(tk.END, "• Widely used in secure communications\n\n", 'bullet')
        
        about_text.insert(tk.END, "🔑 CLASSICAL CIPHERS\n\n", 'title')
        about_text.insert(tk.END, "• Caesar Cipher: Simple substitution cipher\n", 'bullet')
        about_text.insert(tk.END, "• ROT13: Simple letter rotation\n", 'bullet')
        about_text.insert(tk.END, "• Base64: Encoding, not encryption\n", 'bullet')
        about_text.insert(tk.END, "• XOR: Symmetric bitwise operation\n", 'bullet')
        about_text.insert(tk.END, "• Reverse: Simple text reversal\n\n", 'bullet')
        
        about_text.insert(tk.END, "🌐 NETWORK VISUALIZATION\n\n", 'title')
        about_text.insert(tk.END, "• Global attack topology mapping\n", 'bullet')
        about_text.insert(tk.END, "• Real-time threat level monitoring\n", 'bullet')
        about_text.insert(tk.END, "• Defense system visualization\n", 'bullet')
        about_text.insert(tk.END, "• Attack path analysis\n\n", 'bullet')
        
        about_text.insert(tk.END, "⚠️ IMPORTANT WARNING\n\n", 'warning')
        about_text.insert(tk.END, "This is an educational simulation tool only. Do not use for malicious activities.\n", 'bullet')
        about_text.insert(tk.END, "Network attacks are illegal and can cause serious damage.\n\n", 'bullet')
        
        about_text.insert(tk.END, "📚 EDUCATIONAL PURPOSE\n\n", 'subtitle')
        about_text.insert(tk.END, "Understanding these attacks and cryptography helps cybersecurity professionals:\n", 'bullet')
        about_text.insert(tk.END, "• Develop better defense mechanisms\n", 'bullet')
        about_text.insert(tk.END, "• Create effective security policies\n", 'bullet')
        about_text.insert(tk.END, "• Train incident response teams\n", 'bullet')
        about_text.insert(tk.END, "• Protect critical infrastructure\n", 'bullet')
        about_text.insert(tk.END, "• Implement secure cryptographic systems\n", 'bullet')
        about_text.insert(tk.END, "• Analyze network traffic patterns\n", 'bullet')
        
        about_text.config(state=tk.DISABLED)
        
        # Close Button
        close_frame = tk.Frame(about_window, bg=self.colors['panel'], height=50)
        close_frame.pack(fill=tk.X, side=tk.BOTTOM)
        close_frame.pack_propagate(False)
        
        close_button = tk.Button(close_frame, text="✅ Close", 
                                command=about_window.destroy,
                                bg=self.colors['success'], fg='white',
                                font=('Segoe UI', 11, 'bold'),
                                relief=tk.FLAT, padx=30, pady=10)
        close_button.pack(pady=10)
        
    def open_cryption_window(self):
        """Open a modal window with encryption/decryption tools"""
        # Create modal overlay
        overlay = tk.Toplevel(self.root)
        overlay.title("")
        overlay.geometry("1400x900")
        overlay.configure(bg='#000000')
        overlay.transient(self.root)
        overlay.overrideredirect(True)
        overlay.attributes('-alpha', 0.7)
        
        # Center the modal window - Tablet style size
        crypto_window = tk.Toplevel(self.root)
        crypto_window.title("🔐 Encryption & Decryption Tools")
        crypto_window.geometry("1024x768")
        
        # Center the window on screen
        crypto_window.update_idletasks()
        x = (crypto_window.winfo_screenwidth() // 2) - (1024 // 2)
        y = (crypto_window.winfo_screenheight() // 2) - (768 // 2)
        crypto_window.geometry(f"1024x768+{x}+{y}")
        
        crypto_window.configure(bg=self.colors['bg'])
        crypto_window.transient(self.root)
        crypto_window.grab_set()
        crypto_window.resizable(False, False)
        
        # Make overlay close when crypto window closes
        def close_all():
            overlay.destroy()
            crypto_window.destroy()
        
        crypto_window.protocol("WM_DELETE_WINDOW", close_all)
        
        # Title
        title_frame = tk.Frame(crypto_window, bg=self.colors['panel'], height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🔐 CRYPTOGRAPHY TOOLS", 
                               font=('Segoe UI', 16, 'bold'), 
                               bg=self.colors['panel'], fg=self.colors['accent'])
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(title_frame, text="Educational Encryption & Decryption Tools", 
                                 font=('Segoe UI', 10), 
                                 bg=self.colors['panel'], fg=self.colors['text_secondary'])
        subtitle_label.pack()
        
        # Main Content - Split Layout
        content_frame = tk.Frame(crypto_window, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left Panel - Features (wider for tablet)
        left_panel = tk.Frame(content_frame, bg=self.colors['panel'], width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right Panel - Results Table
        right_panel = tk.Frame(content_frame, bg=self.colors['panel'])
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # === LEFT PANEL FEATURES ===
        
        # Input Section
        input_frame = tk.LabelFrame(left_panel, text="📝 Input Message", 
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=self.colors['panel'], fg=self.colors['fg'],
                                   relief=tk.FLAT, bd=2)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.crypto_input = scrolledtext.ScrolledText(input_frame, height=4, 
                                                     bg='white', fg='black',
                                                     font=('Consolas', 9), relief=tk.FLAT)
        self.crypto_input.pack(fill=tk.X, padx=5, pady=5)
        
        # Add watermark text
        self.watermark_text = "Enter your message here..."
        self.crypto_input.insert(tk.END, self.watermark_text)
        self.crypto_input.config(fg='gray')
        
        # Watermark management
        def clear_watermark(event):
            if self.crypto_input.get("1.0", tk.END).strip() == self.watermark_text:
                self.crypto_input.delete("1.0", tk.END)
                self.crypto_input.config(fg='black')
        
        def add_watermark(event):
            if not self.crypto_input.get("1.0", tk.END).strip():
                self.crypto_input.insert(tk.END, self.watermark_text)
                self.crypto_input.config(fg='gray')
        
        # Bind watermark events and auto-scan
        self.crypto_input.bind('<FocusIn>', clear_watermark)
        self.crypto_input.bind('<FocusOut>', add_watermark)
        self.crypto_input.bind('<KeyRelease>', lambda e: self.auto_scan_message())
        self.crypto_input.bind('<Button-1>', lambda e: self.auto_scan_message())
        
        # Algorithm Selection
        algo_frame = tk.LabelFrame(left_panel, text="🔧 Algorithm", 
                                  font=('Segoe UI', 11, 'bold'),
                                  bg=self.colors['panel'], fg=self.colors['fg'],
                                  relief=tk.FLAT, bd=2)
        algo_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.crypto_algorithm = tk.StringVar(value="Caesar Cipher")
        algorithms = ["Caesar Cipher", "ROT13", "Base64", "XOR", "Reverse", "RSA"]
        
        for algo in algorithms:
            tk.Radiobutton(algo_frame, text=algo, variable=self.crypto_algorithm, 
                          value=algo, bg=self.colors['panel'], fg=self.colors['fg'],
                          font=('Segoe UI', 9), selectcolor=self.colors['accent']).pack(anchor=tk.W, padx=5, pady=1)
        
        # Key Input
        key_frame = tk.Frame(algo_frame, bg=self.colors['panel'])
        key_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(key_frame, text="Key/Shift:", bg=self.colors['panel'], fg=self.colors['fg'],
                font=('Segoe UI', 9)).pack(side=tk.LEFT)
        self.crypto_key = tk.Entry(key_frame, bg='#2d2d30', fg=self.colors['fg'],
                                   insertbackground=self.colors['fg'], relief=tk.FLAT, width=8)
        self.crypto_key.pack(side=tk.LEFT, padx=(5, 0))
        self.crypto_key.insert(0, "3")
        
        # RSA Key Size (hidden by default)
        self.rsa_key_frame = tk.Frame(algo_frame, bg=self.colors['panel'])
        
        tk.Label(self.rsa_key_frame, text="Key Size:", bg=self.colors['panel'], fg=self.colors['fg'],
                font=('Segoe UI', 9)).pack(side=tk.LEFT)
        self.rsa_key_size = tk.StringVar(value="1024")
        rsa_sizes = ["512", "1024", "2048"]
        self.rsa_key_size_menu = tk.OptionMenu(self.rsa_key_frame, self.rsa_key_size, *rsa_sizes)
        self.rsa_key_size_menu.config(bg='#2d2d30', fg=self.colors['fg'], relief=tk.FLAT)
        self.rsa_key_size_menu.pack(side=tk.LEFT, padx=(5, 0))
        
        # RSA Keys Display
        self.rsa_keys_frame = tk.Frame(algo_frame, bg=self.colors['panel'])
        
        tk.Label(self.rsa_keys_frame, text="RSA Keys:", bg=self.colors['panel'], fg=self.colors['fg'],
                font=('Segoe UI', 9, 'bold')).pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        self.rsa_keys_display = scrolledtext.ScrolledText(self.rsa_keys_frame, height=3, 
                                                         bg='#1a1a1a', fg='#00ff00',
                                                         font=('Consolas', 8), relief=tk.FLAT)
        self.rsa_keys_display.pack(fill=tk.X, padx=5, pady=5)
        self.rsa_keys_display.insert(tk.END, "Click 'Generate Keys' for RSA...")
        self.rsa_keys_display.config(state=tk.DISABLED)
        
        # RSA Generate Keys Button
        self.rsa_generate_btn = tk.Button(self.rsa_keys_frame, text="🔑 Generate Keys", 
                                         command=self.generate_rsa_keys,
                                         bg=self.colors['accent'], fg='white',
                                         font=('Segoe UI', 9, 'bold'),
                                         relief=tk.FLAT, pady=5)
        self.rsa_generate_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Bind algorithm selection change
        self.crypto_algorithm.trace('w', self.on_algorithm_change)
        
        # Buttons
        button_frame = tk.Frame(left_panel, bg=self.colors['panel'])
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        encrypt_btn = tk.Button(button_frame, text="🔒 ENCRYPT", 
                               command=lambda: self.perform_crypto_operation('encrypt'),
                               bg=self.colors['success'], fg='white',
                               font=('Segoe UI', 10, 'bold'),
                               relief=tk.FLAT, pady=8)
        encrypt_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 2))
        
        decrypt_btn = tk.Button(button_frame, text="🔓 DECRYPT", 
                               command=lambda: self.perform_crypto_operation('decrypt'),
                               bg=self.colors['warning'], fg='white',
                               font=('Segoe UI', 10, 'bold'),
                               relief=tk.FLAT, pady=8)
        decrypt_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(2, 0))
        
        # === RIGHT PANEL RESULTS TABLE ===
        
        # Results Table Frame
        results_frame = tk.LabelFrame(right_panel, text="� Results Table", 
                                      font=('Segoe UI', 12, 'bold'),
                                      bg=self.colors['panel'], fg=self.colors['fg'],
                                      relief=tk.FLAT, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Treeview for results
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Results.Treeview", 
                       background='white',
                       foreground='black',
                       fieldbackground='white',
                       borderwidth=0,
                       font=('Consolas', 9))
        style.configure("Results.Treeview.Heading",
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        columns = ('Time', 'Operation', 'Algorithm', 'Authenticity', 'Result')
        self.crypto_results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', 
                                               height=15, style="Results.Treeview")
        
        # Configure columns
        self.crypto_results_tree.heading('Time', text='Time')
        self.crypto_results_tree.heading('Operation', text='Operation')
        self.crypto_results_tree.heading('Algorithm', text='Algorithm')
        self.crypto_results_tree.heading('Authenticity', text='Authenticity')
        self.crypto_results_tree.heading('Result', text='Result')
        
        self.crypto_results_tree.column('Time', width=80)
        self.crypto_results_tree.column('Operation', width=80)
        self.crypto_results_tree.column('Algorithm', width=100)
        self.crypto_results_tree.column('Authenticity', width=120)
        self.crypto_results_tree.column('Result', width=200)
        
        # Scrollbar for results table
        results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.crypto_results_tree.yview)
        self.crypto_results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        self.crypto_results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
        
        # Initialize results storage
        self.crypto_results = []
        
        # Store reference
        self.crypto_window = crypto_window
        self.rsa_public_key = None
        self.rsa_private_key = None
        
        # Close Button
        close_frame = tk.Frame(crypto_window, bg=self.colors['panel'], height=50)
        close_frame.pack(fill=tk.X, side=tk.BOTTOM)
        close_frame.pack_propagate(False)
        
        close_button = tk.Button(close_frame, text="✅ Close", 
                                command=close_all,
                                bg=self.colors['danger'], fg='white',
                                font=('Segoe UI', 11, 'bold'),
                                relief=tk.FLAT, padx=30, pady=10)
        close_button.pack(pady=10)
    
    def perform_crypto_operation(self, operation):
        """Perform encryption or decryption based on selected algorithm"""
        try:
            text = self.crypto_input.get("1.0", tk.END).strip()
            algorithm = self.crypto_algorithm.get()
            key = self.crypto_key.get()
            
            if not text:
                messagebox.showerror("Error", "Please enter text to process")
                return
            
            result = ""
            
            if algorithm == "Caesar Cipher":
                shift = int(key) if key.isdigit() else 3
                result = self.caesar_cipher(text, shift, operation)
            elif algorithm == "ROT13":
                result = self.rot13(text)
            elif algorithm == "Base64":
                result = self.base64_operation(text, operation)
            elif algorithm == "XOR":
                xor_key = key if key else "KEY"
                result = self.xor_cipher(text, xor_key)
            elif algorithm == "Reverse":
                result = text[::-1]
            elif algorithm == "RSA":
                result = self.rsa_operation(text, operation)
            
            # Detect if result is fake or real
            authenticity = self.detect_authenticity(result, algorithm, operation)
            
            # Add to results table
            self.add_result_to_table(operation, algorithm, authenticity, result)
            
            # Log the operation
            log_entry = {
                'time': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                'type': 'CRYPTO',
                'source': 'Local',
                'destination': 'Local',
                'info': f"{operation.upper()} - {algorithm}: {text[:20]}... - {authenticity}"
            }
            self.packet_log.append(log_entry)
            
            # Add to history
            self.add_to_history(f"{operation.upper()} {algorithm}", "Crypto", f"Algorithm: {algorithm}, Text: {text[:30]}..., Result: {authenticity}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Cryptography operation failed: {str(e)}")
    
    def caesar_cipher(self, text, shift, operation):
        """Caesar cipher implementation"""
        result = ""
        if operation == 'decrypt':
            shift = -shift
            
        for char in text:
            if char.isalpha():
                ascii_offset = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    def rot13(self, text):
        """ROT13 implementation"""
        return self.caesar_cipher(text, 13, 'encrypt')
    
    def base64_operation(self, text, operation):
        """Base64 encode/decode implementation"""
        import base64
        try:
            if operation == 'encrypt':
                result = base64.b64encode(text.encode()).decode()
            else:
                result = base64.b64decode(text.encode()).decode()
            return result
        except:
            return "Invalid Base64 input"
    
    def xor_cipher(self, text, key):
        """XOR cipher implementation"""
        result = ""
        key_length = len(key)
        for i, char in enumerate(text):
            result += chr(ord(char) ^ ord(key[i % key_length]))
        return result
    
    def on_algorithm_change(self, *args):
        """Handle algorithm selection change"""
        algorithm = self.crypto_algorithm.get()
        
        # Hide all RSA-specific components by default
        self.rsa_key_frame.pack_forget()
        self.rsa_keys_frame.pack_forget()
        
        # Show/hide regular key input
        if algorithm == "RSA":
            # Hide regular key input for RSA
            for widget in self.crypto_key.master.winfo_children():
                if widget == self.crypto_key or widget.winfo_children()[0] == self.crypto_key.master.winfo_children()[0]:
                    pass
            self.rsa_key_frame.pack(fill=tk.X, padx=5, pady=5)
            self.rsa_keys_frame.pack(fill=tk.X, padx=5, pady=5)
    
    def generate_rsa_keys(self):
        """Generate RSA key pair"""
        try:
            import hashlib
            import random
            
            key_size = int(self.rsa_key_size.get())
            
            # Simple RSA key generation for educational purposes
            # In real applications, use proper cryptographic libraries
            
            # Generate two prime numbers (simplified for education)
            def generate_prime(bits):
                while True:
                    num = random.getrandbits(bits)
                    if num > 2 and num % 2 != 0:
                        # Simple primality test (Miller-Rabin would be better)
                        is_prime = True
                        for i in range(3, int(num**0.5) + 1, 2):
                            if num % i == 0:
                                is_prime = False
                                break
                        if is_prime:
                            return num
            
            # Generate smaller primes for demonstration (actual RSA uses much larger primes)
            if key_size == 512:
                p_bits, q_bits = 128, 128
            elif key_size == 1024:
                p_bits, q_bits = 256, 256
            else:  # 2048
                p_bits, q_bits = 512, 512
            
            # For educational purposes, use known small primes to avoid long computation
            if key_size == 512:
                p, q = 65537, 65539  # Small primes for demo
            elif key_size == 1024:
                p, q = 1048573, 1048579  # Medium primes for demo
            else:
                p, q = 16777213, 16777219  # Larger primes for demo
            
            # Calculate n and φ(n)
            n = p * q
            phi = (p - 1) * (q - 1)
            
            # Choose public key e (commonly 65537)
            e = 65537
            
            # Calculate private key d (modular inverse of e mod φ(n))
            def mod_inverse(a, m):
                """Calculate modular inverse using extended Euclidean algorithm"""
                def egcd(a, b):
                    if a == 0:
                        return (b, 0, 1)
                    else:
                        g, y, x = egcd(b % a, a)
                        return (g, x - (b // a) * y, y)
                
                g, x, y = egcd(a, m)
                if g != 1:
                    raise Exception('Modular inverse does not exist')
                else:
                    return x % m
            
            d = mod_inverse(e, phi)
            
            # Store keys
            self.rsa_public_key = {'n': n, 'e': e}
            self.rsa_private_key = {'n': n, 'd': d}
            
            # Display keys (truncated for display)
            keys_text = f"Public Key (e={e}):\n{n:20d}\n\nPrivate Key (d={d}):\n{d:20d}\n\nModulus (n={n}):\n{n:20d}"
            
            self.rsa_keys_display.config(state=tk.NORMAL)
            self.rsa_keys_display.delete("1.0", tk.END)
            self.rsa_keys_display.insert(tk.END, keys_text)
            self.rsa_keys_display.config(state=tk.DISABLED)
            
            # Update status
            self.status_var.set("🔑 RSA Keys Generated Successfully")
            
            # Add to history
            self.add_to_history("Generate RSA Keys", "Crypto", f"RSA {self.rsa_key_size.get()}-bit keys generated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate RSA keys: {str(e)}")
    
    def rsa_operation(self, text, operation):
        """Perform RSA encryption or decryption"""
        try:
            if not self.rsa_public_key or not self.rsa_private_key:
                return "Error: Please generate RSA keys first"
            
            # Convert text to numbers
            def text_to_numbers(text):
                return [ord(c) for c in text]
            
            def numbers_to_text(numbers):
                return ''.join([chr(n) for n in numbers if 32 <= n <= 126])
            
            # RSA encryption/decryption
            def rsa_encrypt_block(m, public_key):
                """Encrypt a single message block"""
                n, e = public_key['n'], public_key['e']
                return pow(m, e, n)
            
            def rsa_decrypt_block(c, private_key):
                """Decrypt a single ciphertext block"""
                n, d = private_key['n'], private_key['d']
                return pow(c, d, n)
            
            if operation == 'encrypt':
                # Convert text to numbers
                numbers = text_to_numbers(text)
                
                # Encrypt each number
                encrypted_numbers = []
                for num in numbers:
                    if num < self.rsa_public_key['n']:
                        encrypted_num = rsa_encrypt_block(num, self.rsa_public_key)
                        encrypted_numbers.append(encrypted_num)
                    else:
                        # Handle numbers larger than modulus
                        encrypted_numbers.append(num)  # Keep original for demo
                
                # Convert to hex string for display
                result = ''.join([f"{num:x}" for num in encrypted_numbers])
                
            else:  # decrypt
                # Parse hex string back to numbers
                try:
                    # Split hex string into reasonable chunks
                    hex_chunks = [text[i:i+8] for i in range(0, len(text), 8) if text[i:i+8]]
                    encrypted_numbers = [int(chunk, 16) for chunk in hex_chunks]
                    
                    # Decrypt each number
                    decrypted_numbers = []
                    for num in encrypted_numbers:
                        if num < self.rsa_private_key['n']:
                            decrypted_num = rsa_decrypt_block(num, self.rsa_private_key)
                            decrypted_numbers.append(decrypted_num)
                        else:
                            decrypted_numbers.append(num)
                    
                    # Convert back to text
                    result = numbers_to_text(decrypted_numbers)
                    
                except ValueError:
                    return "Error: Invalid encrypted format"
            
            return result
            
        except Exception as e:
            return f"RSA {operation} error: {str(e)}"
    
    def detect_authenticity(self, result, algorithm, operation):
        """Detect if the encryption/decryption result is fake or real"""
        try:
            # Base cases for educational simulation
            if algorithm == "Reverse":
                return "✅ REAL (Reversible operation)"
            
            if algorithm == "ROT13":
                return "✅ REAL (ROT13 is its own inverse)"
            
            if algorithm == "RSA":
                if operation == 'encrypt':
                    # RSA encryption produces hex-like output
                    if all(c in '0123456789abcdef' for c in result.replace(' ', '')):
                        return "✅ REAL (RSA encrypted data)"
                    else:
                        return "⚠️ FAKE (Invalid RSA format)"
                else:
                    # RSA decryption should produce readable text
                    if result.isprintable() and len(result) > 0:
                        return "✅ REAL (RSA decrypted text)"
                    elif "Error:" in result:
                        return "❌ ERROR (Decryption failed)"
                    else:
                        return "⚠️ FAKE (Invalid RSA decryption)"
            
            # Check for common fake patterns
            fake_indicators = 0
            real_indicators = 0
            
            # Length analysis
            if len(result) == 0:
                fake_indicators += 3
            elif len(result) < 3:
                fake_indicators += 1
            
            # Character analysis
            if result.isalpha():
                real_indicators += 2  # Text results are usually real
            elif all(c in '01' for c in result.replace(' ', '')):
                real_indicators += 1  # Binary could be real
            elif all(c in '0123456789ABCDEFabcdef' for c in result.replace(' ', '')):
                real_indicators += 1  # Hex could be real
            elif result.count(' ') > len(result) * 0.5:
                fake_indicators += 2  # Too many spaces
            
            # Pattern analysis
            if len(set(result)) < 3 and len(result) > 5:
                fake_indicators += 2  # Low character variety
            
            # Algorithm-specific checks
            if algorithm == "Caesar Cipher":
                if operation == 'decrypt' and result.islower():
                    real_indicators += 2  # Decrypted text usually readable
                elif operation == 'encrypt' and not result.isalpha():
                    real_indicators += 1  # Encrypted might have symbols
            
            elif algorithm == "Base64":
                import base64
                try:
                    # Try to decode it back
                    decoded = base64.b64decode(result).decode()
                    if decoded.isprintable():
                        real_indicators += 3
                except:
                    fake_indicators += 2
            
            elif algorithm == "XOR":
                # XOR results are harder to verify
                if any(ord(c) > 127 for c in result):
                    fake_indicators += 1  # Non-printable chars
                else:
                    real_indicators += 1
            
            # Random factor for educational purposes
            import random
            if random.random() < 0.3:  # 30% chance of adding uncertainty
                fake_indicators += 1
            elif random.random() < 0.2:  # 20% chance of favoring real
                real_indicators += 1
            
            # Determine authenticity
            if fake_indicators > real_indicators + 2:
                return "⚠️ FAKE (Suspicious patterns detected)"
            elif real_indicators > fake_indicators + 2:
                return "✅ REAL (Authentic result)"
            else:
                return "🤔 UNCERTAIN (Mixed indicators)"
                
        except Exception:
            return "❌ ERROR (Cannot determine authenticity)"
    
    
    def add_result_to_table(self, operation, algorithm, authenticity, result):
        """Add a result to the results table"""
        try:
            # Get current time
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # Truncate result if too long
            display_result = result[:50] + "..." if len(result) > 50 else result
            
            # Insert into table
            self.crypto_results_tree.insert('', 'end', values=(
                current_time,
                operation.upper(),
                algorithm,
                authenticity,
                display_result
            ))
            
            # Auto-scroll to latest entry
            children = self.crypto_results_tree.get_children()
            if children:
                self.crypto_results_tree.see(children[-1])
                
        except Exception as e:
            print(f"Error adding to table: {e}")
    
    def auto_scan_message(self):
        """Auto-scan and analyze the input message in real-time"""
        try:
            text = self.crypto_input.get("1.0", tk.END).strip()
            
            # Skip if it's just the watermark
            if text == self.watermark_text:
                return
            
            if not text:
                return
            
            # Perform quick scans for real-time feedback
            scan_results = []
            
            # Basic statistics
            char_count = len(text)
            word_count = len(text.split())
            scan_results.append(f"📊 Real-time Analysis:")
            scan_results.append(f"   Characters: {char_count} | Words: {word_count}")
            
            # Quick character analysis
            uppercase_count = sum(1 for c in text if c.isupper())
            lowercase_count = sum(1 for c in text if c.islower())
            digit_count = sum(1 for c in text if c.isdigit())
            special_count = char_count - uppercase_count - lowercase_count - digit_count
            
            if char_count > 0:
                scan_results.append(f"   Case: {uppercase_count}↑ {lowercase_count}↓ | Digits: {digit_count} | Special: {special_count}")
            
            # Quick pattern detection
            patterns_found = []
            
            # Check for common patterns
            clean_text = text.replace(' ', '')
            if len(clean_text) > 3:
                if all(c in '01' for c in clean_text):
                    patterns_found.append("Binary")
                elif all(c in '0123456789ABCDEFabcdef' for c in clean_text):
                    patterns_found.append("Hex")
                
                # Quick Base64 check
                import base64
                try:
                    if len(clean_text) % 4 == 0:
                        base64.b64decode(clean_text, validate=True)
                        patterns_found.append("Base64")
                except:
                    pass
            
            if patterns_found:
                scan_results.append(f"   � Patterns: {', '.join(patterns_found)}")
            
            # Quick security indicators
            if char_count > 5:
                # Simple entropy check
                unique_chars = len(set(text))
                entropy_ratio = unique_chars / char_count
                
                if entropy_ratio > 0.8:
                    scan_results.append(f"   ⚠️ High complexity (possible encryption)")
                elif entropy_ratio < 0.3:
                    scan_results.append(f"   ✅ Low complexity (likely plain text)")
                else:
                    scan_results.append(f"   📝 Medium complexity")
            
            # Quick frequency analysis for longer text
            if char_count > 20 and text.isalpha():
                freq_analysis = {}
                for char in text.lower():
                    freq_analysis[char] = freq_analysis.get(char, 0) + 1
                
                if freq_analysis:
                    most_common = max(freq_analysis, key=freq_analysis.get)
                    scan_results.append(f"   Most frequent: '{most_common}' ({freq_analysis[most_common]} times)")
            
            # Display results
            self.crypto_output.delete("1.0", tk.END)
            self.crypto_output.insert(tk.END, "\n".join(scan_results))
            
        except Exception:
            # Silently handle errors for auto-scan to avoid interrupting typing
            pass
    
    def open_network_map_window(self):
        """Open a new window with network attack map visualization"""
        map_window = tk.Toplevel(self.root)
        map_window.title("🗺️ Network Attack Map - Real-time Visualization")
        map_window.geometry("800x400")
        map_window.configure(bg=self.colors['bg'])
        map_window.transient(self.root)
        
        # Title
        title_frame = tk.Frame(map_window, bg=self.colors['panel'], height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🗺️ NETWORK ATTACK TOPOLOGY", 
                               font=('Segoe UI', 16, 'bold'), 
                               bg=self.colors['panel'], fg=self.colors['accent'])
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(title_frame, text="Real-time Attack Visualization", 
                                 font=('Segoe UI', 10), 
                                 bg=self.colors['panel'], fg=self.colors['text_secondary'])
        subtitle_label.pack()
        
        # Map Canvas
        map_frame = tk.Frame(map_window, bg=self.colors['bg'])
        map_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.map_canvas = Canvas(map_frame, bg='#001122', highlightthickness=0)
        self.map_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Initialize world map locations
        self.world_locations = {
            'usa': {'x': 150, 'y': 180, 'label': 'USA', 'color': self.colors['success'], 'status': 'secure'},
            'europe': {'x': 400, 'y': 140, 'label': 'Europe', 'color': self.colors['text_secondary'], 'status': 'secure'},
            'asia': {'x': 600, 'y': 160, 'label': 'Asia', 'color': self.colors['text_secondary'], 'status': 'secure'},
            'attacker': {'x': 500, 'y': 200, 'label': 'Attacker', 'color': self.colors['danger'], 'status': 'attacker'},
            'target': {'x': 200, 'y': 150, 'label': 'Target', 'color': self.colors['warning'], 'status': 'target'},
            'russia': {'x': 550, 'y': 120, 'label': 'Russia', 'color': self.colors['text_secondary'], 'status': 'secure'},
            'china': {'x': 650, 'y': 180, 'label': 'China', 'color': self.colors['text_secondary'], 'status': 'secure'},
            'brazil': {'x': 170, 'y': 220, 'label': 'Brazil', 'color': self.colors['text_secondary'], 'status': 'secure'},
            'india': {'x': 580, 'y': 200, 'label': 'India', 'color': self.colors['text_secondary'], 'status': 'secure'},
            'uk': {'x': 380, 'y': 120, 'label': 'UK', 'color': self.colors['text_secondary'], 'status': 'secure'}
        }
        
        # Attack paths and routes
        self.attack_paths = []
        self.defense_systems = {
            'usa_firewall': {'x': 150, 'y': 160, 'active': False},
            'europe_firewall': {'x': 400, 'y': 120, 'active': False},
            'asia_firewall': {'x': 600, 'y': 140, 'active': False}
        }
        
        # Start map update loop
        self.map_window = map_window
        self.update_world_map()
        
        # Close Button
        close_frame = tk.Frame(map_window, bg=self.colors['panel'], height=50)
        close_frame.pack(fill=tk.X, side=tk.BOTTOM)
        close_frame.pack_propagate(False)
        
        close_button = tk.Button(close_frame, text="✅ Close Map", 
                                command=map_window.destroy,
                                bg=self.colors['danger'], fg='white',
                                font=('Segoe UI', 11, 'bold'),
                                relief=tk.FLAT, padx=30, pady=10)
        close_button.pack(pady=10)
        
    def update_world_map(self):
        """Update the world map visualization"""
        if hasattr(self, 'map_canvas') and self.map_canvas.winfo_exists():
            self.map_canvas.delete("all")
            
            # Get canvas dimensions
            width = self.map_canvas.winfo_width()
            height = self.map_canvas.winfo_height()
            
            if width <= 1 or height <= 1:
                self.root.after(100, self.update_world_map)
                return
                
            # Draw world map background
            self.draw_world_map_outline(width, height)
            
            # Draw defense systems (firewalls, IDS)
            self.draw_defense_systems()
            
            # Draw attack connections
            if self.is_attacking:
                self.draw_attack_connections()
                
            # Draw spoofing connections
            if hasattr(self, 'last_spoof_time') and time.time() - self.last_spoof_time < 3:
                self.draw_spoofing_connections()
            
            # Draw location markers
            self.draw_location_markers()
            
            # Draw network statistics
            self.draw_network_statistics(width, height)
            
            # Draw legend
            self.draw_advanced_legend(width, height)
            
            # Draw title and status
            self.draw_map_header(width, height)
            
            # Schedule next update
            if hasattr(self, 'map_window') and self.map_window.winfo_exists():
                self.root.after(100, self.update_world_map)
    
    def draw_defense_systems(self):
        """Draw defense systems like firewalls and IDS"""
        for name, defense in self.defense_systems.items():
            if self.is_attacking:
                defense['active'] = True
                
            # Draw defense shield
            if defense['active']:
                # Animated shield effect - ensure integer values
                pulse = int(abs(math.sin(time.time() * 3)) * 5)
                size = 15 + pulse
                self.map_canvas.create_oval(
                    defense['x'] - size, defense['y'] - size,
                    defense['x'] + size, defense['y'] + size,
                    fill='', outline=self.colors['success'], width=2
                )
                self.map_canvas.create_text(
                    defense['x'], defense['y'] - 25,
                    text='🛡️', fill=self.colors['success'],
                    font=('Segoe UI', 12)
                )
            else:
                # Inactive defense
                self.map_canvas.create_oval(
                    defense['x'] - 12, defense['y'] - 12,
                    defense['x'] + 12, defense['y'] + 12,
                    fill='', outline=self.colors['text_secondary'], width=1
                )
                self.map_canvas.create_text(
                    defense['x'], defense['y'] - 20,
                    text='🔒', fill=self.colors['text_secondary'],
                    font=('Segoe UI', 10)
                )
    
    def draw_attack_connections(self):
        """Draw attack connections with advanced effects"""
        attacker = self.world_locations['attacker']
        target = self.world_locations['target']
        
        # Multiple attack paths for realism
        attack_routes = [
            (attacker, target, 'direct'),
            (attacker, self.world_locations['usa'], 'bounce'),
            (attacker, self.world_locations['europe'], 'bounce')
        ]
        
        for start, end, route_type in attack_routes:
            if route_type == 'direct':
                # Direct attack with animation
                for i in range(3):
                    offset = (time.time() * 150 + i * 40) % 120
                    self.map_canvas.create_line(
                        start['x'], start['y'],
                        end['x'], end['y'],
                        fill=self.colors['danger'], width=4,
                        dash=(offset, 120-offset),
                        tags="attack"
                    )
                
                # Main attack arrow
                mid_x = (start['x'] + end['x']) / 2
                mid_y = (start['y'] + end['y']) / 2
                self.map_canvas.create_polygon(
                    mid_x - 12, mid_y - 12,
                    mid_x + 12, mid_y,
                    mid_x - 12, mid_y + 12,
                    fill=self.colors['danger'], outline="",
                    tags="attack"
                )
            else:
                # Bounce/routed attacks
                self.map_canvas.create_line(
                    start['x'], start['y'],
                    end['x'], end['y'],
                    fill=self.colors['warning'], width=2,
                    dash=(10, 5),
                    tags="bounce"
                )
    
    def draw_spoofing_connections(self):
        """Draw spoofing connections from multiple locations"""
        target = self.world_locations['target']
        spoof_sources = ['usa', 'europe', 'asia', 'russia', 'china']
        
        for source_name in spoof_sources:
            if source_name in self.world_locations:
                source = self.world_locations[source_name]
                
                # Animated spoofing lines
                offset = (time.time() * 80) % 40
                self.map_canvas.create_line(
                    source['x'], source['y'],
                    target['x'], target['y'],
                    fill=self.colors['accent'], width=3,
                    dash=(offset, 40-offset),
                    tags="spoof"
                )
                
                # Spoof indicator
                self.map_canvas.create_text(
                    source['x'], source['y'] - 20,
                    text='🎭', fill=self.colors['accent'],
                    font=('Segoe UI', 10)
                )
    
    def draw_location_markers(self):
        """Draw enhanced location markers"""
        for name, location in self.world_locations.items():
            # Determine marker size based on importance
            if name == 'attacker':
                size = 15
                symbol = '🚨'
            elif name == 'target':
                size = 15
                symbol = '🎯'
            else:
                size = 10
                symbol = '🌐'
                
            # Pulsing effect for active locations - ensure integer values
            if name in ['attacker', 'target'] and self.is_attacking:
                pulse = int(abs(math.sin(time.time() * 4)) * 3)
                size += pulse
                
            # Draw location circle
            self.map_canvas.create_oval(
                location['x'] - size, location['y'] - size,
                location['x'] + size, location['y'] + size,
                fill=location['color'], outline='white', width=3
            )
            
            # Draw symbol
            self.map_canvas.create_text(
                location['x'], location['y'] - size - 15,
                text=symbol, fill=location['color'],
                font=('Segoe UI', 12)
            )
            
            # Draw location label
            self.map_canvas.create_text(
                location['x'], location['y'] + size + 15,
                text=location['label'], fill=self.colors['fg'],
                font=('Segoe UI', 10, 'bold')
            )
            
            # Draw status indicator
            status_color = self.colors['success'] if location['status'] == 'secure' else self.colors['danger']
            self.map_canvas.create_oval(
                location['x'] + size - 5, location['y'] - size + 5,
                location['x'] + size, location['y'] - size,
                fill=status_color, outline=''
            )
    
    def draw_network_statistics(self, width, height):
        """Draw network statistics overlay"""
        stats_x = width - 150
        stats_y = 80
        
        # Background panel
        self.map_canvas.create_rectangle(
            stats_x - 10, stats_y - 10,
            stats_x + 140, stats_y + 120,
            fill='#1a1a2e', outline=self.colors['accent'], width=2
        )
        
        # Statistics title
        self.map_canvas.create_text(
            stats_x + 65, stats_y + 5,
            text='NETWORK STATS', fill=self.colors['accent'],
            font=('Segoe UI', 11, 'bold')
        )
        
        # Stats content
        stats = [
            f"Total Attacks: {self.attack_stats['total']}",
            f"DoS Attacks: {self.attack_stats['dos']}",
            f"Spoofed: {self.attack_stats['spoof']}",
            f"Status: {'ACTIVE' if self.is_attacking else 'MONITORING'}",
            f"Threat Level: {'HIGH' if self.is_attacking else 'LOW'}"
        ]
        
        for i, stat in enumerate(stats):
            self.map_canvas.create_text(
                stats_x + 10, stats_y + 30 + i * 18,
                text=stat, fill=self.colors['fg'],
                font=('Segoe UI', 9), anchor='w'
            )
    
    def draw_advanced_legend(self, width, height):
        """Draw comprehensive legend"""
        legend_x = 20
        legend_y = height - 80
        
        # Legend background
        self.map_canvas.create_rectangle(
            legend_x - 5, legend_y - 5,
            legend_x + 200, legend_y + 75,
            fill='#1a1a2e', outline=self.colors['accent'], width=1
        )
        
        # Legend title
        self.map_canvas.create_text(
            legend_x + 97, legend_y + 5,
            text='LEGEND', fill=self.colors['accent'],
            font=('Segoe UI', 10, 'bold')
        )
        
        # Legend items
        legend_items = [
            ('🚨', 'Attacker', self.colors['danger']),
            ('🎯', 'Target', self.colors['warning']),
            ('🌐', 'Secure Node', self.colors['success']),
            ('🎭', 'Spoofed Source', self.colors['accent']),
            ('🛡️', 'Active Defense', self.colors['success']),
            ('🔒', 'Inactive Defense', self.colors['text_secondary']),
            ('---', 'Direct Attack', self.colors['danger']),
            ('- -', 'Routed Attack', self.colors['warning']),
            ('- .', 'Spoofed Traffic', self.colors['accent'])
        ]
        
        for i, (symbol, text, color) in enumerate(legend_items):
            y_pos = legend_y + 25 + (i // 2) * 15
            x_pos = legend_x + 10 + (i % 2) * 100
            
            self.map_canvas.create_text(
                x_pos, y_pos, text=f"{symbol} {text}",
                fill=color, font=('Segoe UI', 8), anchor='w'
            )
    
    def draw_map_header(self, width, height):
        """Draw map title and global status"""
        # Main title
        self.map_canvas.create_text(
            width // 2, 25, text="🌍 GLOBAL CYBER ATTACK MONITORING SYSTEM",
            fill=self.colors['accent'], font=('Segoe UI', 16, 'bold')
        )
        
        # Global threat level indicator
        threat_level = "� CRITICAL" if self.is_attacking else "🟢 NORMAL"
        threat_color = self.colors['danger'] if self.is_attacking else self.colors['success']
        
        # Threat level background
        self.map_canvas.create_rectangle(
            width // 2 - 80, 45,
            width // 2 + 80, 75,
            fill='#1a1a2e', outline=threat_color, width=2
        )
        
        self.map_canvas.create_text(
            width // 2, 60, text=f"THREAT LEVEL: {threat_level}",
            fill=threat_color, font=('Segoe UI', 12, 'bold')
        )
        
        # Real-time clock
        current_time = datetime.now().strftime("%H:%M:%S UTC")
        self.map_canvas.create_text(
            width - 120, 30, text=f"🕐 {current_time}",
            fill=self.colors['text_secondary'], font=('Segoe UI', 10)
        )
    
    def draw_world_map_outline(self, width, height):
        """Draw futuristic world map with glowing effects"""
        # Dark ocean background with grid
        for x in range(0, width, 30):
            self.map_canvas.create_line(x, 0, x, height, fill='#001133', width=1, dash=(1, 4))
        for y in range(0, height, 30):
            self.map_canvas.create_line(0, y, width, y, fill='#001133', width=1, dash=(1, 4))
        
        # Glowing continent outlines based on attack status
        glow_color = self.colors['danger'] if self.is_attacking else '#00ffff'
        
        # North America with multiple glow layers
        for i in range(3):
            width_offset = i * 2
            self.map_canvas.create_polygon(
                100-width_offset, 120-width_offset, 180-width_offset, 110-width_offset, 
                200-width_offset, 140-width_offset, 180-width_offset, 180-width_offset, 
                120-width_offset, 170-width_offset, 100-width_offset, 150-width_offset,
                fill='', outline=glow_color, width=4-i, smooth=True
            )
        
        # Europe with glow
        for i in range(3):
            width_offset = i * 2
            self.map_canvas.create_polygon(
                380-width_offset, 100-width_offset, 450-width_offset, 90-width_offset, 
                500-width_offset, 120-width_offset, 480-width_offset, 160-width_offset, 
                400-width_offset, 150-width_offset, 370-width_offset, 130-width_offset,
                fill='', outline=glow_color, width=4-i, smooth=True
            )
        
        # Asia with glow
        for i in range(3):
            width_offset = i * 2
            self.map_canvas.create_polygon(
                520-width_offset, 130-width_offset, 680-width_offset, 120-width_offset, 
                700-width_offset, 180-width_offset, 650-width_offset, 200-width_offset, 
                540-width_offset, 170-width_offset, 520-width_offset, 150-width_offset,
                fill='', outline=glow_color, width=4-i, smooth=True
            )
        
        # South America
        self.map_canvas.create_polygon(
            150, 200, 180, 250, 170, 300, 140, 280, 120, 230,
            fill='', outline='#00ffff', width=2, smooth=True
        )
        
        # Africa
        self.map_canvas.create_polygon(
            400, 180, 450, 250, 430, 320, 380, 300, 370, 230,
            fill='', outline='#00ffff', width=2, smooth=True
        )
        
        # Australia
        self.map_canvas.create_polygon(
            600, 250, 650, 240, 670, 280, 640, 300, 610, 270,
            fill='', outline='#00ffff', width=2, smooth=True
        )
        
        # Add radar circles at strategic points
        self.draw_radar_systems(width, height)
        
        # Add data overlay effects
        self.draw_data_overlay(width, height)
    
    def draw_radar_systems(self, width, height):
        """Draw radar-like monitoring systems"""
        radar_positions = [
            (width//2, height//2, 80),  # Center radar
            (150, 150, 50),            # North America radar
            (450, 130, 50),            # Europe radar
            (620, 170, 50),            # Asia radar
        ]
        
        for x, y, radius in radar_positions:
            # Animated radar sweep - ensure integer values
            if self.is_attacking:
                angle = (time.time() * 2) % (2 * math.pi)
                end_x = int(x + radius * math.cos(angle))
                end_y = int(y + radius * math.sin(angle))
                
                # Radar sweep line
                self.map_canvas.create_line(
                    x, y, end_x, end_y,
                    fill=self.colors['danger'], width=2
                )
            
            # Radar circles
            for i in range(3):
                r = int(radius * (i + 1) / 3)
                color = self.colors['danger'] if self.is_attacking else '#00ffff'
                self.map_canvas.create_oval(
                    x - r, y - r, x + r, y + r,
                    outline=color, width=1
                )
            
            # Center point
            self.map_canvas.create_oval(
                x - 3, y - 3, x + 3, y + 3,
                fill=self.colors['danger'] if self.is_attacking else '#00ffff',
                outline=''
            )
    
    def draw_data_overlay(self, width, height):
        """Draw data overlay effects"""
        # Random data points for high-tech effect
        for _ in range(20):
            x = random.randint(50, width - 50)
            y = random.randint(50, height - 50)
            
            # Data point
            self.map_canvas.create_oval(
                x - 2, y - 2, x + 2, y + 2,
                fill=self.colors['accent'], outline=''
            )
            
            # Data value
            value = random.randint(0, 999)
            self.map_canvas.create_text(
                x + 10, y, text=f"{value}",
                fill=self.colors['text_secondary'],
                font=('Courier', 8)
            )
        
        # Connection lines between data points
        for _ in range(10):
            x1 = random.randint(50, width - 50)
            y1 = random.randint(50, height - 50)
            x2 = random.randint(50, width - 50)
            y2 = random.randint(50, height - 50)
            
            self.map_canvas.create_line(
                x1, y1, x2, y2,
                fill='#003366', width=1, dash=(2, 4)
            )
    
    def open_history_window(self):
        """Open a window showing the history of all operations"""
        history_window = tk.Toplevel(self.root)
        history_window.title("📜 Operation History")
        history_window.geometry("900x600")
        history_window.configure(bg=self.colors['bg'])
        history_window.transient(self.root)
        history_window.grab_set()
        
        # Title
        title_frame = tk.Frame(history_window, bg=self.colors['panel'], height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📜 OPERATION HISTORY", 
                               font=('Segoe UI', 16, 'bold'), 
                               bg=self.colors['panel'], fg=self.colors['accent'])
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(title_frame, text="Complete log of all network and cryptographic operations", 
                                 font=('Segoe UI', 10), 
                                 bg=self.colors['panel'], fg=self.colors['text_secondary'])
        subtitle_label.pack()
        
        # Content Frame
        content_frame = tk.Frame(history_window, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create Treeview for history
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("History.Treeview", 
                       background='#2d2d30',
                       foreground=self.colors['fg'],
                       fieldbackground='#2d2d30',
                       borderwidth=0,
                       font=('Consolas', 9))
        style.configure("History.Treeview.Heading",
                       background=self.colors['accent'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        
        columns = ('Timestamp', 'Operation', 'Type', 'Details', 'Status')
        history_tree = ttk.Treeview(content_frame, columns=columns, show='headings', 
                                height=20, style="History.Treeview")
        
        # Configure columns
        history_tree.heading('Timestamp', text='Timestamp')
        history_tree.heading('Operation', text='Operation')
        history_tree.heading('Type', text='Type')
        history_tree.heading('Details', text='Details')
        history_tree.heading('Status', text='Status')
        
        history_tree.column('Timestamp', width=120)
        history_tree.column('Operation', width=100)
        history_tree.column('Type', width=100)
        history_tree.column('Details', width=300)
        history_tree.column('Status', width=120)
        
        # Scrollbar
        history_scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=history_tree.yview)
        history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0), pady=0)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 0), pady=0)
        
        # Populate history
        for entry in self.operation_history:
            history_tree.insert('', 'end', values=(
                entry['timestamp'],
                entry['operation'],
                entry['type'],
                entry['details'][:50] + '...' if len(entry['details']) > 50 else entry['details'],
                entry['status']
            ))
        
        # Statistics Frame
        stats_frame = tk.LabelFrame(content_frame, text="📊 Statistics", 
                                font=('Segoe UI', 11, 'bold'),
                                bg=self.colors['panel'], fg=self.colors['fg'],
                                relief=tk.FLAT, bd=2)
        stats_frame.pack(fill=tk.X, padx=0, pady=(10, 0))
        
        # Calculate statistics
        total_ops = len(self.operation_history)
        dos_ops = sum(1 for entry in self.operation_history if entry['type'] == 'DoS')
        spoof_ops = sum(1 for entry in self.operation_history if entry['type'] == 'IP Spoof')
        crypto_ops = sum(1 for entry in self.operation_history if entry['type'] == 'Crypto')
        
        stats_text = f"Total Operations: {total_ops} | DoS: {dos_ops} | IP Spoof: {spoof_ops} | Crypto: {crypto_ops}"
        stats_label = tk.Label(stats_frame, text=stats_text, 
                            bg=self.colors['panel'], fg=self.colors['text_secondary'],
                            font=('Segoe UI', 10))
        stats_label.pack(pady=10)
        
        # Buttons Frame
        buttons_frame = tk.Frame(history_window, bg=self.colors['panel'], height=50)
        buttons_frame.pack(fill=tk.X, side=tk.BOTTOM)
        buttons_frame.pack_propagate(False)
        
        # Clear History Button
        clear_btn = tk.Button(buttons_frame, text="🗑️ Clear History", 
                           command=self.clear_history,
                           bg=self.colors['danger'], fg='white',
                           font=('Segoe UI', 10, 'bold'),
                           relief=tk.FLAT, padx=20, pady=10)
        clear_btn.pack(side=tk.LEFT, padx=(20, 10), pady=10)
        
        # Export History Button
        export_btn = tk.Button(buttons_frame, text="💾 Export History", 
                            command=lambda: self.export_history(history_window),
                            bg=self.colors['success'], fg='white',
                            font=('Segoe UI', 10, 'bold'),
                            relief=tk.FLAT, padx=20, pady=10)
        export_btn.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        # Daily Report Button
        daily_btn = tk.Button(buttons_frame, text="� Open Report", 
                           command=self.open_daily_report,
                           bg=self.colors['accent'], fg='white',
                           font=('Segoe UI', 10, 'bold'),
                           relief=tk.FLAT, padx=20, pady=10)
        daily_btn.pack(side=tk.LEFT, padx=(0, 10), pady=10)
        
        # Close Button
        close_btn = tk.Button(buttons_frame, text="✅ Close", 
                           command=history_window.destroy,
                           bg=self.colors['accent'], fg='white',
                           font=('Segoe UI', 10, 'bold'),
                           relief=tk.FLAT, padx=20, pady=10)
        close_btn.pack(side=tk.RIGHT, padx=(0, 20), pady=10)
    
    def add_to_history(self, operation, op_type, details, status="Success"):
        """Add an operation to the history log and automatically save it to today's CSV report."""
        history_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operation': operation,
            'type': op_type,
            'details': details,
            'status': status
        }
        self.operation_history.append(history_entry)
        # Automatically append to daily report on each new entry
        try:
            self.append_to_daily_report(history_entry)
        except Exception:
            pass
    
    def clear_history(self):
        """Clear the operation history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all operation history?"):
            self.operation_history.clear()
            messagebox.showinfo("History Cleared", "Operation history has been cleared successfully.")
    
    def export_history(self, parent_window):
        """Export history to a text file"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save History As"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("NETWORK ATTACK SIMULATOR - OPERATION HISTORY\n")
                    f.write("=" * 60 + "\n\n")
                    
                    for entry in self.operation_history:
                        f.write(f"Timestamp: {entry['timestamp']}\n")
                        f.write(f"Operation: {entry['operation']}\n")
                        f.write(f"Type: {entry['type']}\n")
                        f.write(f"Details: {entry['details']}\n")
                        f.write(f"Status: {entry['status']}\n")
                        f.write("-" * 40 + "\n\n")
                
                messagebox.showinfo("Export Successful", f"History exported to {filename}")
                parent_window.destroy()
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export history: {str(e)}")
    
    def open_daily_report(self):
        """Open or create daily history report file"""
        try:
            import os
            from datetime import date
            
            # Create daily report filename
            today = date.today().strftime("%Y-%m-%d")
            network_report_filename = f"network_security_report_{today}.csv"
            network_report_path = os.path.join(os.getcwd(), network_report_filename)
            
            # Check if network report exists
            # Always regenerate today's report so data stays current
            try:
                self.create_daily_report(network_report_path, today)
            except Exception:
                pass
            if os.path.exists(network_report_path):
                os.startfile(network_report_path)
                messagebox.showinfo("CSV Report", f"Network security CSV report for {today} opened successfully.\n\nFile: {network_report_filename}")
            else:
                messagebox.showerror("CSV Report Error", f"Unable to locate or create report for {today}.")
                
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to open/create network security report: {str(e)}")
    
    def append_to_daily_report(self, entry):
        """Append a single history entry to the current day's CSV file, creating it if necessary."""
        try:
            import os, csv
            date_str = entry['timestamp'].split(' ')[0]
            filename = f"network_security_report_{date_str}.csv"
            filepath = os.path.join(os.getcwd(), filename)
            file_exists = os.path.exists(filepath)
            mode = 'a' if file_exists else 'w'
            with open(filepath, mode, newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Timestamp', 'Operation', 'Type', 'Details', 'Status']
                if not file_exists:
                    # write BOM for Excel then header
                    csvfile.write('\ufeff')
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                else:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                # sanitize
                safe_entry = {
                    'Timestamp': entry.get('timestamp', ''),
                    'Operation': entry.get('operation', ''),
                    'Type': entry.get('type', ''),
                    'Details': entry.get('details', ''),
                    'Status': entry.get('status', '')
                }
                writer.writerow(safe_entry)
        except Exception:
            pass

    def create_daily_report(self, filepath, date_str):
        """Create a daily report in CSV format for Excel compatibility"""
        try:
            import csv
            
            # Filter today's operations
            today_operations = [
                entry for entry in self.operation_history 
                if entry['timestamp'].startswith(date_str)
            ]
            
            # when creating a fresh report we want to ensure only one BOM and a proper header
            # open with utf-8 so we can manually insert BOM only once
            file_exists = False
            try:
                file_exists = os.path.exists(filepath)
            except Exception:
                file_exists = False

            mode = 'a' if file_exists else 'w'
            with open(filepath, mode, newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Timestamp', 'Operation', 'Type', 'Details', 'Status']
                # write BOM manually only when new file is created
                if not file_exists:
                    csvfile.write('\ufeff')
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()

                # Write all operations
                for entry in today_operations:
                    # Sanitize data for CSV compatibility
                    safe_entry = {
                        'Timestamp': str(entry.get('timestamp', '')).replace('\n', ' ').replace('\r', ' '),
                        'Operation': str(entry.get('operation', '')).replace('\n', ' ').replace('\r', ' '),
                        'Type': str(entry.get('type', '')).replace('\n', ' ').replace('\r', ' '),
                        'Details': str(entry.get('details', '')).replace('\n', ' ').replace('\r', ' '),
                        'Status': str(entry.get('status', '')).replace('\n', ' ').replace('\r', ' ')
                    }
                    writer.writerow(safe_entry)
                
                # Write summary statistics as separate rows
                if today_operations:
                    dos_ops = [op for op in today_operations if op['type'] == 'DoS']
                    spoof_ops = [op for op in today_operations if op['type'] == 'IP Spoof']
                    crypto_ops = [op for op in today_operations if op['type'] == 'Crypto']
                    system_ops = [op for op in today_operations if op['type'] == 'System']
                    
                    # Add summary rows
                    writer.writerow({
                        'Timestamp': date_str + ' 23:59:59',
                        'Operation': 'SUMMARY',
                        'Type': 'STATISTICS',
                        'Details': f'Total Operations: {len(today_operations)}',
                        'Status': 'Completed'
                    })
                    writer.writerow({
                        'Timestamp': date_str + ' 23:59:59',
                        'Operation': 'SUMMARY',
                        'Type': 'STATISTICS',
                        'Details': f'DoS Attacks: {len(dos_ops)}',
                        'Status': 'Completed'
                    })
                    writer.writerow({
                        'Timestamp': date_str + ' 23:59:59',
                        'Operation': 'SUMMARY',
                        'Type': 'STATISTICS',
                        'Details': f'IP Spoofing: {len(spoof_ops)}',
                        'Status': 'Completed'
                    })
                    writer.writerow({
                        'Timestamp': date_str + ' 23:59:59',
                        'Operation': 'SUMMARY',
                        'Type': 'STATISTICS',
                        'Details': f'Cryptography: {len(crypto_ops)}',
                        'Status': 'Completed'
                    })
                    writer.writerow({
                        'Timestamp': date_str + ' 23:59:59',
                        'Operation': 'SUMMARY',
                        'Type': 'STATISTICS',
                        'Details': f'System Operations: {len(system_ops)}',
                        'Status': 'Completed'
                    })
                    
                    # Peak activity analysis
                    hours = [int(op['timestamp'].split(' ')[1].split(':')[0]) for op in today_operations if ' ' in op['timestamp']]
                    if hours:
                        peak_hour = max(set(hours), key=hours.count)
                        writer.writerow({
                            'Timestamp': date_str + ' 23:59:59',
                            'Operation': 'ANALYSIS',
                            'Type': 'PEAK_ACTIVITY',
                            'Details': f'Peak Hour: {peak_hour}:00',
                            'Status': 'Completed'
                        })
                    
                    # Most common operation
                    types = [op['type'] for op in today_operations]
                    if types:
                        most_common = max(set(types), key=types.count)
                        writer.writerow({
                            'Timestamp': date_str + ' 23:59:59',
                            'Operation': 'ANALYSIS',
                            'Type': 'MOST_COMMON',
                            'Details': f'Most Common: {most_common}',
                            'Status': 'Completed'
                        })
                
        except Exception as e:
            raise Exception(f"Failed to create daily report: {str(e)}")

def main():
    root = tk.Tk()
    app = ModernNetworkAttackSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
