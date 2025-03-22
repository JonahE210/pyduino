import multiprocessing
import subprocess
import json
class MultiprocessingArduinoCLI:
    def __init__(self):
        """Initialize multiprocessing and subprocess management."""
        self.process = None

    def run_command(self, command):
        """
        Runs an Arduino CLI command in a subprocess.
        :param command: List of command arguments to run in the terminal.
        :return: Tuple (stdout, stderr)
        """
        try:
            # start subprocess
            self.process = subprocess.Popen(
                command,
                # stdout is the field parameter to capture output, and stderr captures errors
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # parent process waits for completion
            stdout, stderr = self.process.communicate()

            return stdout, stderr
        except Exception as e:
            return None, str(e)

    def run_arduino_task(self, task):
        """
        Executes Arduino-related tasks: board selection, compile, upload.
        :param task: Dictionary containing task type and relevant parameters.
        :return: Tuple (stdout, stderr)
        """
        command = []

        if task["type"] == "board_list":
            command = ["arduino-cli", "board", "list"]
        elif task["type"] == "compile":
            command = ["arduino-cli", "compile", "--fqbn", task["fqbn"], task["sketch"]]
        elif task["type"] == "upload":
            command = ["arduino-cli", "upload", "-p", task["port"], "--fqbn", task["fqbn"], task["sketch"]]
        else:
            return None, f"Unknown task type: {task['type']}"

        return self.run_command(command)

    def run_tasks_parallel(self, tasks):
        """
        Executes multiple Arduino CLI tasks in parallel.
        :param tasks: List of task dictionaries.
        :return: List of tuples (stdout, stderr)
        """
        results = []
        processes = []

        # create queue for results
        results_queue = multiprocessing.Queue()
        # using this instead of Manager.queue since manager is
        # doesn't like working properly
        # (native to multiprocessing)
        def worker(task):
            stdout, stderr = self.run_arduino_task(task)
            results_queue.put((stdout, stderr))

        # starts multiprocessing tasks
        for task in tasks:
            p = multiprocessing.Process(target=worker, args=(task,))
            processes.append(p)
            p.start()

        # ensures all processes complete
        for p in processes:
            p.join()

        # collect results
        while not results_queue.empty():
            results.append(results_queue.get())

        return results

    def terminate_subprocess(self):
        """Kills the child process after execution."""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            print("Subprocess terminated.")


    def send_data(self, data, tags, *args, **kwargs):
        pass

