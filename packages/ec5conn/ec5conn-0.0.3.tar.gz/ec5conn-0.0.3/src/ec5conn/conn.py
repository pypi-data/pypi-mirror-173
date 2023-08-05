#!/usr/bin/env python

import os
import re
import socket
import struct
import sys
import time
import errno

import argparse
import logging
import pydash as _
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)
from .log import clilog

from ping3 import ping, verbose_ping, IP_HEADER_FORMAT, ICMP_HEADER_FORMAT, ICMP_TIME_FORMAT

logger = logging.getLogger(__name__)

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

protocol_meta = {
    'MYSQL': {
        'port': 3306,
        'user': 'root',
        'database': 'mydb',
    },
    'MONGO': {
        'port': 27017,
        'user': 'root',
        'database': 'mydb',
    },
    'TCP': {
        'port': 3306,
    },
    'ICMP': {
        'port': 0,
    },
}


class DestValidator(Validator):
    domain_pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z0-9]{2,3})$'
    )

    def validate(self, value):
        if len(value.text):
            if self.domain_pattern.match(value.text):
                return True
            else:
                parts = value.text.split('.')
                if len(parts) == 4 and all(x.isdigit() for x in parts):
                    numbers = list(int(x) for x in parts)
                    return all(num >= 0 and num < 256 for num in numbers)
                else:
                    raise ValidationError(
                        message="Invalid destination",
                        cursor_position=len(value.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


class PortValidator(Validator):
    def validate(self, value):
        if len(value.text):
            try:
                port = int(value.text)
                if _.is_number(port) and 1 <= port <= 65535:
                    return True
                else:
                    raise ValidationError(
                        message="Invalid port",
                        cursor_position=len(value.text))
            except Exception as err:
                raise ValidationError(
                    message="Invalid port",
                    cursor_position=len(value.text))
        else:
            # use default
            pass


class Conn(object):
    def __init__(self, answers):
        self._dest = _.get(answers, 'dest')
        if not self._dest:
            raise ValueError('Destination not specified')
        self._hostname = socket.gethostname()
        _hostname, _aliases, self._src_addr = socket.gethostbyname_ex(
            self._hostname)
        try:
            # Domain name will translated into IP address, and IP address leaves unchanged.
            _hostname, _aliases, self._dst_addrs = socket.gethostbyname_ex(
                self._dest)
            self._dst_addr = socket.gethostbyname(self._dest)
        except Exception as err:
            raise Exception(
                f'목적지의 호스트를 조회할 수 없습니다. dest={self._dest}, err={str(err)}')
        self._protocol = _.get(answers, 'protocol', 'ICMP')
        self._port = _.get(answers, 'port', 0)
        self._user = _.get(answers, 'user')
        self._password = _.get(answers, 'password')
        self._database = _.get(answers, 'database')

        self._timeout = _.get(answers, 'timeout', 1)
        self._verbose = _.get(answers, 'verbose', False)

        self._last_error = None
        self.results = {}

    def desc(self):
        clilog(f'- 출발지: {self._hostname} ({self._src_addr})', 'blue')
        clilog(f'- 목적지: {self._dest} ({self._dst_addr})', 'blue')
        clilog(f'- 프로토콜: {self._protocol}', 'blue')
        if self._port:
            clilog(f'- 포트: {self._port}', 'blue')

    def report(self):
        clilog('[Report]', 'yellow')
        self.desc()
        os_errnos = []
        actions = []
        for _key, item, in self.results.items():
            value = _.get(item, 'value')
            if value:
                msg = f"- {_.get(item, 'title')}: {_.get(item, 'value')}"
                if _.is_number(value):
                    msg += f" {_.get(item, 'unit', '')}"
                clilog(msg, 'blue')
                _errno = _.get(item, 'errno')
                if _errno:
                    if _errno in errno.errorcode.keys():
                        os_errnos.append(_errno)
                        os_errnos = _.uniq(os_errnos)
                _action = _.get(item, 'action')
                if _action:
                    actions.append(_action)

        if _.is_empty(os_errnos) and _.is_empty(actions):
            return

        clilog('[에러 조치]', 'red')
        net_err_mesgs = []
        net_errnos = [errno.EHOSTUNREACH, errno.ENETUNREACH,
                      errno.ETIMEDOUT, errno.ECONNREFUSED, errno.ECONNRESET]
        for _errno in os_errnos[:]:
            errno.errorcode
            if _errno in net_errnos:
                net_err_mesgs.append(
                    f'> [Errno {_errno}] {os.strerror(_errno)}')
                os_errnos.remove(_errno)

        if net_err_mesgs:
            net_err_mesgs = _.push(net_err_mesgs,
                                   '1. 목적지 입력(ip,domain,port)이 올바른지 확인하십시오.',
                                   '2. 목적지 서버가 down 상태인지 확인하십시오.',
                                   '3. 네트워크 경로 또는 목적지 서버의 보안정책(firewall,iptables)을 확인하십시오.',
                                   )
            msg = _.join(net_err_mesgs, '\n')
            clilog(msg, 'red')

        etc_errs = []
        for _errno in os_errnos:
            etc_errs.append(f'> {os.strerror(_errno)}')
            if _errno == errno.EPERM:
                etc_errs.append('sudo 또는 관리자-권한이 필요합니다.')
            else:
                etc_errs.append('조치사항 확인 안됨')
        if etc_errs:
            msg = _.join(etc_errs, '\n')
            clilog(msg, 'red')

        if actions:
            msg = _.join(actions, '\n')
            clilog(msg, 'red')

    def test_ping(self):
        clilog('[Test Ping]', 'yellow')
        ret = None
        result = {
            'value': None,
            'title': 'Ping',
            'unit': 'ms',
            'errno': None,
            'action': None,
        }
        try:
            # if self._verbose:
            #     verbose_ping(self._dst_addr, 4, timeout=self._timeout)
            verbose_ping(self._dst_addr, 3, timeout=self._timeout)
            ret = ping(self._dest, self._timeout, 'ms')
            if _.is_float(ret):
                ret = _.ceil(ret, 1)
        except KeyboardInterrupt:
            ret = -1
        except Exception as err:
            ret = -2
            result['errno'] = _.get(err, 'errno')
            result['value'] = str(err)

        if ret == -1:
            result['value'] = 'KeyboardInterrupt'
            rc = False
        elif ret == -2:
            rc = False
        elif ret == None:
            result['value'] = 'Request timeout for ICMP packet.'
            result['errno'] = errno.ETIMEDOUT
            # clilog('Ping Timeout', 'red')
            rc = False
        elif ret == False:
            result['value'] = 'Ping Error'
            # clilog('Ping Error', 'red')
            rc = False
        else:
            result['value'] = ret
            rc = True

        self.results['ping'] = result

        return rc

    def test_traceroute(self):
        clilog('[Test Traceroute]', 'yellow')
        ret = None
        result = {
            'value': None,
            'title': 'Traceroute',
            'unit': 'ms',
            'errno': None,
            'action': None,
        }
        # https://gist.github.com/pnc/502451
        dest_addr = socket.gethostbyname(self._dst_addr)
        port = 33434
        max_hops = 30
        icmp = socket.getprotobyname('icmp')
        udp = socket.getprotobyname('udp')
        ttl = 1

        try:
            clilog(
                f'traceroute to {self._dest} ({dest_addr}), {max_hops} hops max')

            while True:
                try:
                    recv_socket = socket.socket(
                        socket.AF_INET, socket.SOCK_RAW, icmp)
                except PermissionError as err:
                    # [Errno 1] Operation not permitted
                    if err.errno == errno.EPERM:
                        recv_socket = socket.socket(
                            socket.AF_INET, socket.SOCK_DGRAM, icmp)
                    else:
                        raise err
                send_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_DGRAM, udp)
                send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

                # Build the GNU timeval struct (seconds, microseconds)
                timeout = struct.pack("ll", self._timeout, 0)

                # Set the receive timeout so we behave more like regular traceroute
                recv_socket.setsockopt(
                    socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)

                recv_socket.bind(("", port))
                sys.stdout.write(" %d  " % ttl)
                time_sent = time.time()
                send_socket.sendto("".encode(), (dest_addr, port))
                curr_addr = None
                curr_name = None
                finished = False
                tries = 3
                while not finished and tries > 0:
                    try:
                        _recv_data, curr_addr = recv_socket.recvfrom(512)
                        time_recv = time.time()
                        rtt = _.ceil((time_recv - time_sent) * 1000, 1)
                        sys.stdout.write(f"{rtt} ms ")
                        finished = True
                        curr_addr = curr_addr[0]
                        try:
                            curr_name = socket.gethostbyaddr(curr_addr)[0]
                        except socket.error:
                            curr_name = curr_addr
                    except socket.error as err:
                        tries = tries - 1
                        sys.stdout.write("* ")

                send_socket.close()
                recv_socket.close()

                if not finished:
                    pass

                if curr_addr is not None:
                    curr_host = "%s (%s)" % (curr_name, curr_addr)
                else:
                    curr_host = ""
                sys.stdout.write("%s\n" % (curr_host))

                if curr_addr == dest_addr:
                    ret = ttl
                    break
                ttl += 1
                if ttl > max_hops:
                    ret = -99
                    break
        except KeyboardInterrupt:
            ret = -1
        except Exception as err:
            ret = -2
            result['errno'] = _.get(err, 'errno')
            result['value'] = str(err)

        if ret == -1:
            result['value'] = 'KeyboardInterrupt'
            rc = False
        elif ret == -2:
            rc = False
        elif ret == -99:
            result['value'] = 'Destination Unreachable'
            result['errno'] = errno.ENETUNREACH
            rc = False
        else:
            result['value'] = ret
            rc = True

        self.results['traceroute'] = result

        return rc

    def test_tcp(self):
        clilog('[Test TCP]', 'yellow')
        ret = None
        result = {
            'value': None,
            'title': 'TCP',
            'errno': None,
            'action': None,
        }
        try:
            tcp_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM, socket.getprotobyname('tcp'))
            tcp_socket.connect((self._dst_addr, int(self._port)))
            tcp_socket.close()
        except KeyboardInterrupt:
            ret = -1
        except Exception as err:
            ret = -2
            result['errno'] = _.get(err, 'errno')
            result['value'] = str(err)

        if ret == -1:
            result['value'] = 'KeyboardInterrupt'
            rc = False
        elif ret == -2:
            rc = False
        else:
            result['value'] = ret
            rc = True

        self.results['tcp'] = result

        return rc

    def test_mysql(self):
        clilog('[Test MYSQL]', 'yellow')
        ret = None
        result = {
            'value': None,
            'title': 'Mysql',
            'errno': None,
            'action': None,
        }
        try:
            import mysql.connector
            from mysql.connector import errorcode

            mysql_config = {
                'user': self._user,
                'password': self._password,
                'host': self._dst_addr,
                'port': self._port,
                'database': self._database,
                'raise_on_warnings': True,
            }
            cnx = mysql.connector.connect(**mysql_config)
            cursor = cnx.cursor()
            ret_msg = []
            query = 'SELECT NOW();'
            ret_msg.append(f'\n  > {query}')
            time_start = time.time()
            cursor.execute(query)
            time_end = time.time()
            duration = _.ceil((time_end - time_start) * 1000, 1)
            for (_now, ) in cursor:
                ret_msg.append(f'    {str(_now)}')
            ret_msg.append(f'  {duration} ms')
            ret = _.join(ret_msg, '\n')
            cursor.close()
        except mysql.connector.Error as err:
            result['errno'] = _.get(err, 'errno')
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                result['value'] = 'Something is wrong with your user name or password'
                result['action'] = 'User/Password를 확인하십시오.'
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                result['value'] = 'Database does not exist'
                result['action'] = 'Database를 확인하십시오.'
            else:
                result['value'] = str(err)
            ret = -2
        except KeyboardInterrupt:
            result['value'] = 'KeyboardInterrupt'
            ret = -1
        except Exception as err:
            ret = -3
            result['errno'] = _.get(err, 'errno')
            result['value'] = str(err)
        else:
            cnx.close()

        if ret in [None, False, -1, -2, -3]:
            rc = False
        else:
            result['value'] = ret
            rc = True

        self.results['mysql'] = result

        return rc

    def test_mongo(self):
        clilog('[Test MONGO]', 'yellow')
        ret = None
        result = {
            'value': None,
            'title': 'Mongo',
            'errno': None,
            'action': None,
        }
        try:
            from pymongo import MongoClient
            from pymongo.errors import ConnectionFailure

            from urllib.parse import quote_plus

            uri = f"mongodb://{quote_plus(self._user)}:{quote_plus(self._password)}@{self._dst_addr}:{self._port}/{self._database}"
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            time_start = time.time()
            ret = f"version={_.get(client.server_info(), 'version')}"
            time_end = time.time()
            duration = _.ceil((time_end - time_start) * 1000, 1)
            ret += f', {duration} ms'
        except ConnectionFailure as err:
            ret = -2
            result['errno'] = _.get(err, 'errno')
            err_msg = str(err)
            result['value'] = err_msg
        except KeyboardInterrupt:
            result['value'] = 'KeyboardInterrupt'
            ret = -1
        except Exception as err:
            ret = -3
            result['errno'] = _.get(err, 'errno')
            err_msg = str(err)
            result['value'] = err_msg
            if 'Authentication failed' in err_msg:
                result['action'] = 'User/Password/Database를 확인하십시오.'
        else:
            client.close()

        if ret in [None, False, -1, -2, -3]:
            rc = False
        else:
            result['value'] = ret
            rc = True

        self.results['mongo'] = result

        return rc

    def test(self):
        ret = None
        protocol_ret = None

        if self._protocol == 'MYSQL':
            protocol_ret = self.test_mysql()
        elif self._protocol == 'MONGO':
            protocol_ret = self.test_mongo()

        if protocol_ret:
            clilog('OK', 'green')
            return protocol_ret
        else:
            ret = protocol_ret
            if self._protocol != 'TCP':
                clilog('FAIL', 'red')

        if self._protocol == 'TCP' or ret == False:
            tcp_ret = self.test_tcp()
            if tcp_ret:
                clilog('OK', 'green')
                if self._protocol == 'TCP':
                    return tcp_ret
                return ret
            else:
                clilog('FAIL', 'red')

        icmp_ret = self.test_ping()
        if icmp_ret:
            clilog('OK', 'green')
        else:
            clilog('FAIL', 'red')

        icmp_ret = self.test_traceroute()
        if icmp_ret:
            clilog('OK', 'green')
        else:
            clilog('FAIL', 'red')

        if self._protocol == 'ICMP':
            ret = icmp_ret

        return ret


