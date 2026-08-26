import httpx

BASE = "http://127.0.0.1:8000"
c = httpx.Client(timeout=10)

# --- 登录 ---
print("=== 登录个人用户 ===")
r = c.post(f"{BASE}/api/auth/login", json={
    "account": "202320211001",
    "password": "test123456",
    "user_type": "personal",
})
if r.status_code != 200:
    print("  个人用户不存在，注册中...")
    c.post(f"{BASE}/api/auth/register/personal", json={
        "student_id": "202320211001",
        "full_name": "测试用户",
        "password": "test123456",
        "university": "山东大学",
        "contact": "13812345678",
        "major": "计算机科学与技术",
    })
    r = c.post(f"{BASE}/api/auth/login", json={
        "account": "202320211001",
        "password": "test123456",
        "user_type": "personal",
    })
personal_token = r.json()["access_token"]
personal_auth = {"Authorization": f"Bearer {personal_token}"}
print(f"  OK: {r.json()['name']}")

print("\n=== 登录政企用户 ===")
r = c.post(f"{BASE}/api/auth/login", json={
    "account": "test@company.com",
    "password": "test123456",
    "user_type": "enterprise",
})
if r.status_code != 200:
    print("  政企用户不存在，注册中...")
    c.post(f"{BASE}/api/auth/register/enterprise", json={
        "org_name": "测试企业",
        "org_type": "企业单位",
        "admin_location": "山东省济南市历下区文化路179号",
        "admin_code": "370102",
        "org_email": "test@company.com",
        "contact_person": "测试负责人",
        "contact_phone": "13987654321",
        "password": "test123456",
        "org_profile": "本企业致力于推动产学研融合与边疆地区社会实践发展，专注于乡村振兴、教育帮扶、医疗健康等核心领域。",
    })
    r = c.post(f"{BASE}/api/auth/login", json={
        "account": "test@company.com",
        "password": "test123456",
        "user_type": "enterprise",
    })
enterprise_token = r.json()["access_token"]
enterprise_auth = {"Authorization": f"Bearer {enterprise_token}"}
print(f"  OK: {r.json()['name']}")

# --- 团队 API ---
print("\n=== 1. 创建团队 ===")
r = c.post(f"{BASE}/api/teams/", headers=personal_auth, json={
    "team_name": "鸿雁社会实践队",
    "leader_name": "测试用户",
    "leader_contact": "13812345678",
    "leader_email": "test@sdu.edu.cn",
    "student_id": "202320211001",
    "university": "山东大学",
    "team_specialty": "乡村振兴",
    "team_description": "致力于乡村振兴社会实践，服务边疆地区发展。",
    "teacher_name": "张老师",
    "teacher_contact": "13900000001",
})
print(f"  Status: {r.status_code}")
print(f"  Team: id={r.json().get('id')}, name={r.json().get('team_name')}, specialty={r.json().get('team_specialty')}")
team_id = r.json().get("id")

print("\n=== 2. 团队列表 ===")
r = c.get(f"{BASE}/api/teams/")
print(f"  Status: {r.status_code}, Total: {r.json().get('total')}, Items: {len(r.json().get('items', []))}")

print("\n=== 3. 按分类筛选团队 ===")
r = c.get(f"{BASE}/api/teams/?category=乡村振兴")
print(f"  Status: {r.status_code}, Total: {r.json().get('total')} (filtered by 乡村振兴)")

print("\n=== 4. 团队详情 ===")
r = c.get(f"{BASE}/api/teams/{team_id}")
print(f"  Status: {r.status_code}")
print(f"  Name: {r.json().get('team_name')}, Members: {len(r.json().get('members', []))}")

