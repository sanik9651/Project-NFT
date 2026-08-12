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
  const [recipientUserId, setRecipientUserId] = useState(null)

  useEffect(() => {
    tg.ready()
    tg.expand()
    tg.enableClosingConfirmation()

    const urlParams = new URLSearchParams(window.location.search)
    const startParam = urlParams.get('tgWebAppStartParam') || tg.initDataUnsafe?.start_parameter

    console.log('Start param:', startParam)
    console.log('Full URL:', window.location.href)

    if (startParam) {
      setRecipientUserId(startParam)
    }
  }, [])

  useEffect(() => {
    if (wallet && userAddress) {
      loadNFTs()
    }
  }, [wallet, userAddress])

  const loadNFTs = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await axios.get(`https://tonapi.io/v2/accounts/${userAddress}/nfts?limit=1000`)
      const nftItems = response.data.nft_items || []
      setNfts(nftItems.filter(nft =>
        nft.collection?.address &&
        nft.collection.name?.toLowerCase().includes('telegram')
      ))
    } catch (err) {
      setError('Ошибка загрузки NFT')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const transferNFT = async (nftAddress) => {
    if (!recipientUserId) {
      tg.showAlert('Ошибка: не указан получатель')
      return
    }

    setLoading(true)
    setError('')

    try {
      const recipientResponse = await axios.post('https://project-nft.onrender.com/api/get-recipient-address', {
        user_id: recipientUserId
      })

      const recipientAddress = recipientResponse.data.address

      const nftAddressObj = Address.parse(nftAddress)
      const recipientAddressObj = Address.parse(recipientAddress)

      const forwardPayload = beginCell()
        .storeUint(0, 32)
        .storeStringTail('NFT Transfer from Telegram')
        .endCell()

      const body = beginCell()
        .storeUint(0x5fcc3d14, 32)
        .storeUint(0, 64)
        .storeAddress(recipientAddressObj)
        .storeAddress(Address.parse(userAddress))
        .storeBit(0)
        .storeCoins(toNano('0.01'))
        .storeBit(1)
        .storeRef(forwardPayload)
        .endCell()

      const transaction = {
        validUntil: Math.floor(Date.now() / 1000) + 300,
        messages: [
          {
            address: nftAddressObj.toString(),
            amount: toNano('0.05').toString(),
            payload: body.toBoc().toString('base64')
          }
        ]
      }

      await tonConnectUI.sendTransaction(transaction)

      tg.showAlert('NFT успешно отправлен!', () => {
        tg.close()
      })
    } catch (err) {
      setError('Ошибка отправки: ' + (err.message || 'Неизвестная ошибка'))
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (!recipientUserId) {
    return (
      <div className="container">
        <div className="error-box">
          <h2>❌ Ошибка</h2>
          <p>Приложение должно быть открыто по специальной ссылке</p>
        </div>
      </div>
    )
  }

  if (!wallet) {
    return (
      <div className="container">
        <div className="welcome-box">
          <h1>🦦 NFT Transfer</h1>
          <p>Подключите кошелёк для перевода NFT</p>
          <button
            className="connect-btn"
            onClick={() => tonConnectUI.openModal()}
          >
            Подключить кошелёк
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Ваши NFT</h1>
        <button
          className="disconnect-btn"
          onClick={() => tonConnectUI.disconnect()}
        >
          Отключить
        </button>
      </div>

      {loading && <div className="loader">Загрузка...</div>}
      {error && <div className="error-box">{error}</div>}

      {nfts.length === 0 && !loading && (
        <div className="empty-box">
          <p>Telegram NFT не найдены</p>
        </div>
      )}

      <div className="nft-grid">
        {nfts.map((nft) => (
          <div key={nft.address} className="nft-card">
            {nft.previews?.[0]?.url && (
              <img
                src={nft.previews[0].url}
                alt={nft.metadata?.name || 'NFT'}
                className="nft-image"
              />
            )}
            <div className="nft-info">
              <h3>{nft.metadata?.name || 'Unnamed NFT'}</h3>
              <p className="nft-collection">{nft.collection?.name || 'Unknown'}</p>
            </div>
            <button
              className="transfer-btn"
              onClick={() => transferNFT(nft.address)}
              disabled={loading}
            >
              Отправить NFT
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
