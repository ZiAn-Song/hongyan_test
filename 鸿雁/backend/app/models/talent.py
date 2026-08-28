from datetime import datetime

from sqlalchemy import String, Integer, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SduTalent(Base):
    """山大科研与人才资源（供给侧·高校科研，跨类型统一排序的一部分）"""
    __tablename__ = "sdu_talents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domain: Mapped[str] = mapped_column(String(50), index=True)          # 农业/能源/智能制造/AI
    org: Mapped[str | None] = mapped_column(String(200), nullable=True)  # 所属学院
    field: Mapped[str | None] = mapped_column(String(500), nullable=True)  # 研究领域/方向
    team: Mapped[str] = mapped_column(String(300), index=True)           # 团队/实验室名称
    leader: Mapped[str | None] = mapped_column(String(200), nullable=True)   # 负责人/核心教师
    leader_title: Mapped[str | None] = mapped_column(Text, nullable=True)    # 人才头衔
    patents: Mapped[str | None] = mapped_column(Text, nullable=True)         # 代表性专利
    core_tech: Mapped[str | None] = mapped_column(Text, nullable=True)       # 核心技术成果/产品
    awards: Mapped[str | None] = mapped_column(Text, nullable=True)          # 获奖/项目级别
    west_scene: Mapped[str | None] = mapped_column(String(500), nullable=True)  # 可服务的西部场景（匹配桥梁）
    application: Mapped[str | None] = mapped_column(String(500), nullable=True)  # 具体应用方向（匹配桥梁）
    maturity: Mapped[str | None] = mapped_column(String(100), nullable=True)     # 技术成熟度
    cases: Mapped[str | None] = mapped_column(Text, nullable=True)               # 已转化/合作案例
    source_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    source_note: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
