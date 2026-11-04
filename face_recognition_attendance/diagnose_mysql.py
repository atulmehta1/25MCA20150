import socket
import sys

def check_port(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except Exception:
        return False

def test_mysql():
    print("=" * 60)
    print("MySQL Connection Diagnostic Tool")
    print("=" * 60)

    # 1. Check ports
    ports_to_check = [3306, 3307]
    open_ports = [p for p in ports_to_check if check_port('localhost', p)]
    
    if not open_ports:
        print("[!] ERROR: No MySQL service is listening on port 3306 or 3307.")
        print("    Please check that your MySQL Server is running in Windows Services:")
        print("    Press Win+R -> type 'services.msc' -> find 'MySQL80' -> click Start.")
        return

    print(f"[+] MySQL port is ACTIVE on port(s): {open_ports}")
    active_port = open_ports[0]

    # 2. Try pymysql
    try:
        import pymysql
    except ImportError:
        print("[!] PyMySQL is not installed. Run: pip install pymysql")
        return

    # Passwords to test
    passwords = [
        'atulmehta12345',
        'root',
        '',
        'admin',
        '1234',
        '123456',
        '12345678',
        'password',
        'mysql'
    ]

    working_password = None

    print(f"\n[*] Testing connection to MySQL (user: root, port: {active_port})...")
    for pwd in passwords:
        pwd_display = repr(pwd) if pwd else "'' (no password)"
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password=pwd,
                port=active_port,
                connect_timeout=2
            )
            conn.close()
            print(f"[SUCCESS] Connected to MySQL with password: {pwd_display}!")
            working_password = pwd
            break
        except pymysql.err.OperationalError as e:
            err_code = e.args[0] if e.args else None
            if err_code == 1045:
                print(f"[-] Password {pwd_display}: Access Denied (incorrect password)")
            else:
                print(f"[-] Error with {pwd_display}: {e}")
        except Exception as e:
            print(f"[-] Unexpected error with {pwd_display}: {e}")

    if working_password is not None:
        print("\n" + "=" * 60)
        print(f"[+] SUCCESS! Working password found: '{working_password}'")
        print("[*] Updating .env file automatically...")
        
        # Update .env
        env_path = 'c:/Users/atulm/Downloads/project/New folder (2)/face_recognition_attendance/.env'
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if line.startswith('DB_TYPE='):
                    new_lines.append('DB_TYPE=mysql')
                elif line.startswith('DB_PASSWORD='):
                    new_lines.append(f'DB_PASSWORD={working_password}')
                elif line.startswith('DB_PORT='):
                    new_lines.append(f'DB_PORT={active_port}')
                else:
                    new_lines.append(line)
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines) + '\n')
            print("[+] .env successfully updated with the working MySQL password!")
            print("[*] You can now start the application: npm start")
        except Exception as err:
            print(f"[!] Could not update .env automatically: {err}")
    else:
        print("\n" + "=" * 60)
        print("[!] None of the common passwords matched for user 'root'.")
        print("    To find or reset your MySQL root password:")
        print("    1. Open MySQL Workbench.")
        print("    2. On the welcome screen, look at 'Local instance MySQL80'.")
        print("    3. Click the Wrench icon -> 'Test Connection'.")
        print("    4. Type the password that succeeds into .env (DB_PASSWORD=...).")
        print("=" * 60)

if __name__ == '__main__':
    test_mysql()
