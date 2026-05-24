"""
Script de vérification du système RAG ENIAD
Lance : python verifier_rag.py
"""
import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'http://localhost:8000/api'
OK   = "[OK]  "
FAIL = "[ERR] "

def check(label, condition, detail=""):
    status = OK if condition else FAIL
    print(f"  {status} {label}" + (f" -> {detail}" if detail else ""))
    return condition

print("\n" + "="*55)
print("  VERIFICATION RAG ENIAD — SmartStudent")
print("="*55)

# 1. Backend
print("\n[1] Backend actif")
try:
    r = requests.get("http://localhost:8000/health", timeout=3)
    check("Backend OK", r.status_code == 200, r.json().get("service",""))
except:
    check("Backend OK", False, "DEMARRER le backend d'abord")
    sys.exit(1)

# 2. Login
print("\n[2] Auth")
r = requests.post(f'{BASE}/auth/login',
    json={'email':'meryemreguigue.99@gmail.com','password':'meryem123'})
check("Login", r.status_code == 200)
if r.status_code != 200:
    sys.exit(1)
token = r.json()['access_token']
h = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

# 3. Statut RAG
print("\n[3] Statut RAG")
r = requests.get(f'{BASE}/admin/rag/status')
check("Endpoint /admin/rag/status", r.status_code == 200)
if r.status_code == 200:
    data = r.json()
    check("RAG pret", data.get('ready', False), data.get('message',''))
    check("Documents indexes", data.get('document_count', 0) > 0,
          f"{data.get('document_count',0)} documents")

# 4. Recherche RAG
print("\n[4] Recherche documentaire")
r = requests.post(f'{BASE}/admin/rag/search', headers=h,
    json={'query': 'emploi du temps IA semestre 5', 'n_results': 3})
check("POST /admin/rag/search", r.status_code == 200)
if r.status_code == 200:
    results = r.json().get('results', [])
    check("Resultats trouves", len(results) > 0, f"{len(results)} resultats")
    if results:
        best = results[0]
        check("Score de pertinence", best.get('score', 0) > 0.3,
              f"score={best.get('score','?')}")
        check("Contenu present", len(best.get('content','')) > 20)

# 5. Requete convention de stage
print("\n[5] Recherche convention de stage")
r = requests.post(f'{BASE}/admin/rag/search', headers=h,
    json={'query': 'convention de stage telecharger PDF', 'n_results': 2})
if r.status_code == 200:
    results = r.json().get('results', [])
    has_link = any('stage' in r.get('content','').lower() or
                   'convention' in r.get('content','').lower()
                   for r in results)
    check("Trouve convention stage", has_link)

# 6. Question Agent Admin
print("\n[6] Agent Admin avec RAG")
r = requests.post(f'{BASE}/admin/ask', headers=h,
    json={'question': "Ou puis-je telecharger l emploi du temps de la filiere IA semestre 5 ?"})
check("POST /admin/ask", r.status_code == 200)
if r.status_code == 200:
    data = r.json()
    check("Reponse non vide", len(data.get('answer','')) > 50,
          f"{len(data.get('answer',''))} chars")
    check("RAG utilise", data.get('rag_used', False),
          f"{data.get('rag_document_count',0)} docs indexes")
    print(f"\n  Reponse : {data.get('answer','')[:200]}...")

# 7. Question filiere
print("\n[7] Question filiere IA")
r = requests.post(f'{BASE}/admin/ask', headers=h,
    json={'question': "Quelles sont les filieres disponibles a l ENIAD ?"})
check("POST /admin/ask filiere", r.status_code == 200)
if r.status_code == 200:
    answer = r.json().get('answer','')
    has_ia = 'ia' in answer.lower() or 'intelligence artificielle' in answer.lower()
    check("Mentionne filiere IA", has_ia, answer[:100])

print("\n" + "="*55)
print("  RAG ENIAD verifie !")
print("  Si RAG not ready : lance d abord :")
print("  python -m backend.scripts.setup_rag")
print("="*55 + "\n")
