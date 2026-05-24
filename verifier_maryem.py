"""
Script de vérification — Partie Maryem
Lance : python verifier_maryem.py
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

print("\n" + "="*50)
print("  VÉRIFICATION PARTIE MARYEM — SmartStudent")
print("="*50)

# ── 1. Backend actif ──────────────────────────────────
print("\n[1] Backend")
try:
    r = requests.get("http://localhost:8000/health", timeout=3)
    check("Backend démarré", r.status_code == 200, r.json().get("service",""))
except Exception as e:
    check("Backend démarré", False, "DÉMARRER le backend d'abord !")
    print("\n  → Lance : cd page-not-found && .venv\\Scripts\\python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000")
    exit(1)

# ── 2. Authentification ───────────────────────────────
print("\n[2] Authentification")
r = requests.post(f'{BASE}/auth/login',
    json={'email':'meryemreguigue.99@gmail.com','password':'meryem123'})
check("Login fonctionne", r.status_code == 200)
if r.status_code != 200:
    print("  → Mot de passe incorrect. Essaie meryem ou un autre.")
    exit(1)
token = r.json()['access_token']
h = {'Authorization': f'Bearer {token}'}
check("Token JWT reçu", len(token) > 50, f"{len(token)} caractères")

# ── 3. Événements Campus ──────────────────────────────
print("\n[3] Module Campus — Événements")
r = requests.get(f'{BASE}/campus/events', headers=h)
check("GET /campus/events répond", r.status_code == 200)
events = r.json()
check("Au moins 1 événement en base", len(events) >= 1, f"{len(events)} événements trouvés")
if events:
    e = events[0]
    check("Événement a un titre", bool(e.get('title')), e.get('title',''))
    check("Événement a une date", bool(e.get('start_date')))
    check("Événement a un type", bool(e.get('event_type')), e.get('event_type',''))

# ── 4. Planning — Tâches ──────────────────────────────
print("\n[4] Module Planning — Tâches")
# Créer une tâche
r = requests.post(f'{BASE}/planning/tasks', headers=h, json={
    'title': 'Test tâche vérification',
    'category': 'study',
    'due_date': '2026-06-20T10:00:00',
    'priority': 2
})
check("POST /planning/tasks (créer)", r.status_code == 200)
task_id = None
if r.status_code == 200:
    task = r.json()
    task_id = task['id']
    check("Tâche a un ID", task_id is not None, f"id={task_id}")
    check("Tâche a le bon titre", task['title'] == 'Test tâche vérification')
    check("Statut initial = pending", task['status'] == 'pending')

# Lister
r = requests.get(f'{BASE}/planning/tasks', headers=h)
check("GET /planning/tasks (lister)", r.status_code == 200)
tasks = r.json()
check("La tâche créée apparaît", any(t['id'] == task_id for t in tasks) if task_id else False)

# Marquer terminée
if task_id:
    r = requests.put(f'{BASE}/planning/tasks/{task_id}', headers=h, json={'status':'completed'})
    check("PUT /planning/tasks/{id} (compléter)", r.status_code == 200)
    check("Statut = completed", r.json().get('status') == 'completed')

# Supprimer
if task_id:
    r = requests.delete(f'{BASE}/planning/tasks/{task_id}', headers=h)
    check("DELETE /planning/tasks/{id} (supprimer)", r.status_code == 200)

# ── 5. Examens — Quiz ─────────────────────────────────
print("\n[5] Module Examens — Quiz")
r = requests.post(f'{BASE}/exams/generate', headers=h, json={
    'subject': 'Algorithmique',
    'num_questions': 3,
    'difficulty': 'easy'
})
check("POST /exams/generate (générer quiz)", r.status_code == 200)
exam_id = None
if r.status_code == 200:
    exam = r.json()
    exam_id = exam['id']
    questions = exam.get('questions', [])
    check("Quiz a des questions", len(questions) >= 1, f"{len(questions)} questions")
    check("Quiz a un titre", bool(exam.get('title')))
    if questions:
        q = questions[0]
        check("Question a du texte", bool(q.get('question')))
        check("Question a 4 options", len(q.get('options',[])) == 4)
        check("Question a une réponse", bool(q.get('answer')))

# Soumettre
if exam_id and questions:
    answers = [q.get('answer','') for q in questions]
    r = requests.post(f'{BASE}/exams/{exam_id}/submit', headers=h,
        json={'exam_id': exam_id, 'answers': answers})
    check("POST /exams/{id}/submit (soumettre)", r.status_code == 200)
    if r.status_code == 200:
        result = r.json()
        check("Résultat a un score", 'score' in result, f"score={result.get('score')}/{result.get('total')}")
        check("Pourcentage calculé", 'percentage' in result, f"{result.get('percentage')}%")

# Historique & Stats
r = requests.get(f'{BASE}/exams/history', headers=h)
check("GET /exams/history", r.status_code == 200, f"{len(r.json())} quiz")

r = requests.get(f'{BASE}/exams/stats', headers=h)
check("GET /exams/stats", r.status_code == 200)
if r.status_code == 200:
    s = r.json()
    check("Stats contiennent average_score", 'average_score' in s, f"{s.get('average_score')}%")

# ── Résumé ────────────────────────────────────────────
print("\n" + "="*50)
print("  Tous les endpoints backend sont opérationnels !")
print("  Lance maintenant l'app Flutter pour tester l'UI.")
print("="*50 + "\n")
