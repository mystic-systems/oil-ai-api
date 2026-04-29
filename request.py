import subprocess
import sys

required_packages = {
    "flask": "flask",
    "requests": "requests",
    "pandas": "pandas",
    "yfinance": "yfinance",
    "flask-cors": "flask_cors"
}

def check_and_install(import_name):
    try:
        __import__(import_name)
        print(f"[OK] {import_name} este deja instalat.")
        return True
    except ImportError:
        print(f"[MISSING] {import_name} nu este instalat.")
        return False

def install_package(package):
    print(f"Se instalează {package} ...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    missing = []

    for pip_name, import_name in required_packages.items():
        if not check_and_install(import_name):
            missing.append(pip_name)

    if not missing:
        print("\nToate pachetele sunt deja instalate.")
        return

    print("\nPachete lipsă:", ", ".join(missing))
    answer = input("Vrei să le instalezi? (yes/no): ").strip().lower()

    if answer == "yes":
        for pkg in missing:
            install_package(pkg)
        print("\nGata! Toate pachetele au fost instalate.")
    else:
        print("Instalarea a fost anulată.")

if __name__ == "__main__":
    main()

input("Apasa Enter pentru iesire")