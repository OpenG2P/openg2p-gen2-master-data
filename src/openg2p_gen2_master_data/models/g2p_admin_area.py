import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_fastapi_common.models import BaseORMModel


class G2PAdministrativeAreaLarge(BaseORMModel):
    __tablename__ = "g2p_administrative_area_large"

    area_id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    area_mnemonic: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    area_description: Mapped[str] = mapped_column(String, nullable=False)


class G2PAdministrativeAreaSmall(BaseORMModel):
    __tablename__ = "g2p_administrative_area_small"

    area_id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    area_mnemonic: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    area_description: Mapped[str] = mapped_column(String, nullable=False)
    administrative_area_large_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("g2p_administrative_area_large.area_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
