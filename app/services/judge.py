import os
import tempfile
import subprocess
import time
from typing import Tuple
from bson import ObjectId

from repositories import (
    submission_repo,
    submission_result_repo,
    test_case_repo,
    problem_repo
)


class JudgeService:
    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.docker_images = {
            'python': 'python:3.12-slim',
            'python3': 'python:3.12-slim',
            'cpp': 'gcc:11.2.0',
            'c': 'gcc:11.2.0',
            'java': 'openjdk:17-slim',
            'go': 'golang:1.18-alpine'
        }
        self.file_extensions = {
            'python': '.py',
            'python3': '.py',
            'cpp': '.cpp',
            'c': '.c',
            'java': '.java',
            'go': '.go'
        }
        self.run_commands = {
            'python': ['python', '{file}'],
            'python3': ['python3', '{file}'],
            'cpp': ['{executable}'],
            'c': ['{executable}'],
            'java': ['java', '{class}'],
            'go': ['{executable}']
        }
        self.compile_commands = {
            'python': None,
            'python3': None,
            'cpp': ['g++', '-O2', '-o', '{executable}', '{file}'],
            'c': ['gcc', '-O2', '-o', '{executable}', '{file}'],
            'java': ['javac', '{file}'],
            'go': ['go', 'build', '-o', '{executable}', '{file}']
        }

    def judge_submission(self, submission_id: str) -> bool:
        submission = submission_repo.find_by_id(submission_id)
        if not submission:
            return False

        problem = problem_repo.find_by_id(str(submission.problem_id.id))
        if not problem:
            return False

        submission_result_repo.clear_for_submission(submission_id)

        test_cases = test_case_repo.find_by_problem(str(problem.id))

        if not test_cases:
            return False

        with tempfile.TemporaryDirectory(dir=self.temp_dir) as temp_dir:
            file_path, executable_path, class_name = self._prepare_files(
                temp_dir,
                submission.code,
                submission.language
            )

            compile_success, compile_error = self._compile_code(
                submission.language,
                file_path,
                executable_path
            )

            if not compile_success:
                for test_case in test_cases:
                    submission_result_repo.create({
                        'submission_id': ObjectId(submission_id),
                        'test_case_id': test_case.id,
                        'status': 'Compilation Error',
                        'execution_time': 0,
                        'memory_used': 0,
                        'error': compile_error
                    })
                return True

            for test_case in test_cases:
                status, exec_time, memory, error = self._run_test(
                    submission.language,
                    file_path,
                    executable_path,
                    class_name,
                    test_case.input_data,
                    test_case.expected_output,
                    problem.time_limit,
                    problem.memory_limit
                )

                submission_result_repo.create({
                    'submission_id': ObjectId(submission_id),
                    'test_case_id': test_case.id,
                    'status': status,
                    'execution_time': exec_time,
                    'memory_used': memory,
                    'error': error
                })

        if submission_id:
            self._update_submission_status(submission_id)
        else:
            raise ValueError("submission_id is required but not provided")

        return True

    def _prepare_files(self, temp_dir: str, code: str, language: str) -> Tuple[str, str, str]:
        file_extension = self.file_extensions.get(language, '.txt')
        filename = f"solution{file_extension}"
        file_path = os.path.join(temp_dir, filename)

        with open(file_path, 'w') as f:
            f.write(code)

        executable_path = os.path.join(temp_dir, 'solution')

        class_name = 'Solution'
        if language == 'java':
            for line in code.split('\n'):
                if 'public class' in line:
                    parts = line.split('public class')[1].strip().split(' ')
                    class_name = parts[0].split('{')[0].strip()
                    break
            new_filename = f"{class_name}.java"
            new_file_path = os.path.join(temp_dir, new_filename)
            os.rename(file_path, new_file_path)
            file_path = new_file_path

        return file_path, executable_path, class_name

    def _compile_code(self, language: str, file_path: str, executable_path: str) -> Tuple[bool, str]:
        compile_command = self.compile_commands.get(language)

        if not compile_command:
            return True, ""

        command = []
        for part in compile_command:
            if '{file}' in part:
                part = part.replace('{file}', file_path)
            elif '{executable}' in part:
                part = part.replace('{executable}', executable_path)
            command.append(part)

        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )

            if process.returncode != 0:
                return False, process.stderr

            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Compilation timed out"
        except Exception as e:
            return False, str(e)

    def _run_test(
            self,
            language: str,
            file_path: str,
            executable_path: str,
            class_name: str,
            input_data: str,
            expected_output: str,
            time_limit: float,
            memory_limit: int
    ) -> Tuple[str, float, int, str]:
        input_file = os.path.join(os.path.dirname(file_path), 'input.txt')
        with open(input_file, 'w') as f:
            f.write(input_data or "")

        docker_image = self.docker_images.get(language, 'python:3.12-slim')

        run_command = self.run_commands.get(language, ['python', '{file}'])
        cmd_parts = []

        for part in run_command:
            if '{file}' in part:
                part = part.replace('{file}', os.path.basename(file_path))
            elif '{executable}' in part:
                part = part.replace('{executable}', os.path.basename(executable_path))
            elif '{class}' in part:
                part = part.replace('{class}', class_name)
            cmd_parts.append(part)

        docker_cmd = [
            'docker', 'run',
            '--rm',
            '--network', 'none',
            f'--cpus={max(0.1, time_limit / 2)}',
            f'--memory={memory_limit}m',
            '--memory-swap=-1',
            '-v', f'{os.path.dirname(file_path)}:/app',
            '-w', '/app',
            '--ulimit', f'cpu={int(time_limit + 1)}',
            docker_image,
            'sh', '-c',
            f'cd /app && cat input.txt | timeout {time_limit}s {" ".join(cmd_parts)} > output.txt 2> error.txt'
        ]

        start_time = time.time()
        try:
            process = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=time_limit * 2
            )

            exec_time = time.time() - start_time

            output_file = os.path.join(os.path.dirname(file_path), 'output.txt')
            error_file = os.path.join(os.path.dirname(file_path), 'error.txt')

            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    output = f.read()
            else:
                output = ""

            if os.path.exists(error_file):
                with open(error_file, 'r') as f:
                    error = f.read()
            else:
                error = ""

            memory_used = 0

            try:
                if process.stdout:
                    pass
            except (OSError, subprocess.SubprocessError):
                memory_used = 0

            if process.returncode != 0:
                if process.returncode == 124 or process.returncode == 137:
                    return "Time Limit Exceeded", exec_time, memory_used, error
                else:
                    return "Runtime Error", exec_time, memory_used, error

            output = output.strip()
            expected = (expected_output or "").strip()

            if output == expected:
                return "Accepted", exec_time, memory_used, ""
            else:
                return "Wrong Answer", exec_time, memory_used, ""

        except subprocess.TimeoutExpired:
            return "Time Limit Exceeded", time_limit, 0, "Execution timed out"
        except Exception as e:
            return "Runtime Error", 0, 0, str(e)

    @staticmethod
    def _update_submission_status(submission_id: str) -> None:
        results = submission_result_repo.find_by_submission(submission_id)

        if not results:
            submission_repo.update(submission_id, {'status': 'Error'})
            return

        statuses = [result.status for result in results]
        if all(status == 'Accepted' for status in statuses):
            overall_status = 'Accepted'
        elif 'Compilation Error' in statuses:
            overall_status = 'Compilation Error'
        elif 'Runtime Error' in statuses:
            overall_status = 'Runtime Error'
        elif 'Time Limit Exceeded' in statuses:
            overall_status = 'Time Limit Exceeded'
        elif 'Wrong Answer' in statuses:
            overall_status = 'Wrong Answer'
        else:
            overall_status = 'Unknown'

        submission_repo.update(submission_id, {'status': overall_status})
