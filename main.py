#!usr/bin/python3
import argparse
import sniffles
import parse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='sniffles', description='''Sniff 
                        packets received over Ethernet. Use on a Linux 
                        machine with construct version at least 2.9.39.''')
    
    parser.add_argument('interface', metavar='INTERFACE',
                        help='Interface to listen for traffic on.')
    parser.add_argument('-t', '--timeout', type=int, default=0,
                        help='''Time to capture for (in seconds). If set to 0 or
                        unspecified, ^C must be sent to close the program.''')
    
    format_parser = parser.add_mutually_exclusive_group()
    format_parser.add_argument('-x', '--hexdump', action='store_true',
                               help='Write hexdump to stdout.')
    format_parser.add_argument('-o', '--outfile', metavar='OUTFILE',
                               help='Write pcapng to a file.')
    format_parser.add_argument('-p', '--protocols', nargs='+',
                               default=list(parse.HEADERS),
                               choices=list(parse.HEADERS),
                               help='''Write human-readable output for the 
                               specified protocol(s) to stdout.''')
    
    kwargs = vars(parser.parse_args())
    sniffer = sniffles.Sniffer(kwargs.pop('interface'))
    timeout = kwargs.pop('timeout')

    if kwargs.pop('hexdump'):
        sniffer.sniff('hexdump', timeout, **kwargs)
    elif kwargs['outfile'] is not None:
        sniffer.sniff('outfile', timeout, **kwargs)
    else:  # outfile
        kwargs['protocols'] = list(parse.HEADERS)
        sniffer.sniff('protocols', timeout, **kwargs)
