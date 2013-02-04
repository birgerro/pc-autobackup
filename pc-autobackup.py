#!/usr/bin/python
#
# Copyright 2013 Jeff Rebeiro (jeff@rebeiro.net) All rights reserved
# Main runnable for PC Autobackup

__author__ = 'jeff@rebeiro.net (Jeff Rebeiro)'

import logging
import optparse

from twisted.internet import reactor
from twisted.web.server import Site

import common
import ssdp
import mediaserver


def main():
  parser = optparse.OptionParser()
  parser.add_option('-b', '--bind', dest='bind',
                    help='bind the server to a specific IP',
                    metavar='IP')
  parser.add_option('-d', '--debug', dest='debug', action='store_true',
                    default=False, help='debug output')
  parser.add_option('--log_file', dest='log_file',
                    help='output log to file', metavar='FILE')
  parser.add_option('-o', '--output_dir', dest='output_dir',
                    help='output directory for files', metavar='DIR')
  parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
                    default=False, help='verbose output')
  (options, args) = parser.parse_args()

  logging_options = {'level': logging.WARN}

  if options.verbose:
    logging_options['level'] = logging.INFO
  if options.debug:
    logging_options['level'] = logging.DEBUG
  if options.log_file:
    logging_options['filename'] = options.log_file

  logging.basicConfig(**logging_options)

  logging.info('pc-autobackup started')

  config = common.LoadOrCreateConfig()
  if options.bind:
    config.set('AUTOBACKUP', 'default_interface', options.bind)
  if options.output_dir:
    config.set('AUTOBACKUP', 'backup_dir', options.output_dir)

  resource = mediaserver.MediaServer()
  factory = Site(resource)
  reactor.listenMulticast(1900, ssdp.SSDPServer())
  logging.info('SSDPServer started')
  reactor.listenTCP(52235, factory)
  logging.info('MediaServer started')
  reactor.run()


if __name__ == '__main__':
  main()