def ask_conn(args={}):
    full_questions = [
        {
            'type': 'input',
            'name': 'dest',
            'message': '목적지의 IP나 Domain을 입력하세요. :',
            'validate': DestValidator,
        }, {
            'type': 'list',
            'name': 'protocol',
            'message': '목적지에 연결할 프로토콜을 입력하세요. :',
            'choices': protocol_meta.keys(),
        },
    ]

    questions = []
    for question in full_questions:
        if _.get(args, question['name']):
            continue
        questions.append(question)
    answers = prompt(questions, args, style=style)
    if _.is_empty(answers):
        return answers

    protocol = _.get(answers, 'protocol')
    if protocol == 'ICMP':
        return answers

    # TCP
    default_port = _.get(protocol_meta, f'{protocol}.port', 0)
    answers = prompt({
        'type': 'input',
        'name': 'port',
        'message': f"목적지의 PORT를 입력하세요. [default={default_port}] :",
        'validate': PortValidator,
    }, answers, style=style)

    if _.is_empty(answers):
        return answers

    if not _.get(answers, 'port'):
        answers['port'] = default_port

    if protocol in ['MYSQL', 'MONGO']:
        default_user = _.get(protocol_meta, f'{protocol}.user', 'root')
        default_password = _.get(
            protocol_meta, f'{protocol}.password', 'password')
        default_database = _.get(protocol_meta, f'{protocol}.database', 'mydb')
        answers = prompt([{
            'type': 'input',
            'name': 'user',
            'message': f"User [default={default_user}] :",
        }, {
            'type': 'input',
            'name': 'password',
            'is_password': True,
            'message': f"Password [default={default_password}] :",
        }, {
            'type': 'input',
            'name': 'database',
            'message': f"Database [default={default_database}] :",
        }], answers, style=style)
        if not _.get(answers, 'user'):
            answers['user'] = default_user
        if not _.get(answers, 'password'):
            answers['password'] = default_password
        if not _.get(answers, 'database'):
            answers['database'] = default_database

    return answers


def conn_main():
    clilog('[Connection Test Mode]', 'green')

    ap = argparse.ArgumentParser(description='ec5 cli - conn')
    ap.add_argument('--dest', type=str, dest='dest', default='',
                    help='IP address or DNS name of destination to connect to.')
    ap.add_argument('--protocol', type=str, dest='protocol', default='',
                    help='MYSQL, TCP, ICMP')
    ap.add_argument('--timeout', type=int, dest='timeout', default=1,
                    help='Time in seconds to wait for ping.', metavar='seconds')
    ap.add_argument('--verbose', '-v', dest='verbose',
                    default=False, action='store_true', help='Verbose-mode')
    args, _unknown = ap.parse_known_args()

    try:
        answers = ask_conn(vars(args))
        if not answers:
            return 1
        clilog(' ')

        logger.debug(f"ans={answers}")
        conn = Conn(answers)
        ret = conn.test()
        clilog('[Result]', 'yellow')
        if ret:
            clilog('OK', 'green')
        else:
            clilog('FAIL', 'red')
        conn.report()
    except Exception as err:
        clilog(str(err), 'red')
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(conn_main())
