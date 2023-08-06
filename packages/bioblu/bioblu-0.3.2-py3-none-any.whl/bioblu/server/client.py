#!/usr/bin/env python3

import logging
import os
import socket

from shared import LOGFORMAT, send_all_files, recv_file, handle_header, initiate_socket, output, send_msg


def recv_results(fdir_dst, conn = None):
    if conn is None:
        conn = initiate_socket()  # Will this be handled after the server is done with the prediction?

    header_code, msg = handle_header(conn=conn)
    output("MSG", msg[0])

    header_code, (fname, fsize) = handle_header(conn=conn)
    output("RESULTS", f"{fname}, {int(fsize)} bytes.")
    send_msg("ACCEPT", conn)
    recv_file(fname=fname, fsize=fsize, fdir_dst=fdir_dst, conn=conn)
    send_msg("OK", conn)
    conn.close()


def main(fdir, results_fdir):
    send_all_files(fdir)
    recv_results(fdir_dst=results_fdir)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format=LOGFORMAT)
    logging.disable()

    fdir = "/media/findux/DATA/Documents/Malta_II/demo/demo_dataset/imgs/"
    results_fdir = "/home/findux/Desktop/"
    main(fdir, results_fdir)

