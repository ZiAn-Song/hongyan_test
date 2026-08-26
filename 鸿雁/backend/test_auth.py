import httpx

BASE = "http://127.0.0.1:8000"
c = httpx.Client(timeout=10)

print("=== 1. 个人注册 ===")
r = c.post(f"{BASE}/api/auth/register/personal", json={
    "student_id": "202320211001",
    "full_name": "测试用户",
    "password": "test123456",
    "gender": "男",
    "university": "山东大学",
    "contact": "13812345678",
    "email": "test@sdu.edu.cn",
    "major": "计算机科学与技术",
})
print(f"  Status: {r.status_code}")
data = r.json()
print(f"  id={data.get('id')}, name={data.get('full_name')}, univ={data.get('university')}")

print("\n=== 2. 政企注册 ===")
r = c.post(f"{BASE}/api/auth/register/enterprise", json={
    "org_name": "测试企业",
    "org_type": "企业单位",
    "admin_location": "山东省济南市历下区文化路179号",
    "admin_code": "370102",
    "org_email": "test@company.com",
    "contact_person": "测试负责人",
    "contact_phone": "13987654321",
    "password": "test123456",
    "org_profile": "本企业致力于推动产学研融合与边疆地区社会实践发展，专注于乡村振兴、教育帮扶、医疗健康等核心领域，已与多所高校建立合作关系。",
    "additional_info": "无",
})
print(f"  Status: {r.status_code}")
data = r.json()
print(f"  id={data.get('id')}, org={data.get('org_name')}, type={data.get('org_type')}")

print("\n=== 3. 个人登录 ===")
r = c.post(f"{BASE}/api/auth/login", json={
    "account": "202320211001",
    "password": "test123456",
    "user_type": "personal",
})
print(f"  Status: {r.status_code}")
token = r.json().get("access_token")
print(f"  token={token[:30]}...")
print(f"  user_type={r.json().get('user_type')}, name={r.json().get('name')}")

print("\n=== 4. Token 验证 /me ===")
r = c.get(f"{BASE}/api/auth/me", headers={"Authorization": f"Bearer {token}"})
print(f"  Status: {r.status_code}")
data = r.json()
print(f"  id={data.get('id')}, type={data.get('user_type')}, name={data.get('name')}")

print("\n=== 5. 错误密码 ===")
r = c.post(f"{BASE}/api/auth/login", json={
    "account": "202320211001",
    "password": "wrongpassword",
    "user_type": "personal",
})
print(f"  Status: {r.status_code} (expected 401)")
print(f"  Detail: {r.json().get('detail')}")

print("\n=== 6. 重复学号注册 ===")
r = c.post(f"{BASE}/api/auth/register/personal", json={
    "student_id": "202320211001",
    "full_name": "重复用户",
    "password": "test123456",
    "university": "另一所大学",
    "contact": "13800000000",
})
print(f"  Status: {r.status_code} (expected 400)")
print(f"  Detail: {r.json().get('detail')}")

print("\n=== 7. 无 Token 访问 /me ===")
r = c.get(f"{BASE}/api/auth/me")
print(f"  Status: {r.status_code} (expected 401)")
print(f"  Detail: {r.json().get('detail')}")

print("\n=== 8. 政企登录 ===")
r = c.post(f"{BASE}/api/auth/login", json={
    "account": "test@company.com",
    "password": "test123456",
    "user_type": "enterprise",
})
print(f"  Status: {r.status_code}")
data = r.json()
print(f"  user_type={data.get('user_type')}, name={data.get('name')}")

c.close()
print("\n=== All tests passed! ===")
