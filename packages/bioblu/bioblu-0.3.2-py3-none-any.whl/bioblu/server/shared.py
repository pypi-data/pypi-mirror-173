#!/usr/bin/env python3
import logging
import os
from pathlib import Path
import socket
from typing import List

HOST = socket.gethostbyname(socket.gethostname())  # ToDo: hardcode this eventually.
PORT = 5050
ADDR = (HOST, PORT)
BUFFER_SIZE = 4096
HEADER_LEN = 128  # Header length (when in bytes)
TRANSMISSION_CODES = ["FT", "MSG"]  # File_transfer: FT, Message: MSG, EOT
STORAGE_FOLDER = "/media/findux/DATA/Documents/Malta_II/server/storage/"
ENCODING = "utf-8"
SEP = "<sep>"
LOGFORMAT = f"[ %(levelname)s ]\t%(funcName)10s\t%(message)s"



def get_fpaths(fdir, recursive = False) -> List[str]:
    """Returns a list with the abs. paths to every file and folder in the provided dir."""
    if recursive:
        file_paths = [str(path) for path in Path(fdir).rglob('*')]
    else:
        file_paths = [os.path.join(fdir, fname) for fname in sorted(os.listdir(fdir))]
    return file_paths


def folder_has_subfolders(fdir) -> bool:
    fpaths = get_fpaths(fdir, recursive=False)
    return any([os.path.isdir(fp) for fp in fpaths])


def output(o_type: str, msg: str):
    print(f"[{o_type.center(10, ' ')}]".ljust(25), msg)


def initiate_socket(host=HOST, port=PORT):
    logging.debug("Initiating socket...")
    addr = (host, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    logging.debug("Socket created.")
    return client


def create_header(header_code: str, content: str):
    assert header_code in TRANSMISSION_CODES
    if header_code == "FT":
        try:
            fname = os.path.basename(content)
            fsize = os.path.getsize(content)
        except FileNotFoundError:
            output("ERROR", f"File not found: {content}")
            return None
        header_elements = [header_code, fname, str(fsize)]
    else:
        header_elements = [header_code, content]

    # Assemble header
    header = SEP.join(header_elements)
    header_b = header.encode(ENCODING)
    if len(header_b) > HEADER_LEN:
        output("WARNING", f"Header length exceeded: {len(header_b)}")
        header_b = header_b[:HEADER_LEN + 1]
    # Pad header:
    header_b += b" " * (HEADER_LEN - len(header_b))
    return header_b


def send_msg(msg: str, conn):
    msg_b = msg.encode(ENCODING)
    msg_len = len(msg_b)

    message = f"MSG{SEP}{msg}"
    message_b = message.encode(ENCODING)
    assert len(message_b) <= HEADER_LEN
    message_b += b" " * (HEADER_LEN - len(message_b))
    output("MSG", f"Sending msg: {msg}")
    conn.sendall(message_b)


def send_file(conn, fpath):
    assert os.path.isfile(fpath)

    fname = os.path.basename(fpath)

    # Send header:
    header: bytes = create_header("FT", fpath)
    logging.debug("Sending header...")
    conn.sendall(header)

    # Wait for response:
    logging.debug("Waiting for file accept.")
    header_code, header_content = handle_header(conn)
    assert header_code == "MSG"
    msg = header_content[0]
    output("SERVER", msg)

    # Send file:
    if msg == "REFUSE":
        output("CONN", "Closing connection")
        conn.close()
    elif msg == "ACCEPT":
        output("CONN", f"Sending file {fname} ...")
        with open(fpath, "rb") as f:
            outbound_data = f.read()
        conn.sendall(outbound_data)
        logging.debug(f"Done transmitting file. Using .shutdown(1) on socket.")
        conn.shutdown(1)  # Se

        # Get receipt confirmation:
        header_code, header_content = handle_header(conn)
        assert header_code == "MSG"
        conf_msg = header_content[0]
        output("SERVER", conf_msg)
        conn.close()


def send_all_files(fdir):
    assert not folder_has_subfolders(fdir)
    fpaths = get_fpaths(fdir)
    for fpath in fpaths:
        conn = initiate_socket()
        logging.info(f"Processing file {fpath}")
        send_file(conn, fpath)
    conn = initiate_socket()
    send_msg("EOT", conn)
    conn.close()


def recv_file(fname: str, fsize: int, fdir_dst: str, conn=None) -> bool:
    """

    :param fname:
    :param fsize:
    :param fdir_dst:
    :param conn:
    :return: bool: file received and saved successfully.
    """
    fpath_dst = os.path.join(fdir_dst, fname)
    if conn is None:
        conn = initiate_socket()
    logging.info(f"Writing file to: {fpath_dst}")
    while True:  # Loop unntil the file is fully received
        received_bytes = conn.recv(BUFFER_SIZE)
        if len(received_bytes) < BUFFER_SIZE:
            logging.debug(f"Latest batch: {len(received_bytes)} bytes received.")
            # ToDo: consider padding the data.
        if received_bytes:
            with open(fpath_dst, "ab") as f:
                f.write(received_bytes)
        if received_bytes == b"":
            output("EOF", "Reached end of file.")
            break

        # filesizes_match = os.path.getsize(fpath_dst) == fsize
        # logging.debug(f"Filesizes match: {filesizes_match}, ({os.path.getsize(fpath_dst):,}, {fsize:,})")
        # if filesizes_match:
        #     break
    if os.path.getsize(fpath_dst) == fsize:
        return True
    else:
        return False


def handle_header(conn: socket):
    raw_header: bytes = conn.recv(HEADER_LEN)
    code, header_contents = "", []
    if raw_header == b"":
        logging.info("Empty byte.")
        code = "EB"
    else:
        logging.debug(f"Raw header: {raw_header}")
        header: str = raw_header.decode(ENCODING)
        code, *header_contents = header.split(SEP)

    if code == "MSG":
        header_contents[0] = str(header_contents[0]).strip()
    return code, header_contents


if __name__ == "__main__":
    header = create_header("MSG", "fucktheduck")
    print(header)
    header = create_header("FT", "/media/findux/DATA/Documents/Malta_II/server/fake_results_for_server_test.txt")
    print(header)
