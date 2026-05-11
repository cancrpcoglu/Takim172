from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Frontend'den gelecek olan istek modeli."""
    message: str = Field(..., description="Kullanıcının gönderdiği mesaj")
    session_id: str = Field(default="test_session", description="Kullanıcıyı tanımak için oturum ID'si")