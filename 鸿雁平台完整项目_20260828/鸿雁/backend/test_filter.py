import httpx

c = httpx.Client(timeout=10)
BASE = "http://127.0.0.1:8000"

# Login
r = c.post(f"{BASE}/api/auth/login", json={
    "account": "test@company.com",
    "password": "test123456",
    "user_type": "enterprise",
})

print("=== All demands ===")
r = c.get(f"{BASE}/api/demands/")
data = r.json()
print(f"  Total: {data['total']}")

print("\n=== Filter by 乡村振兴 ===")
r = c.get(f"{BASE}/api/demands/?category=乡村振兴")
data = r.json()
print(f"  Total: {data['total']} (expected > 0)")
if data["items"]:
    d = data["items"][0]
    print(f"  First: company={d['company_name']}, majors={d['target_majors']}")

print("\n=== Filter by 科技赋能 ===")
r = c.get(f"{BASE}/api/demands/?category=科技赋能")
print(f"  Total: {r.json()['total']} (expected > 0)")

print("\n=== Filter by 医疗健康 (expect 0) ===")
r = c.get(f"{BASE}/api/demands/?category=医疗健康")
print(f"  Total: {r.json()['total']} (expected 0)")

c.close()
print("\nDone!")