# --- 需求 API ---
print("\n=== 5. 创建需求 ===")
r = c.post(f"{BASE}/api/demands/", headers=enterprise_auth, json={
    "internship_location": "新疆喀什地区",
    "estimated_time": "2024年7月-8月",
    "requirements_content": "需要计算机科学、教育学专业的学生参与乡村振兴社会实践活动。",
    "target_majors": ["乡村振兴", "科技赋能", "教育帮扶"],
    "org_type": "企业单位",
    "org_name": "测试企业",
    "contact_info": "test@company.com",
})
print(f"  Status: {r.status_code}")
print(f"  Demand: id={r.json().get('id')}, company={r.json().get('company_name')}")
demand_id = r.json().get("id")

print("\n=== 6. 需求列表 ===")
r = c.get(f"{BASE}/api/demands/")
print(f"  Status: {r.status_code}, Total: {r.json().get('total')}")

print("\n=== 7. 按分类筛选需求 ===")
r = c.get(f"{BASE}/api/demands/?category=乡村振兴")
print(f"  Status: {r.status_code}, Total: {r.json().get('total')} (filtered by 乡村振兴)")
r = c.get(f"{BASE}/api/demands/?category=医疗健康")
print(f"  Status: {r.status_code}, Total: {r.json().get('total')} (filtered by 医疗健康, expect 0)")

print("\n=== 8. 需求详情 ===")
r = c.get(f"{BASE}/api/demands/{demand_id}")
print(f"  Status: {r.status_code}")
print(f"  Location: {r.json().get('internship_location')}, Majors: {r.json().get('target_majors')}")

# --- 论坛 API ---
print("\n=== 9. 发帖 ===")
r = c.post(f"{BASE}/api/forum/posts", headers=personal_auth, json={
    "title": "暑期社会实践经验分享",
    "content": "今年暑假我们团队前往新疆喀什地区开展社会实践，收获颇丰。",
    "category": "最新",
    "team": "鸿雁社会实践队",
    "location": "新疆喀什",
})
print(f"  Status: {r.status_code}")
print(f"  Post: id={r.json().get('id')}, title={r.json().get('title')}")
post_id = r.json().get("id")

print("\n=== 10. 帖子列表 ===")
r = c.get(f"{BASE}/api/forum/posts")
print(f"  Status: {r.status_code}, Total: {r.json().get('total')}")

print("\n=== 11. 帖子详情（views+1）===")
r = c.get(f"{BASE}/api/forum/posts/{post_id}")
print(f"  Status: {r.status_code}")
print(f"  Views: {r.json().get('views')} (expected 1)")
print(f"  Comments: {len(r.json().get('comments', []))}")

print("\n=== 12. 评论 ===")
r = c.post(f"{BASE}/api/forum/posts/{post_id}/comments", headers=personal_auth, json={
    "content": "非常棒的经验分享！",
})
print(f"  Status: {r.status_code}")
print(f"  Comment: id={r.json().get('id')}, author={r.json().get('author_name')}")

print("\n=== 13. 再次查看帖子（验证评论已添加）===")
r = c.get(f"{BASE}/api/forum/posts/{post_id}")
print(f"  Views: {r.json().get('views')} (expected 2)")
print(f"  Comments: {len(r.json().get('comments', []))} (expected 1)")
comment = r.json()["comments"][0] if r.json().get("comments") else {}
print(f"  Comment content: {comment.get('content')}")

# --- 权限测试 ---
print("\n=== 14. 个人用户创建需求（应被拒绝）===")
r = c.post(f"{BASE}/api/demands/", headers=personal_auth, json={
    "internship_location": "test",
    "estimated_time": "test",
    "requirements_content": "test content here",
    "target_majors": [],
    "org_type": "test",
    "org_name": "test",
    "contact_info": "test",
})
print(f"  Status: {r.status_code} (expected 403)")

print("\n=== 15. 政企用户发帖（允许）===")
r = c.post(f"{BASE}/api/forum/posts", headers=enterprise_auth, json={
    "title": "企业视角的产学研合作",
    "content": "从企业角度看产学研合作的重要性和实践路径。",
    "category": "热门",
})
print(f"  Status: {r.status_code} (expected 201)")

c.close()
print("\n=== All business API tests completed! ===")
