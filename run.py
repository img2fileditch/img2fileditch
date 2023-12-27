import multiprocessing
import subprocess

if __name__ == '__main__':
    # Define the commands to run each Flask server
    command_app1 = ['python', 'main.py']
    command_app2 = ['python', 'bot.py']

    # Create separate processes for each Flask server
    process_app1 = multiprocessing.Process(target=subprocess.run, args=(command_app1,))
    process_app2 = multiprocessing.Process(target=subprocess.run, args=(command_app2,))

    # Start both processes
    process_app1.start()
    process_app2.start()

    # Wait for both processes to finish
    process_app1.join()
    process_app2.join()
