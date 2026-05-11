import React, { useState, useRef, useEffect } from 'react';
import aiAvatar from './avatar.png';

type AuthMode = 'login' | 'register';
interface Product { id: number; name: string; price: number; emoji: string; category: string; }
interface CartItem extends Product { quantity: number; }

const PRODUCTS: Product[] = [
  { id: 1, name: "Kablosuz Kulaklık", price: 1250, emoji: "🎧", category: "Elektronik" },
  { id: 2, name: "Akıllı Saat", price: 3400, emoji: "⌚", category: "Elektronik" },
  { id: 3, name: "Kahve Makinesi", price: 2100, emoji: "☕", category: "Mutfak" },
  { id: 4, name: "Sırt Çantası", price: 750, emoji: "🎒", category: "Aksesuar" },
  { id: 5, name: "Gaming Mouse", price: 900, emoji: "🖱️", category: "Elektronik" },
  { id: 6, name: "Termos", price: 550, emoji: "🥤", category: "Mutfak" },
];

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<AuthMode>('login');
  const [authError, setAuthError] = useState('');
  
  const [formData, setFormData] = useState({ firstName: '', lastName: '', email: '', password: '' });
  
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  
  const [selectedCategory, setSelectedCategory] = useState('Tümü');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState([{ id: 1, text: "Merhaba! Size nasıl yardımcı olabilirim?", sender: 'ai', time: '23:41' }]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  // Hızlı sorular menüsü için yeni state
  const [showQuickReplies, setShowQuickReplies] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const addToCart = (product: Product) => {
    setCartItems(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item => item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item);
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };

  const removeFromCart = (productId: number) => {
    setCartItems(prev => {
      const existing = prev.find(item => item.id === productId);
      if (existing && existing.quantity > 1) {
        return prev.map(item => item.id === productId ? { ...item, quantity: item.quantity - 1 } : item);
      }
      return prev.filter(item => item.id !== productId);
    });
  };

  const handleAuthSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError('');
    const storedUsers = JSON.parse(localStorage.getItem('kobi_users') || '[]');

    if (authMode === 'register') {
      if (storedUsers.find((u: any) => u.email === formData.email)) {
        setAuthError('Bu e-posta zaten kayıtlı!');
        return;
      }
      const newUser = { ...formData };
      storedUsers.push(newUser);
      localStorage.setItem('kobi_users', JSON.stringify(storedUsers));
      setCurrentUser(newUser);
      setIsLoggedIn(true);
      setShowAuthModal(false);
    } else {
      const user = storedUsers.find((u: any) => u.email === formData.email && u.password === formData.password);
      if (user) {
        setCurrentUser(user);
        setIsLoggedIn(true);
        setShowAuthModal(false);
      } else {
        setAuthError('E-posta veya şifre hatalı!');
      }
    }
  };

  const sendMessage = (text: string) => {
    if (!text.trim()) return;
    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setMessages(prev => [...prev, { id: Date.now(), text: text, sender: 'user', time: now }]);
    setInputValue('');
    setIsTyping(true);
    setShowQuickReplies(false); // Menü açıksa kapat
    
    setTimeout(() => {
      let response = "Harika bir seçim! Bu ürün stoklarımızda mevcut.";
      if (text.includes("Kargom")) response = "Siparişiniz şu an hazırlık aşamasında, en kısa sürede kargoya verilecektir.";
      if (text.includes("Fırsatlı")) response = "Bugüne özel Kahve Makinelerinde %20 indirim sizi bekliyor!";
      
      setMessages(prev => [...prev, { id: Date.now() + 1, text: response, sender: 'ai', time: now }]);
      setIsTyping(false);
    }, 1500);
  };

  const handleSend = () => sendMessage(inputValue);

  const filteredProducts = selectedCategory === 'Tümü' 
    ? PRODUCTS 
    : PRODUCTS.filter(p => p.category === selectedCategory);

  const cartTotal = cartItems.reduce((acc, curr) => acc + (curr.price * curr.quantity), 0);
  const cartCount = cartItems.reduce((acc, curr) => acc + curr.quantity, 0);

  return (
    <div style={styles.appContainer} onClick={() => { setIsProfileOpen(false); setIsCartOpen(false); setShowQuickReplies(false); }}>
      
      <style>{`
        @keyframes typing {
          0% { opacity: 0.3; transform: translateY(0px); }
          50% { opacity: 1; transform: translateY(-3px); }
          100% { opacity: 0.3; transform: translateY(0px); }
        }
        .typing-dot {
          width: 6px;
          height: 6px;
          margin: 0 2px;
          background-color: #94a3b8;
          border-radius: 50%;
          display: inline-block;
          animation: typing 1.4s infinite ease-in-out;
        }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        .dropdown-item:hover {
          background-color: #f8fafc !important;
          color: #1e3a8a !important;
        }
        .quick-reply-btn:hover {
          background-color: #f1f5f9 !important;
        }
      `}</style>

      {/* Auth Modal, Navbar ve Sidebar kısımları değişmedi... */}
      {showAuthModal && (
        <div style={styles.modalOverlay} onClick={() => setShowAuthModal(false)}>
          <div style={styles.modalContent} onClick={e => e.stopPropagation()}>
            <div style={styles.modalHeader}>
              <h2 style={{margin:0}}>{authMode === 'login' ? 'Giriş Yap' : 'Hesap Oluştur'}</h2>
              <button style={styles.closeBtnSmall} onClick={() => setShowAuthModal(false)}>✕</button>
            </div>
            {authError && <div style={styles.errorBox}>{authError}</div>}
            <form onSubmit={handleAuthSubmit} style={styles.authForm}>
              {authMode === 'register' && (
                <div style={{display:'flex', gap:'10px'}}>
                  <input placeholder="Ad" required style={{ ...styles.input, flex: 1, minWidth: 0 }} onChange={e => setFormData({...formData, firstName: e.target.value})} />
                  <input placeholder="Soyad" required style={{ ...styles.input, flex: 1, minWidth: 0 }} onChange={e => setFormData({...formData, lastName: e.target.value})} />
                </div>
              )}
              <input type="email" placeholder="E-posta" required style={styles.input} onChange={e => setFormData({...formData, email: e.target.value})} />
              <input type="password" placeholder="Şifre" required style={styles.input} onChange={e => setFormData({...formData, password: e.target.value})} />
              <button type="submit" style={styles.submitBtn}>{authMode === 'login' ? 'Giriş Yap' : 'Üye Ol'}</button>
            </form>
            <div style={styles.modalFooter}>
              {authMode === 'login' ? 
                <span onClick={() => setAuthMode('register')}>Hesabın yok mu? <b>Üye Ol</b></span> : 
                <span onClick={() => setAuthMode('login')}>Zaten üye misin? <b>Giriş Yap</b></span>}
            </div>
          </div>
        </div>
      )}

      <header style={styles.navbar}>
        <div style={styles.logo} onClick={() => setSelectedCategory('Tümü')}>KOBİ-MART</div>
        <div style={styles.searchBar}>
          <input placeholder="Ürün ara..." style={styles.searchInput} />
        </div>
        <div style={styles.navIcons}>
          <div style={{position: 'relative'}}>
            <span style={{...styles.iconBtn, cursor: 'pointer'}} onClick={(e) => { e.stopPropagation(); setIsCartOpen(!isCartOpen); }}>🛒 ({cartCount})</span>
            {isCartOpen && (
              <div style={styles.cartDropdown} onClick={e => e.stopPropagation()}>
                <div style={styles.dropdownHeader}><strong>Sepetim</strong></div>
                <div style={{maxHeight: '200px', overflowY: 'auto'}}>
                  {cartItems.length === 0 ? (
                    <div style={{padding: '15px', fontSize: '13px', color: '#64748b'}}>Sepetiniz boş</div>
                  ) : (
                    cartItems.map(item => (
                      <div key={item.id} style={styles.cartItem}>
                        <div style={{display:'flex', flexDirection:'column'}}>
                          <span>{item.emoji} {item.name}</span>
                          <span style={{fontSize:'10px', color:'#94a3b8'}}>{item.quantity} x ₺{item.price}</span>
                        </div>
                        <button 
                          onClick={() => removeFromCart(item.id)}
                          style={{border:'none', background:'#fee2e2', color:'#ef4444', borderRadius:'4px', cursor:'pointer', padding:'2px 8px'}}
                        >
                          Kaldır
                        </button>
                      </div>
                    ))
                  )}
                </div>
                {cartItems.length > 0 && (
                  <div style={styles.cartFooter}>
                    <strong>Toplam: ₺{cartTotal}</strong>
                    <button style={{...styles.submitBtn, padding: '5px', marginTop: '10px', fontSize: '12px'}}>Satın Al</button>
                  </div>
                )}
              </div>
            )}
          </div>
          {isLoggedIn ? (
            <div style={{position:'relative'}}>
              <div style={styles.profileCircle} onClick={(e) => {e.stopPropagation(); setIsProfileOpen(!isProfileOpen)}}>
                {currentUser.firstName[0].toUpperCase()}{currentUser.lastName[0].toUpperCase()}
              </div>
              {isProfileOpen && (
                <div style={styles.dropdown}>
                  <div style={styles.dropdownHeader}>
                    <strong>{currentUser.firstName} {currentUser.lastName}</strong>
                    <div style={{fontSize: '11px', color: '#94a3b8'}}>{currentUser.email}</div>
                  </div>
                  <div className="dropdown-item" style={styles.dropdownItem}>📦 Siparişlerim</div>
                  <div className="dropdown-item" style={styles.dropdownItem}>💳 Ödeme Bilgilerim</div>
                  <div className="dropdown-item" style={styles.dropdownItem}>📍 Adreslerim</div>
                  <div className="dropdown-item" style={styles.dropdownItem}>🚚 Kargom Nerede?</div>
                  <div style={styles.dropdownDivider}></div>
                  <div className="dropdown-item" style={{...styles.dropdownItem, color: '#ef4444'}} onClick={() => setIsLoggedIn(false)}>🚪 Çıkış Yap</div>
                </div>
              )}
            </div>
          ) : (
            <button style={styles.loginBtn} onClick={() => {setAuthMode('login'); setShowAuthModal(true)}}>Giriş Yap</button>
          )}
        </div>
      </header>

      <div style={styles.mainLayout}>
        <aside style={styles.sidebar}>
          <h3 style={styles.sideTitle}>Kategoriler</h3>
          {['Tümü', 'Elektronik', 'Mutfak', 'Aksesuar'].map(cat => (
            <div key={cat} 
                 style={{...styles.sideItem, color: selectedCategory === cat ? '#1e3a8a' : '#64748b', fontWeight: selectedCategory === cat ? 'bold' : 'normal'}}
                 onClick={() => setSelectedCategory(cat)}>
              {cat}
            </div>
          ))}
        </aside>

        <main style={styles.content}>
          <div style={styles.banner}>
             {isLoggedIn ? `🌟 Hoş geldin ${currentUser.firstName}! Senin için seçtiklerimize göz at.` : "🚀 Alışveriş asistanı için hemen giriş yapın."}
          </div>
          <div style={styles.productGrid}>
            {filteredProducts.map(p => (
              <div key={p.id} style={styles.productCard}>
                <div style={styles.productImg}>{p.emoji}</div>
                <div style={styles.productInfo}>
                  <div style={{fontWeight:'bold'}}>₺{p.price}</div>
                  <div style={{fontSize:'14px', color:'#475569'}}>{p.name}</div>
                  <button style={styles.addBtn} onClick={() => addToCart(p)}>Sepete Ekle</button>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>

      <div style={styles.chatFloatingContainer}>
        {isChatOpen ? (
          <div style={styles.chatWindow}>
            <div style={styles.chatHeader}>
              <div style={{display:'flex', alignItems:'center', gap:'8px'}}>
                <div style={styles.onlineDot}></div>
                <span>KOBİ-AI Asistan</span>
              </div>
              <button style={styles.closeBtnSmall} onClick={() => setIsChatOpen(false)}>✕</button>
            </div>
            <div style={styles.chatBody}>
              {messages.map(m => (
                <div key={m.id} style={{display:'flex', gap:'10px', alignItems: 'flex-end', justifyContent: m.sender === 'user' ? 'flex-end' : 'flex-start'}}>
                  {m.sender === 'ai' && (
                    <div style={styles.chatBubbleAvatar}>
                       <img src={aiAvatar} alt="KOBİ-AI Avatar" style={{width: '100%', height: '100%'}} />
                    </div>
                  )}
                  <div style={{display:'flex', flexDirection:'column', alignItems: m.sender === 'user' ? 'flex-end' : 'flex-start'}}>
                    <div style={{...styles.bubble, backgroundColor: m.sender === 'user' ? '#1e3a8a' : 'white', color: m.sender === 'user' ? 'white' : '#1e293b', borderRadius: m.sender === 'user' ? '15px 15px 0 15px' : '0 15px 15px 15px'}}>
                      {m.text}
                    </div>
                    <span style={styles.chatTime}>{m.time}</span>
                  </div>
                </div>
              ))}
              
              {isTyping && (
                <div style={{display:'flex', gap:'10px', alignItems: 'flex-end'}}>
                  <div style={styles.chatBubbleAvatar}>
                    <img src={aiAvatar} alt="KOBİ-AI Avatar" style={{width: '100%', height: '100%'}} />
                  </div>
                  <div style={styles.typingBubble}>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                    <div className="typing-dot"></div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* GÜNCELLENEN INPUT ALANI */}
            <div style={{...styles.chatInputArea, position: 'relative'}}>
              {/* Hızlı Soru Menüsü */}
              {showQuickReplies && (
                <div style={{
                  position: 'absolute',
                  bottom: '65px',
                  right: '15px',
                  backgroundColor: 'white',
                  borderRadius: '12px',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.15)',
                  width: '200px',
                  zIndex: 1001,
                  display: 'flex',
                  flexDirection: 'column',
                  overflow: 'hidden',
                  border: '1px solid #e2e8f0'
                }}>
                  {[
                    { label: "🚚 Kargom nerede?", text: "🚚 Kargom nerede?" },
                    { label: "🔥 Fırsatlı ürünler?", text: "🔥 Fırsatlı ürünler neler?" },
                    { label: "💳 Ödeme yöntemleri", text: "💳 Ödeme yöntemleri" }
                  ].map((phrase, idx) => (
                    <button 
                      key={idx}
                      onClick={() => sendMessage(phrase.text)}
                      style={{
                        padding: '12px 15px',
                        border: 'none',
                        background: 'none',
                        textAlign: 'left',
                        fontSize: '13px',
                        cursor: 'pointer',
                        borderBottom: idx === 2 ? 'none' : '1px solid #f1f5f9'
                      }}
                      className="dropdown-item"
                    >
                      {phrase.label}
                    </button>
                  ))}
                </div>
              )}

              <input 
                value={inputValue} 
                onChange={e => setInputValue(e.target.value)} 
                onKeyPress={e => e.key === 'Enter' && handleSend()} 
                placeholder="Asistana sorun..." 
                style={styles.chatInput} 
              />
              
              {/* Hızlı Soru Butonu */}
              <button 
                onClick={(e) => { e.stopPropagation(); setShowQuickReplies(!showQuickReplies); }}
                style={{...styles.sendIconBtn, backgroundColor: '#f1f5f9', color: '#000000', fontSize: '16px'}}
              >
                ⚡
              </button>
              
              <button onClick={handleSend} style={styles.sendIconBtn}>➤</button>
            </div>
          </div>
        ) : (
          <button style={styles.chatTriggerBtn} onClick={() => setIsChatOpen(true)}>✨ KOBİ-AI Sor</button>
        )}
      </div>
    </div>
  );
}

// Styles objesi aynı kaldı...
const styles: { [key: string]: React.CSSProperties } = {
  appContainer: { minHeight: '100vh', backgroundColor: '#f8fafc', fontFamily: 'Inter, sans-serif' },
  navbar: { height: '70px', backgroundColor: 'white', display: 'flex', alignItems: 'center', padding: '0 5%', borderBottom: '1px solid #e2e8f0', position: 'sticky', top: 0, zIndex: 100 },
  logo: { fontSize: '24px', fontWeight: '800', color: '#1e3a8a', cursor: 'pointer' },
  searchBar: { flex: 1, display: 'flex', justifyContent: 'center' },
  searchInput: { width: '60%', padding: '10px 20px', borderRadius: '20px', border: '1px solid #e2e8f0', outline: 'none' },
  navIcons: { display: 'flex', gap: '20px', alignItems: 'center' },
  loginBtn: { backgroundColor: '#1e3a8a', color: 'white', border: 'none', padding: '8px 20px', borderRadius: '20px', fontWeight: 'bold', cursor: 'pointer' },
  profileCircle: { width: '38px', height: '38px', backgroundColor: '#1e3a8a', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', fontWeight: 'bold', border: '2px solid #e2e8f0' },
  
  dropdown: { position: 'absolute', top: '50px', right: 0, backgroundColor: 'white', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)', width: '220px', overflow: 'hidden', border: '1px solid #f1f5f9', zIndex: 200 },
  cartDropdown: { position: 'absolute', top: '40px', right: 0, backgroundColor: 'white', borderRadius: '12px', boxShadow: '0 10px 15px rgba(0,0,0,0.1)', width: '250px', border: '1px solid #f1f5f9', zIndex: 200 },
  cartItem: { padding: '10px 15px', borderBottom: '1px solid #f1f5f9', fontSize: '12px', display: 'flex', justifyContent: 'space-between', alignItems:'center' },
  cartFooter: { padding: '15px', textAlign: 'center', fontSize: '14px', backgroundColor: '#f8fafc' },
  dropdownHeader: { padding: '15px', borderBottom: '1px solid #f1f5f9', backgroundColor: '#f8fafc' },
  dropdownItem: { padding: '12px 15px', fontSize: '13px', cursor: 'pointer', color: '#475569', transition: 'all 0.2s', display: 'flex', alignItems: 'center', gap: '10px' },
  dropdownDivider: { height: '1px', backgroundColor: '#f1f5f9', margin: '5px 0' },

  mainLayout: { display: 'flex', padding: '20px 5%', gap: '30px' },
  sidebar: { width: '220px', backgroundColor: 'white', padding: '20px', borderRadius: '15px', height: 'fit-content', border: '1px solid #f1f5f9' },
  sideTitle: { fontSize: '16px', fontWeight: 'bold', marginBottom: '15px' },
  sideItem: { padding: '8px 0', cursor: 'pointer', fontSize: '14px' },
  
  content: { flex: 1 },
  banner: { padding: '20px', backgroundColor: '#eff6ff', borderRadius: '15px', marginBottom: '20px', textAlign: 'center', fontWeight: 'bold', color: '#1e40af' },
  productGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '20px' },
  productCard: { backgroundColor: 'white', borderRadius: '12px', overflow: 'hidden', border: '1px solid #f1f5f9' },
  productImg: { height: '120px', fontSize: '40px', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f8fafc' },
  productInfo: { padding: '15px' },
  addBtn: { width: '100%', marginTop: '10px', padding: '8px', backgroundColor: '#f59e0b', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' },

  chatFloatingContainer: { position: 'fixed', right: '30px', bottom: '30px', zIndex: 1000 },
  chatTriggerBtn: { padding: '12px 24px', backgroundColor: '#1e3a8a', color: 'white', borderRadius: '30px', border: 'none', fontWeight: 'bold', cursor: 'pointer', boxShadow: '0 4px 12px rgba(0,0,0,0.2)' },
  chatWindow: { width: '350px', height: '500px', backgroundColor: 'white', borderRadius: '20px', display: 'flex', flexDirection: 'column', overflow: 'hidden', boxShadow: '0 10px 25px rgba(0,0,0,0.1)' },
  chatHeader: { padding: '15px 20px', backgroundColor: '#1e3a8a', color: 'white', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  onlineDot: { width: '8px', height: '8px', backgroundColor: '#10b981', borderRadius: '50%' },
  chatBody: { flex: 1, padding: '15px', backgroundColor: '#f1f5f9', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '10px' },
  bubble: { padding: '10px 14px', maxWidth: '80%', fontSize: '13px', boxShadow: '0 1px 2px rgba(0,0,0,0.1)' },
  typingBubble: { backgroundColor: 'white', padding: '12px 16px', borderRadius: '0 15px 15px 15px', boxShadow: '0 1px 2px rgba(0,0,0,0.1)', display: 'flex', alignItems: 'center' },
  chatBubbleAvatar: { width: '30px', height: '30px', borderRadius: '50%', overflow: 'hidden', border: '1px solid #e2e8f0', flexShrink: 0 },
  chatTime: { fontSize: '10px', color: '#94a3b8', marginTop: '2px' },
  chatInputArea: { padding: '15px', borderTop: '1px solid #eee', display: 'flex', gap: '8px' },
  chatInput: { flex: 1, padding: '10px 15px', borderRadius: '20px', border: '1px solid #eee', outline: 'none' },
  sendIconBtn: { backgroundColor: '#1e3a8a', color: 'white', border: 'none', width: '35px', height: '35px', borderRadius: '50%', cursor: 'pointer' },

  modalOverlay: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 },
  modalContent: { backgroundColor: 'white', padding: '30px', borderRadius: '20px', width: '350px' },
  authForm: { display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '20px' },
  input: { padding: '12px', borderRadius: '10px', border: '1px solid #e2e8f0' },
  submitBtn: { backgroundColor: '#1e3a8a', color: 'white', padding: '12px', borderRadius: '10px', border: 'none', fontWeight: 'bold', cursor: 'pointer' },
  errorBox: { backgroundColor: '#fee2e2', color: '#ef4444', padding: '10px', borderRadius: '8px', fontSize: '12px', textAlign: 'center' },
  closeBtnSmall: { background: 'none', border: 'none', color: 'inherit', cursor: 'pointer', fontSize: '16px' },
  modalHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  modalFooter: { textAlign: 'center', marginTop: '15px', fontSize: '13px', cursor: 'pointer' }
};