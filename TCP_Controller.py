import tkinter
import socket

class Listener():
#FUNCTION
#=======================================================================================================#
    def __init__(self, IP, PORT):
        global connection1, adress
        try:
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            listener.bind((IP, PORT))
            listener.listen(0)

            (connection1, adress) = listener.accept()
            connection_situation.delete("1.0", tkinter.END)
            connection_situation.insert(tkinter.END, "SUCCESSFUL")

            adress_situation.delete("1.0", tkinter.END)
            ip_address = adress[0]
            adress_situation.insert(tkinter.END, ip_address)
            error_situation.delete("1.0", tkinter.END)
        
        except Exception as e:
            connection_situation.delete("1.0", tkinter.END)
            connection_situation.insert(tkinter.END, "UNSUCCESSFUL")

            adress_situation.delete("1.0", tkinter.END)
            adress_situation.insert(tkinter.END, "Error")

            error_situation.delete("1.0", tkinter.END)
            error_situation.insert(tkinter.END, str(e))

    def execute_command(self, event = None):
        global command_output
        command_input = command_line.get("1.0", tkinter.END).strip()
        
        if command_input == "clear" or command_input == "cls":
            output_text.delete("1.0", tkinter.END)
        
        else:
            try:
                connection1.send(command_input.encode("utf-8"))

                command_output = connection1.recv(2048)
                output_text.insert(tkinter.END, command_output)
                output_text.see(tkinter.END)

            except Exception as e:

                connection_situation.delete("1.0", tkinter.END)
                connection_situation.insert(tkinter.END, "DISCONNECTED")

                adress_situation.delete("1.0", tkinter.END)
                adress_situation.insert(tkinter.END, "Error")

                error_situation.delete("1.0", tkinter.END)
                error_situation.insert(tkinter.END, str(e))

        command_line.delete("1.0", tkinter.END)
        return "break"

if __name__ == "__main__":

    def socket_info():
        try:
            ip = ip_entry.get()
            port = int(port_entry.get())
            Listener(ip, port)
        
        except Exception as e:
            error_situation.delete("1.0", tkinter.END)
            error_situation.insert(tkinter.END, str(e))

    def close_socket():
        global connection1
        try:
            connection1.close()
            connection_situation.delete("1.0", tkinter.END)
            connection_situation.insert(tkinter.END, "DISCONNECTED")
            adress_situation.delete("1.0", tkinter.END)
            adress_situation.insert(tkinter.END, "Error")
            error_situation.delete("1.0", tkinter.END)

        except Exception as e:
            error_situation.delete("1.0", tkinter.END)
            error_situation.insert(tkinter.END, str(e))

#MAIN FRAME
#=======================================================================================================#
    window = tkinter.Tk()
    window.title("Socket Monitor")

    frame = tkinter.Frame(window, bg="#262626")
    frame.pack(fill=tkinter.BOTH, expand=True)

    width = 1210
    height = 699

    window.resizable(False, False)
    window.geometry(f"{width}x{height}")

#CONTAINER FRAME
#=======================================================================================================#
    container_frame = tkinter.Frame(frame, bg="#303030")
    container_frame.pack(side=tkinter.LEFT, padx=10, pady=10, expand=True)

#CONFIG FRAME
#=======================================================================================================#
    config_frame = tkinter.LabelFrame(container_frame, text="CONFIGRATION", bg="#303030", fg="lightgray")
    config_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

#INFO FRAME
#=======================================================================================================#
    info_frame = tkinter.LabelFrame(container_frame, text="INFORMATION", bg="#303030", fg="lightgray")
    info_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

#X FRAME
#=======================================================================================================#
    _frame = tkinter.LabelFrame(container_frame, text="VERSION" ,bg="#303030", fg="lightgray")
    _frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

#SET IP
#=======================================================================================================#
    ip_label = tkinter.Label(config_frame, text="Set IP :", bg="#303030", fg="lightgray")
    ip_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    ip_entry = tkinter.Entry(config_frame)
    ip_entry.grid(row=0, column=1, padx=5, pady=5)

#SET PORT
#=======================================================================================================#
    port_label = tkinter.Label(config_frame, text="Set Port :", bg="#303030", fg="lightgray")
    port_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    port_entry = tkinter.Entry(config_frame)
    port_entry.grid(row=1, column=1, padx=5, pady=5)

#START BUTTON
#=======================================================================================================#
    button_label = tkinter.Label(config_frame, text="Start to Listen :", bg="#303030", fg="lightgray")
    button_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    button1_button = tkinter.Button(config_frame, text="START",command=socket_info, bg="#017359")
    button1_button.grid(row=2, column=1, padx=5, pady=5, sticky="news")

#STOP BUTTON
#=======================================================================================================#
    button2_label = tkinter.Label(config_frame, text="Stop to Listen :", bg="#303030", fg="lightgray")
    button2_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    button2_button = tkinter.Button(config_frame, text="STOP",command=close_socket, bg="#9E0000", fg="#D6D6D6")
    button2_button.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

#CONNECTION
#=======================================================================================================#
    connection_label = tkinter.Label(info_frame, text="Connection :", bg="#303030", fg="lightgray")
    connection_label.grid(row=0, column=0, padx=5, pady=0, sticky="w")

    connection_situation = tkinter.Text(info_frame, width=15, height=1, fg="#00F204", bg="black")
    connection_situation.grid(row=0, column=1, padx=20, pady=5, sticky="news")

#ADRESS
#=======================================================================================================#
    adress_label = tkinter.Label(info_frame, text="Adress :", bg="#303030", fg="lightgray")
    adress_label.grid(row=1, column=0, padx=5, pady=0, sticky="w")

    adress_situation = tkinter.Text(info_frame, width=15, height=1, fg="#00F204", bg="black")
    adress_situation.grid(row=1, column=1, padx=20, pady=5, sticky="news")

#ERROR
#=======================================================================================================#
    error_label = tkinter.Label(info_frame, text="Errors :", bg="#303030", fg="lightgray")
    error_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    error_situation = tkinter.Text(info_frame, width=18, height=18, fg="red", bg="black")
    error_situation.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="news")

#OUTPUT FRAME
#=======================================================================================================#
    output_frame = tkinter.LabelFrame(container_frame, text="OUTPUT", bg="#303030", fg="lightgray")
    output_frame.grid(row=0, column=1, padx=20, pady=5, rowspan=2, sticky="nsew")

    output_text = tkinter.Text(output_frame, width=110, height=34, fg="white", bg="black")
    output_text.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

#COMMAND FRAME
#=======================================================================================================#
    command_frame = tkinter.LabelFrame(container_frame, text="COMMAND", bg="#303030", fg="lightgray")
    command_frame.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

    command_line = tkinter.Text(command_frame, width=105, height=2, fg="white", bg="black")
    command_line.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
    command_line.bind("<Return>", Listener.execute_command)


#=======================================================================================================#
    version_label = tkinter.Label(_frame, text="Listener 1.4", bg="#303030", fg="lightgray")
    version_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    devops_label = tkinter.Label(_frame, text="Developed By Atahan Poyraz", bg="#303030", fg="lightgray")
    devops_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

#SHOW WINDOW
#=======================================================================================================#
    for widget in container_frame.winfo_children():
        widget.grid_configure(padx=6, pady=3)

window.mainloop()
