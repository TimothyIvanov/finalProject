# main.py
from retrieve_sites import retrieve_sites
from retrieve_data import retrieve_data_from_sites
from process_data import process_data_from_sites
from utils import print_status, handle_errors

def main():
    print('Starting the application...')

    try:
        print_status("Retrieving sites", "in progress")
        retrieve_sites()
        print_status("Sites retrieved", "completed")

        print_status("Retrieving data from sites", "in progress")
        retrieve_data_from_sites()
        print_status("Data retrieved", "completed")

        print_status("Processing data", "in progress")
        process_data_from_sites()
        print_status("Data processed", "completed")

    except Exception as e:
        handle_errors(e)

if __name__ == '__main__':
    main()
