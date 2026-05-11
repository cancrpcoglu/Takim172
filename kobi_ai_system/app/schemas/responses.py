from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ChatResponse(BaseModel):
    """Frontend'e döneceğimiz standart AI yanıt şeması."""
    
    # Kullanıcıya gösterilecek doğal dil metni
    message: str = Field(..., description="Kullanıcıya gösterilecek doğal dildeki yanıt.")
    
    # Frontend'in arayüzü değiştirmesi için (Örn: ürünleri kart olarak göstermek için)
    ui_type: str = Field(
        default="text", 
        description="Arayüz tipi: 'text', 'product_carousel', 'cargo_timeline' vb."
    )
    
    # Eğer ui_type 'text' değilse, Frontend'in kullanacağı ham JSON verisi
    ui_data: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Frontend bileşenlerini besleyecek ek veriler (Örn: Ürün listesi)"
    )