from pydantic import BaseModel, Field


class PersonalRegisterRequest(BaseModel):
    student_id: str = Field(..., min_length=5, max_length=20, description="学号")
    full_name: str = Field(..., min_length=2, max_length=50, description="姓名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    gender: str | None = Field(None, max_length=10, description="性别")
    university: str = Field(..., min_length=1, max_length=100, description="高校")
    contact: str = Field(..., pattern=r"^1[3-9]\d{9}$", description="手机号")
    email: str | None = Field(None, max_length=100, description="邮箱")
    major: str | None = Field(None, max_length=100, description="专业")


class EnterpriseRegisterRequest(BaseModel):
    org_name: str = Field(..., min_length=2, max_length=200, description="机构名称")
    org_type: str = Field(..., max_length=50, description="机构类型")
    admin_location: str = Field(..., min_length=5, max_length=300, description="行政地点")
    admin_code: str = Field(..., pattern=r"^\d{6}$", description="行政编码")
    org_email: str = Field(..., max_length=100, description="邮箱")
    contact_person: str = Field(..., max_length=50, description="负责人姓名")
    contact_phone: str = Field(..., pattern=r"^1[3-9]\d{9}$", description="联系电话")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    org_profile: str = Field(..., min_length=50, description="机构简介")
    additional_info: str | None = Field(None, description="补充信息")


class LoginRequest(BaseModel):
    account: str = Field(..., description="学号或邮箱")
    password: str = Field(..., description="密码")
    user_type: str = Field(..., pattern=r"^(personal|enterprise)$", description="用户类型")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_type: str
    user_id: int
    name: str
    role: str


class UserResponse(BaseModel):
    id: int
    student_id: str
    full_name: str
    role: str
    gender: str | None
    university: str | None
    contact: str | None
    email: str | None
    major: str | None

    model_config = {"from_attributes": True}


class CompanyResponse(BaseModel):
    id: int
    org_name: str
    org_type: str
    admin_location: str | None
    admin_code: str | None
    org_email: str | None
    contact_person: str | None
    contact_phone: str | None
    org_profile: str | None

    model_config = {"from_attributes": True}
