#!/usr/bin/env python3

import logging
import os.path
import socket
import time

from shared import PORT, HOST, ADDR, LOGFORMAT, STORAGE_FOLDER,\
    handle_header, output, recv_file, send_file, send_msg


TEST_RESULTS_FILE = "/media/findux/DATA/Documents/Malta_II/server/fake_results_for_server_test.txt"

def handle_client(conn, target_dir=STORAGE_FOLDER) -> bool:
    """
    :param conn:
    :return: connected. (whether socket is still connected).
    """
    header_code, header_content = handle_header(conn)
    output("HEADER", f"{header_code} header received.")

    connected = True
    EOT_triggered = False
    files_received = 0

    if header_code == "EB":
        output("CONN", "Empty byte received. Closing connection")
        conn.close()
        connected = False
    elif header_code == "MSG":
        message = header_content[0]
        output("MSG", f"Received message: {message}")
        if message == "EOT":
            EOT_triggered = True
    elif header_code == "FT":
        if len(header_content) != 2:  # If header content is not [fname, fsize]
            output("ERROR", f"Wrong header content length. Expected 2, got {len(header_content)}")
            output("MSG", "REFUSE")
            logging.debug("Sending REFUSE message.")
            send_msg("REFUSE", conn)
            logging.info("Closing connection.")
            conn.close()
            connected = False
        else:
            fname, fsize = header_content
            fpath_dst = os.path.join(target_dir, fname)
            if os.path.isfile(fpath_dst):  # Refuse if file exists.
                logging.info("File already exists. Refusing...")
                send_msg("REFUSE", conn)
                conn.close()
                connected = False
            else:  # Send accept msg
                output("MSG", "ACCEPT")
                send_msg("ACCEPT", conn)
                recv_success = recv_file(fname, fsize=int(fsize), fdir_dst=target_dir, conn=conn)
                logging.debug(f"File receive successful: {recv_success}")
                if recv_success:
                    send_msg("OK", conn)
                    files_received += 1
                else:
                    send_msg("ERROR", conn)
                    conn.close()
                    connected = False
    elif header_code == "EOT":
        EOT_triggered = True


    return connected, files_received, EOT_triggered


def run_server(port=PORT, host=HOST):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(ADDR)
        server.listen()
        print(f"------------------------------------------------\n"
              f"Starting server.\n"
              f"HOST: {HOST}\n"
              f"PORT: {PORT}\n"
              f"------------------------------------------------\n")

        while True:
            output("SERVER", "... listening ...")
            conn, addr = server.accept()
            connected = True
            total_files_received = 0
            while connected:
                connected, file_received, EOT_triggered= handle_client(conn)
                total_files_received += file_received
                if EOT_triggered:
                    break

            if EOT_triggered:
                conn, addr = server.accept()
                output("EOT", "Starting object detection....")
                send_msg("Starting object detection... please wait.", conn)
                print(" ... brrrrrrrrrrrrrrr.....")
                time.sleep(3)
                send_file(conn, TEST_RESULTS_FILE)  # ToDo: update to use actual file
                # ToDo: on Error: try five times to resend it.
                conn.close()



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format=LOGFORMAT)
    logging.disable()

    run_server()
