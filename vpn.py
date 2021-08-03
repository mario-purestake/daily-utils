#!/usr/bin/python3

import os, re, argparse, sys


def check_arg(args=None):
  parser = argparse.ArgumentParser(description='Script to open and manage OpenVPN sessions')
  parser.add_argument('-c',  '--config', required = False, help='Config file to use to open a new VPN session', default="Madrid")
  parser.add_argument('-k',  '--kill', required = False, help='Terminate all current VPN sessions', action="store_true")
  
  results = parser.parse_args(args)
  return (results.config,results.kill)

def main():
  streamed_out = os.popen("openvpn3 sessions-list")
  output = streamed_out.read()

  if arg_kill or "No sessions available" not in output:
    sessions_str = output.replace('\n', ' NEW_L').split(" NEW_L NEW_L")
    sessions = []
    print(f"There are {len(sessions_str)} open sessions." if len(sessions_str) > 1 else 
          f"There is {len(sessions_str)} open session.")

    for index, session_str in enumerate(sessions_str):
      session = {}

      session['path'] = re.search("Path: (\S+) ", session_str).group(1).strip()
      session['config'] = re.search("Config name: (\S+) ", session_str).group(1).strip()
      session['conn_status'] = re.search("Status: (.*).*$", session_str).group(1).split('NEW_L')[0].strip()

      print(f"  Session {index + 1}: ")
      print(f"   - Path: {session['path']}")
      print(f"   - Config: {session['config']}")
      print(f"   - Status: {session['conn_status']}")

      sessions.append(session)

    terminate = input("\nDo you want to terminate those sessions to open a new one? [y/N]: " if len(sessions_str) > 1 else 
                      "\nDo you want to terminate this session to open a new one? [y/N]: ")

    if "y" not in terminate.lower():
      return

    print("")
    
    for index, session in enumerate(sessions):
      print(f"Terminating session {index+1} using {session['config']}...")
      os.system(f"openvpn3 session-manage --path {session['path']} --disconnect")
      print("")


  if not arg_kill:
    create = input(f"Do you want to create a new session using {arg_config}? [Y/n]: ")

    if "n" in create.lower():
      return

    print(f"Openning new session using {arg_config}...\n")
    os.system(f"openvpn3 session-start --config {arg_config}")

if __name__ == '__main__':
  arg_config,arg_kill = check_arg(sys.argv[1:])
  arg_config = f"PS-{arg_config}"
  main()
