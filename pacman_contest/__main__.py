import json
import logging

from .pacman_html_generator import HtmlGenerator
from .pacman_ssh_contest import load_settings, ContestRunner
from .cluster_manager import Host

if __name__ == '__main__':
    settings = load_settings()

    # from getpass import getuser

    # prompt for password (for password authentication or if private key is password protected)
    # hosts = [Host(no_cpu=2, hostname='localhost', username=getuser(), password=getpass(), key_filename=None)]
    # use this if no pass is necessary (for private key authentication)
    # hosts = [Host(no_cpu=2, hostname='localhost', username=getuser(), password=None, key_filename=None)]

    with open(settings['workers_file'], 'r') as f:
        workers_details = json.load(f)['workers']
        logging.info("Host workers details to be used: {}".format(workers_details))

    hosts = [Host(no_cpu=w['no_cpu'], hostname=w['hostname'], username=w['username'], password=w['password'],
                  key_filename=w['private_key_file'], key_password=w['private_key_password']) for w in workers_details]
    del settings['workers_file']


    logging.info("Will create contest runner with options: {}".format(settings))
    runner = ContestRunner(**settings)  # Setup ContestRunner
    runner.run_contest_remotely(hosts)  # Now run ContestRunner with the hosts!

    stats_file_url, replays_file_url, logs_file_url = runner.store_results()
    html_generator = HtmlGenerator(settings['www_dir'], settings['organizer'])
    html_generator.add_run(runner.contest_timestamp_id, stats_file_url, replays_file_url, logs_file_url)
    logging.info("Web pages generated. Now cleaning up and closing... Thank you!")

    runner.clean_up()
