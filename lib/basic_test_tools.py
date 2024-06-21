import subprocess
import traceback

from lib.log_tools import log


class BasicTestTools:
    """
    basic test tools including adb fastboot
    """

    def __init__(self, sn="", logger=None):
        self.logger = logger or log.logger
        self.sn = sn

    @staticmethod
    def cmder(cmd, timeout=None, shell=True):
        """
        run cmd by local shell, eg: shell or cmd or powershell
        Args:
            cmd: 要执行的命令
            timeout: 等待命令执行完成的延迟时间
            shell: True使用cmd执行命令，False可指定执行程序

        Returns: 命令执行状态, 命令执行返回结果

        """
        sp = subprocess.Popen(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = sp.communicate(timeout=timeout)
        out = out.decode(encoding='utf-8', errors='ignore') if out else ''
        err = err.decode(encoding='utf-8', errors='ignore') if err else ''
        out = '\n'.join([line_strip for line in out.splitlines() if (line_strip := line.strip()) != ""])
        err = '\n'.join([line_strip for line in err.splitlines() if (line_strip := line.strip()) != ""])
        if sp.returncode == 0:
            return True, f'{out}\n{err}'
        else:
            return False, f'{out}\n{err}'

    def _cmd_sn_wrapper(self, cmd):
        """
        给adb命令添加设备sn
        Args:
            cmd: 设备sn

        Returns:

        """
        if self.sn == "":
            return cmd
        sn_clause = f" -s {self.sn}"
        if "adb" in cmd:
            return cmd.replace("adb", f"adb{sn_clause}")
        elif "fastboot" in cmd:
            return cmd.replace("fastboot", f"fastboot{sn_clause}")

    def add_sn_to_exec(self, cmd):
        """
        add sn to cmd if sn is not blank
        Args:
            cmd:

        Returns:

        """
        if self.sn == "":
            return cmd
        else:
            return f'{cmd} -s {self.sn}'

    def _process_cmd(self, exec_cmd, verbosity):
        """
        process cmd
        Args:
            exec_cmd:
            verbosity:

        Returns:

        """
        if verbosity >= 1:
            self.logger.info(exec_cmd)
        try:
            state, ret = self.cmder(exec_cmd)
            ret = ret.strip()
        except Exception:
            log.logger.error(traceback.format_exc())
            return False, ""
        if verbosity >= 2:
            if state is True:
                self.logger.info(f'{state}\n{ret}')
            else:
                self.logger.error(f'{state}\n{ret}')
        return state, ret

    def adb_exec(self, cmd, verbosity=2):
        """
        执行adb命令，并打印命令和执行结果
        Args:
            cmd: 命令
            verbosity: 是否打印命令和结果

        Returns:

        """
        exec_cmd = f"{self.add_sn_to_exec('adb')} {cmd}"
        return self._process_cmd(exec_cmd, verbosity)

    def adb_shell(self, cmd, verbosity=2):
        """
        执行adb shell命令，并打印命令和执行结果
        Args:
            cmd: adb shell命令
            verbosity: 是否打印结果
        """
        shell_cmd = f'{self.add_sn_to_exec("adb")} shell "{cmd}"'
        return self._process_cmd(shell_cmd, verbosity)

    def fastboot_exec(self, cmd, verbosity=2):
        """
        execute cmd by fastboot
        Args:
            cmd:
            verbosity:

        Returns:

        """
        exec_cmd = f"{self.add_sn_to_exec('fastboot')} {cmd}"
        return self._process_cmd(exec_cmd, verbosity)


if __name__ == '__main__':
    bt = BasicTestTools()
    bt.adb_exec('help')
